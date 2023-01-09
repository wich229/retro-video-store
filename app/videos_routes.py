from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

# GET /videos
@videos_bp.route("", methods=["GET"])
def get_videos_optional_query():
    videos_query = Video.query
    
    title_query = request.args.get("title")
    if title_query == "title":
        videos_query = videos_query.order_by(Video.title.asc())

    release_date_query = request.args.get("release_date")
    if release_date_query == "release_date":
        videos_query = videos_query.order_by(Video.release_date.asc())

    videos = videos_query.all()
    
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())

    return jsonify(videos_response)


# GET /videos/<id>
@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    video_data = validate_model(Video,video_id)

    return video_data.to_dict()


# POST /videos
@videos_bp.route("", methods=["POST"])
def create_video():
    video_data = request.get_json()
    
    ###### refactor ######
    if "title" not in video_data.keys():
        abort(make_response({"details": f"Request body must include title."}, 400))
    if "release_date" not in video_data.keys():
        abort(make_response({"details": f"Request body must include release_date."}, 400))
    if  "total_inventory" not in video_data.keys():
        abort(make_response({"details": f"Request body must include total_inventory."}, 400))
        
    new_video = Video(
        title = video_data["title"],
        release_date = video_data["release_date"],
        total_inventory = video_data["total_inventory"]
    )
    

    db.session.add(new_video)
    db.session.commit()

    return make_response(jsonify(new_video.to_dict()), 201)

# PUT /videos/<id>
@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    video = validate_model(Video,video_id)
    video_data = request.get_json()
    
    ###### refactor ######
    if "title" not in video_data.keys():
        abort(make_response({"details": f"Request body must include title."}, 400))
    if "release_date" not in video_data.keys():
        abort(make_response({"details": f"Request body must include release_date."}, 400))
    if  "total_inventory" not in video_data.keys():
        abort(make_response({"details": f"Request body must include total_inventory."}, 400))
        
    video.title = video_data["title"]
    video.release_date =video_data["release_date"]
    video.total_inventory = video_data["total_inventory"]

    db.session.commit()

    return make_response(video_data, 200)

# DELETE /videos/<id>
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_customer_by_id(video_id):
    video_to_delete = validate_model(Video,video_id)
    db.session.delete(video_to_delete)
    db.session.commit()

    msg = f"Customer {video_to_delete.id} successfully deleted"
    return make_response(jsonify({"id":video_to_delete.id, "message":msg}), 200)

# GET /id/rentals
@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_video(video_id):
    video = validate_model(Video, video_id)
    # rentals = Rental.query.all()
    rentals = Rental.query.filter(Rental.video_id == video.id).all()
    customer_query = Customer.query

    # sort queries for title and release date
    sort_query = request.args.get("sort")

    if sort_query == "name":
        customer_query = customer_query.order_by(Customer.name.asc())
    elif sort_query == "postal_code":
        customer_query = customer_query.order_by(Customer.postal_code.asc())

    #exception handling: page_num and count queries are invalid
    try:
        page_num_query = int(request.args.get("page_num"))
    except:
        page_num_query = None

    try :
        count_query = int(request.args.get("count"))
    except:
        count_query = None

    if page_num_query and count_query:
        customers = customer_query.paginate(page = page_num_query, per_page = count_query).items
    elif page_num_query:
        customers = customer_query.paginate(page = page_num_query).items
    elif count_query:
        customers = customer_query.paginate(per_page = count_query).items
    else:
        customers = customer_query.all()

    # get rentals
    customer_list = []
    for rental in rentals:
        customer_list.append(Customer.query.get(rental.customer_id))
    
    rental_response = []
    for customer in customers:
        if customer in customer_list:
            rental_response.append(customer.to_dict())

    return make_response(jsonify(rental_response), 200)
