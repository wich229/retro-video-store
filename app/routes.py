from datetime import date, datetime

from flask import Blueprint, jsonify, request, abort, make_response

from app import db
from app.models.customer import Customer
from app.models.video import Video


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



# CUSTOMERS
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_dict())
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
        Customer.query.filter_by(id=customer_id).delete()

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

# VIDEOS
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
VIDEO_PARAMS = ("title", "release_date", "total_inventory")

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
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
        Video.query.filter_by(id=video_id).delete()

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