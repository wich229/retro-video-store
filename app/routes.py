from datetime import date, timedelta

from flask import Blueprint, jsonify, request, abort, make_response

from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
CUSTOMER_PARAMS = ("name", "postal_code", "phone")

def validate_params_or_abort(body, params):
    for attr in params:
        if attr not in body:
            response = make_response({"details": f"Request body must include {attr}."}, 400)
            abort(response)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} was not found"}, 404))
    
    return model

def order_customers(sort_query):
    if sort_query == "name":
        customers = Customer.query.order_by(Customer.name.asc())
    elif sort_query == "postal_code":
        customers = Customer.query.order_by(Customer.postal_code.asc())
    elif sort_query == "postal_code":
        customers = Customer.query.order_by(Customer.registered_at.asc())
    else:
        customers = Customer.query.order_by(Customer.id.asc())
    return customers



    # CUSTOMERS
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    sort_query = request.args.get("sort")
    per_page = request.args.get("n")
    if per_page:
        per_page = int(per_page)
    pages = request.args.get("p")
    if pages:
        pages = int(pages)
    customer_query = order_customers(sort_query)
    customer_page = customer_query.paginate(page=pages,per_page=per_page)
    customers = customer_page.items
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
    print(customers_response)
    return jsonify(customers_response)


@customers_bp.route("", methods = ["POST"])
def create_customers():
    request_body = request.get_json()

    validate_params_or_abort(request_body, CUSTOMER_PARAMS)

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
    )
    db.session.add(new_customer)
    db.session.commit()

    return {"id": new_customer.id}, 201


@customers_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_one_customer(customer_id):

    customer = validate_model(Customer, customer_id)

    if request.method == "GET":
        return jsonify(customer.to_dict())

    elif request.method == "DELETE":
        Rental.query.filter_by(id=customer_id).delete()

        db.session.delete(customer)
        db.session.commit()

        return {"id": customer.id}
    
    elif request.method == "PUT":
        body = request.get_json()
        validate_params_or_abort(body, CUSTOMER_PARAMS)
        customer.name = body["name"]
        customer.postal_code = body["postal_code"]
        customer.phone = body["phone"]

        db.session.commit()
        
        return customer.to_dict()

@customers_bp.route("/<customer_id>/rentals", methods = ["GET"])
def get_videos_from_customer(customer_id):
    customer = validate_model(Customer, customer_id)
    videos = db.session.query(Video).join(Rental).filter_by(customer_id=customer_id).filter_by(checked_in = False)
    return jsonify([video.to_dict() for video in videos])

@customers_bp.route("/<customer_id>/history", methods = ["GET"])
def get_rental_history_from_customer(customer_id):
    customer = validate_model(Customer, customer_id)    
    rental_history =db.session.query(Video, Rental).join(Rental).filter_by(customer_id=customer_id).filter_by(checked_in = True).all()
    rental_response = []
    for video, rental in rental_history:
        rental_response.append({
            "title": video.title,
            "checkout_date": rental.due_date - timedelta(days=7),
            "due_date": rental.due_date
        })
    return jsonify(rental_response)


# VIDEOS
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
VIDEO_PARAMS = ("title", "release_date", "total_inventory")

def order_videos(sort_query):
    if sort_query == "title":
        videos = Video.query.order_by(Video.title.asc()).all()
    elif sort_query == "release_date":
        videos = Video.query.order_by(Video.release_date.asc()).all()
    else:
        videos = Video.query.order_by(Video.id.asc()).all()
    return videos

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    sort_query = request.args.get("sort")
    videos = order_videos(sort_query)
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())
    return jsonify(videos_response)

@videos_bp.route("", methods=["POST"])
def create_videos():
    body = request.get_json()
    validate_params_or_abort(body, VIDEO_PARAMS)

    video = Video(
        title = body["title"],
        release_date = body["release_date"],
        total_inventory = body["total_inventory"]
    )

    db.session.add(video)
    db.session.commit()

    return video.to_dict(), 201

@videos_bp.route("/<video_id>", methods = ["GET", "DELETE", "PUT"])
def handle_one_video(video_id):
    video = validate_model(Video, video_id)

    if request.method == "GET":
        return jsonify(video.to_dict())

    elif request.method == "DELETE":
        Rental.query.filter_by(id=video_id).delete()

        db.session.delete(video)
        db.session.commit()

        return {"id": video.id}
    
    elif request.method == "PUT":
        body = request.get_json()
        validate_params_or_abort(body, VIDEO_PARAMS)
        video.title = body["title"]
        video.total_inventory = body["total_inventory"]
        video.release_date = body["release_date"]

        db.session.commit()
        
        return video.to_dict()

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_customers_from_video(video_id):
    video = validate_model(Video, video_id)
    customers = db.session.query(Customer).join(Rental).filter_by(video_id = video_id).filter_by(checked_in = False)
    return jsonify([customer.to_dict() for customer in customers])



# RENTALS
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
RENTAL_PARAMS = ("customer_id", "video_id")


@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    body = request.get_json()

    validate_params_or_abort(body, RENTAL_PARAMS)

    video_id, customer_id = body["video_id"], body["customer_id"]

    video = validate_model(Video, video_id)
    customer = validate_model(Customer, customer_id)

    if video.available_inventory == 0:
        return {"message": "Could not perform checkout"}, 400

    due_date = date.today() + timedelta(days=7)
    rental = Rental(
        customer_id=customer_id,
        video_id=video_id,
        due_date = due_date
    )

    db.session.add(rental)
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.commit()
    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    body = request.get_json()

    validate_params_or_abort(body, RENTAL_PARAMS)

    video_id, customer_id = body["video_id"], body["customer_id"]

    video = validate_model(Video, video_id)
    customer = validate_model(Customer, customer_id)

    rentals = Rental.query.filter_by(customer_id = customer_id).filter_by(video_id = video_id).all()
    if not rentals:
        return {"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400
    
    for rental in rentals:
        if rental.checked_in:
            return {"message": f"Customer {customer_id} already checked in video {video_id}"}, 400
        rental.checked_in = True
    customer.videos_checked_out_count -= 1
    video.available_inventory += 1

    db.session.commit()

    return {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }
