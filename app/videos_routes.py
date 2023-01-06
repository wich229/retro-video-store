from app import db
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model

videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")

# GET /videos
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos_query = Video.query
    
    ###### refactor ######
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        videos_query = videos_query.order_by(Video.name.asc())
    if sort_query == "desc":
        videos_query = videos_query.order_by(Video.name.desc())
    
    videos = videos_query.all()
    
    videos_response = []
    for video in videos:
        videos_response.append(video.to_dict())

    return jsonify(videos_response)


# GET /vidoes/<id>
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
    video_data = validate_model(Video,video_id)
    db.session.delete(video_data)
    db.session.commit()

    return make_response(jsonify(video_data.to_dict()), 200)

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def rentals_by_video(video_id):
    video = validate_model(Video, video_id)
    rentals = Rental.query.all()
    
    rentals_response = []
    for rental in rentals:
        if rental.video_id == video.id:
            customer = Customer.query.get(rental.customer_id)
            rentals_response.append({"due_date": rental.due_date,
                                "name": customer.name,
                                "phone": customer.phone,
                                "postal_code": customer.postal_code
                                })


    return make_response(jsonify(rentals_response), 200)
"""
GET /videos/<id>/rentals

List the customers who currently have the video checked out
Required Arguments
Arg 	Type 	Details
id 	integer 	The id of the video
Response

Typical success response is a list of customers with the due date:

Status: 200

[
    {
        "due_date": "Thu, 13 May 2021 21:36:38 GMT",
        "name": "Edith Wong",
        "phone": "(555) 555-5555",
        "postal_code": "99999",
    },
    {
        "due_date": "Thu, 13 May 2021 21:36:47 GMT",
        "name": "Ricarda Mowery",
        "phone": "(555) 555-5555",
        "postal_code": "99999",
    }
]

Errors and Edge Cases to Check

    The API should return back detailed errors and a status 404: Not Found if the video does not exist
    The API should return an empty list if the video is not checked out to any customers.


"""