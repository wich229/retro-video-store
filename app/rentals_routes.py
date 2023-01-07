from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model
import datetime 

rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


# POST /rentals/check-out
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_video():
    checkout_data = request.get_json()
    
    # check vlaid customer and video
    try:
        customer = validate_model(Customer, checkout_data["customer_id"])
        video = validate_model(Video, checkout_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
        
    
    # check if the customer did rent the video
    rentals = Rental.query.all()
    for rental in rentals:
        if (rental.customer_id == customer.id 
                and rental.video_id == video.id 
                and rental.status == "checked_out"):
            abort(make_response({"message":f"Customer {customer.id} \
                    is already renting video {video.id}."}, 400))

    #check video inventory
    if video.total_inventory <= 0:
        abort(make_response({"message":"Could not perform checkout"}, 400))
    
    # add and update "total_inventory" and "available_inventory" (in video)
    video.available_inventory = video.total_inventory - 1
    video.total_inventory -= 1
    
    # add and update "videos_checked_out_count" (in customer)
    customer.videos_checked_out_count += 1
    db.session.commit()
    
    # create new rental
    new_rental = Rental(
                        video_id = video.id,
                        customer_id = customer.id,
                        due_date = datetime.date.today() + datetime.timedelta(days=7),
                        status = "checked_out" 
                    )
    
    db.session.add(new_rental)
    db.session.commit()
    
    checkout_response = {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
    }
    
    return make_response(jsonify(checkout_response), 200)


# POST /rentals/check-in
@rentals_bp.route("/check-in", methods=["POST"])
def checkin_video():
    check_in_data = request.get_json()
    
    # check vlaid customer and video
    try:
        customer = validate_model(Customer, check_in_data["customer_id"])
        video = validate_model(Video, check_in_data["video_id"])
    except KeyError as err:
        abort(make_response({"message":f"Missing {err.args[0]}."}, 400))
    
    # check if the customer did rent the video
    rentals = Rental.query.all()
    rental_found = False

    for rental in rentals:
        if (rental.customer_id == customer.id 
                and rental.video_id == video.id 
                and rental.status == "checked_out"):
                rental_found = True

    if rental_found == False:
        msg = f"No outstanding rentals for customer {customer.id} and video {video.id}"
        abort(make_response({"message":msg}, 400))

    check_in_data["status"] = "checked_in"
    
    # add and update "total_inventory" and "available_inventory" (in video)
    video.available_inventory += 1
    video.total_inventory += 1
    
    # add and update "videos_checked_out_count" (in customer)
    customer.videos_checked_out_count -= 1
    db.session.commit()
    
    check_in_response = {
                    "customer_id": customer.id,
                    "video_id": video.id,
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory
                }
    ###########################################
    # we may need to check if we still        #
    # need the status if we want to delete    #
    # because we modify the rental instead of #
    # create a new rental                     # 
    ###########################################
    Rental.query.filter_by(customer_id = customer.id, video_id = video.id).delete()

    db.session.commit()
    return make_response(jsonify(check_in_response), 200)