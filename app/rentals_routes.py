from app import db
from app.models.rental import Rental
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model


rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


# POST /rentals/check-out

# POST /rentals/check-in