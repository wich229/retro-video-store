from app import db
from app.models.video import Video
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
