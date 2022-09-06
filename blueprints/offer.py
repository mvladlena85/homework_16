from flask import Blueprint, jsonify, request

from db import db
from db.models import Offer
from tools import offer_instance_to_dict

offer_blueprint = Blueprint('offer_blueprint', __name__)


@offer_blueprint.route('/offers/')
def get_offers():
    offers = Offer.query.all()
    result = []
    for offer in offers:
        result.append(offer_instance_to_dict(offer))
    return jsonify(result)


@offer_blueprint.route('/offers/<int:uid>')
def get_offers_by_id(uid):
    offer = Offer.query.get(uid)
    if offer is not None:
        result = offer_instance_to_dict(offer)
        return jsonify(result), 200
    else:
        return "No such offer", 204


@offer_blueprint.route('/offers/', methods=['POST'])
def create_offer():
    data = request.get_json()
    offer = Offer(order_id=data['order_id'],
                  executor_id=data['executor_id'])
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer_instance_to_dict(offer))


@offer_blueprint.route('/offers/<int:uid>', methods=['PUT', 'DELETE'])
def change_offer(uid):
    if request.method == 'PUT':
        data = request.json
        keys = data.keys()
        offer = Offer.query.get(uid)
        if "order_id" in keys:
            offer.order_id = data["order_id"]
        if "executor_id" in keys:
            offer.executor_id = data["executor_id"]

        db.session.add(offer)
        db.session.commit()

        offer = Offer.query.get(uid)

        result = offer_instance_to_dict(offer)
        return jsonify(result), 200

    elif request.method == 'DELETE':
        offer = Offer.query.get(uid)
        if offer is not None:
            db.session.delete(offer)
            db.session.commit()
        return '', 204
