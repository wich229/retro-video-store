from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, abort, make_response, request
"""
add 404 error checking if customer does not exist and edge cases 
"""
customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

# POST /customers 
@customers_bp.route("",methods=["POST"])
def create_customer():
    customer_data = request.get_json()
    new_customer = Customer(
        name = customer_data["name"],
        postal_code = customer_data["postal_code"],
        phone_number = customer_data["phone_number"],
        register_at = customer_data["register_at"],
        videos_checked_out_count = customer_data["videos_checked_out_count"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(f"Customer {new_customer.name} created", 201)

# GET /customers X
@customers_bp.route("", methods=["GET"])
def get_customers_optional_query():
    customer_query = Customer.query
    # queries??
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            customer_query = customer_query.order_by(Customer.videos_checked_out_count.desc())
        else:
            customer_query = customer_query.order_by(Customer.videos_checked_out_count.asc())
        

    customers = customer_query.all()
    customer_response = []
    for customer in customers:
        customer_response.append({
            "id": customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone_number": customer.phone_number,
            "register_at": customer.register_at,
            "videos_checked_out_count": customer.videos_checked_out_count
        })

    return jsonify(customer_response)

# GET /customers/<id>
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer_to_return = validate_id_and_return_customer(customer_id)

    return jsonify({
        "id": customer_to_return.id,
        "name": customer_to_return.name,
        "postal_code": customer_to_return.postal_code,
        "phone_number": customer_to_return.phone_number,
        "register_at": customer_to_return.register_at,
        "videos_checked_out_count": customer_to_return.videos_checked_out_count
    })

# PUT /customers/<id>
@customers_bp.route("/<customer_id>", methods=["PUT"])
def replace_customer_with_id(customer_id):
    customer_data = request.get_json()
    customer_to_update = validate_id_and_return_customer(customer_id)

    customer_to_update.name = customer_data["name"],
    customer_to_update.postal_code = customer_data["postal_code"],
    customer_to_update.phone_number = customer_data["phone_number"],
    customer_to_update.register_at = customer_data["register_at"],
    customer_to_update.videos_checked_out_count = customer_data["videos_checked_out_count"]

    db.session.commit()

    return make_response(f"Customer {customer_to_update.name} updated", 200)

# DELETE /customers/<id>
@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    customer_to_delete = validate_id_and_return_customer(customer_id)
    db.session.delete(customer_to_delete)
    db.session.commit()

    return make_response(f"Customer {customer_to_delete.name} deleted", 200)

# Helper Function
def validate_id_and_return_customer(customer_id):
    try:
        customer_id_as_int = int(customer_id)
    except:
        msg = f"Customer's id {customer_id} is not an integer"
        abort(make_response({"message": msg}, 400))

    customer = Customer.query.get(customer_id_as_int)
    if customer:
        return customer
    
    abort(make_response({"message": f"Customer with id {customer_id} not found"}, 404))
