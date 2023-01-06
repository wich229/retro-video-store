from app import db
from app.models import Video, Rental, Customer
from flask import Blueprint, jsonify, abort, make_response, request
from customers_routes import validate_model

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# POST
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    checkout_data = request.get_json()
    try:
        customer = Customer.query.get(checkout_data["customer_id"])
    except:
        abort(make_response({"message":f"Customer does not exist."}, 404))

    try:
        video = Video.query.get(checkout_data["video_id"])
    except:
        abort(make_response({"message":f"Video does not exist."}, 404))

    if checkout_data["available_inventory"] == 0:
        abort(make_response({"message":f"No available inventory."}, 400))
        
    new_rental = Rental(video_id = checkout_data["video_id"],
                            customer_id = checkout_data["customer_id"],
                            videos_checked_out_count = checkout_data["videos_checked_out_count"],
                            available_inventory = checkout_data["available_inventory"]
                            )
    





    """
    The API should return back detailed errors and a status 404: Not Found if the customer does not exist
    The API should return back detailed errors and a status 404: Not Found if the video does not exist
    The API should return back detailed errors and a status 400: Bad Request if the video does not have any available inventory before check out
"""
    
    # create a rental for the specific video and customer.
    # create a due date. The rental's due date is the seven days from the current date.
    pass
"""
def test_checkout_video(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 0
"""