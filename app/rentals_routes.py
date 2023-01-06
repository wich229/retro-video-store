from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request
import datetime 

rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

# POST
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    checkout_data = request.get_json()

    try:
        customer = Customer.query.get(checkout_data["customer_id"])
        video = Video.query.get(checkout_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
    
    if not customer:
        abort(make_response({"message":f"Customer does not exist."}, 404))

    if not video:
        abort(make_response({"message":f"Video does not exist."}, 404))

    #find how many copies of the video being checked out are already rented
    rentals = Rental.query.all()
    rental_count = 0
    for rental in rentals:
        if rental.video_id == video.id:
            rental_count += 1

    available_inventory = video.total_inventory - rental_count
    if available_inventory <= 0:
        abort(make_response({"message":"Could not perform checkout"}, 400))

    # not sure if we need to update video total_inventory
    video.total_inventory -= 1 

    new_rental = Rental(video_id = video.id,
                        customer_id = customer.id,
                        due_date = datetime.date.today() - datetime.timedelta(days=7),
                        status = "checked out" #not sure what status should be 
                        )

    check_out_response = {"customer_id": new_rental.customer_id,
                            "video_id": new_rental.video_id,
                            "due_date": new_rental.due_date,
                            "videos_checked_out_count": rental_count + 1,
                            "available_inventory": available_inventory - 1
                            } 
    db.session.add(new_rental)
    db.session.commit()

    return make_response(jsonify(check_out_response), 200)


@rentals_bp.route("/check-in", methods=["POST"])
def checkin_video():
    check_in_data = request.get_json()
    try:
        customer = Customer.query.get(check_in_data["customer_id"])
        video = Video.query.get(check_in_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
    
    if not customer:
        abort(make_response({"message":f"Customer does not exist."}, 404))

    if not video:
        abort(make_response({"message":f"Video does not exist."}, 404))
    
    rentals = Rental.query.all()
    rental_count = 0
    rental_found = False

    for rental in rentals:
        if rental.customer_id == customer.id:
            if rental.video_id == video.id:
                rental_found = True
            rental_count += 1

    if rental_found == False:
        msg = f"No outstanding rentals for customer {customer.id} and video {video.id}"
        abort(make_response({"message":msg}, 400))

    check_in_data["status"] = "checked_in"

    check_in_response = {
    "customer_id": customer.id,
    "video_id": video.id,
    "videos_checked_out_count": rental_count - 1,
    "available_inventory": video.total_inventory + 1
    }
    Rental.query.filter_by(customer_id=customer.id, video_id = video.id).delete()

    db.session.commit()
    return make_response(jsonify(check_in_response), 200)


