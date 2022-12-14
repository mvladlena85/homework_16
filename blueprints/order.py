from flask import Blueprint, jsonify, request
from db.models import Order, db
from tools import str_to_date, order_instance_to_dict

order_blueprint = Blueprint('order_blueprint', __name__)


@order_blueprint.route('/orders/')
def get_orders():
    """
    The view contains request for all orders
    :return: json
    """
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append(order_instance_to_dict(order))
    return jsonify(result), 200


@order_blueprint.route('/orders/<int:uid>/')
def get_orders_by_id(uid):
    """
    The view contains request for order by id
    :return: json
    """
    order = Order.query.get(uid)
    if order is not None:
        result = order_instance_to_dict(order)
        return jsonify(result), 200
    else:
        return "No such order", 404


@order_blueprint.route('/orders/', methods=['POST'])
def create_order():
    """
    The view allows to create new order
    :return: json
    """
    order_data = request.get_json()
    order = Order(name=order_data['name'],
                  description=order_data['description'],
                  start_date=str_to_date(order_data['start_date']),
                  end_date=str_to_date(order_data['end_date']),
                  address=order_data['address'],
                  price=order_data['price'],
                  customer_id=order_data['customer_id'],
                  executor_id=order_data['executor_id'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order_instance_to_dict(order)), 201


@order_blueprint.route('/orders/<int:uid>', methods=['PUT', 'DELETE'])
def change_order(uid):
    """
    The view contains following DB requests:
    - change order data
    - delete order by id
    """
    if request.method == 'PUT':
        data = request.json
        keys = data.keys()
        order = Order.query.get(uid)
        if "name" in keys:
            order.name = data["name"]
        if "description" in keys:
            order.description = data["description"]
        if "start_date" in keys:
            order.start_date = str_to_date(data["start_date"])
        if "end_date" in keys:
            order.end_date = str_to_date(data["end_date"])
        if "address" in keys:
            order.address = data["address"]
        if "price" in keys:
            order.price = data["price"]
        if "customer_id" in keys:
            order.customer_id = data["customer_id"]
        if "executor_id" in keys:
            order.executor_id = data["executor_id"]

        db.session.add(order)
        db.session.commit()

        order = Order.query.get(uid)

        result = order_instance_to_dict(order)
        return jsonify(result), 200

    elif request.method == 'DELETE':
        order = Order.query.get(uid)
        if order is not None:
            db.session.delete(order)
            db.session.commit()
        return '', 204
