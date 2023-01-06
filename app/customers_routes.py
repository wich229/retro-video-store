from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
from app.routes_helper import validate_model


customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# POST /customers 
@customers_bp.route("",methods=["POST"])
def create_customer():
    customer_data = request.get_json()
    
    ###### refactor ######
    if "name" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include name."}, 400))
    if "postal_code" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include postal_code."}, 400))
    if  "phone" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include phone."}, 400))
        
    new_customer = Customer(
        name = customer_data["name"],
        postal_code = customer_data["postal_code"],
        phone = customer_data["phone"]
        # register_at = customer_data["register_at"]
        # videos_checked_out_count = customer_data["videos_checked_out_count"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(new_customer.to_dict()), 201)


# GET /customers X
@customers_bp.route("", methods=["GET"])
def get_customers_optional_query():
    customer_query = Customer.query
    
    ###### refactor ######
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        customer_query = customer_query.order_by(Customer.name.asc())
    if sort_query == "desc":
        customer_query = customer_query.order_by(Customer.name.desc())
    
    customers = customer_query.all()
    
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())

    return jsonify(customer_response)


# GET /customers/<id>
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer_to_return = validate_model(Customer,customer_id)

    return customer_to_return.to_dict()

# PUT /customers/<id>
@customers_bp.route("/<customer_id>", methods=["PUT"])
def replace_customer_with_id(customer_id):
    customer = validate_model(Customer,customer_id)
    customer_data = request.get_json()
    
    ###### refactor ######
    if "name" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include name."}, 400))
    if "postal_code" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include postal_code."}, 400))
    if  "phone" not in customer_data.keys():
        abort(make_response({"details": f"Request body must include phone."}, 400))
    
    customer.name = customer_data["name"]
    customer.postal_code = customer_data["postal_code"]
    customer.phone = customer_data["phone"]
    # customer_to_update.register_at = customer_data["register_at"]
    # customer_to_update.videos_checked_out_count = customer_data["videos_checked_out_count"]

    db.session.commit()

    return make_response(customer_data, 200)


# DELETE /customers/<id>
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    customer_to_delete = validate_model(Customer,customer_id)
    db.session.delete(customer_to_delete)
    db.session.commit()

    return make_response({"id":customer_to_delete.id}, 200)
