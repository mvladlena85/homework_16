from flask import jsonify, request, Blueprint
from db.models import User, db
from tools import user_instance_to_dict


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/users/')
def get_users():
    """
    The view contains request for all users
    :return: json
    """
    users = User.query.all()
    result = []
    for user in users:
        result.append(user_instance_to_dict(user))
    return jsonify(result), 200


@user_blueprint.route('/users/', methods=['POST'])
def create_user():
    """
    The view allows to create new user
    :return: json
    """
    data = request.get_json()
    user = User(first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                age=data.get('age'),
                email=data.get('email'),
                role=data.get('role'),
                phone=data.get('phone'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user_instance_to_dict(user)), 201


@user_blueprint.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def change_user(uid):
    """
    The view contains following DB requests:
    - get user by id
    - change user's data
    - delete user by id
    """
    user = User.query.get(uid)
    if request.method == 'GET':
        if user is not None:
            result = user_instance_to_dict(user)
            return jsonify(result), 200
        else:
            return "No such user", 404

    elif request.method == 'PUT':
        user_data = request.json
        keys = user_data.keys()
        if "first_name" in keys:
            user.first_name = user_data["first_name"]
        if "last_name" in keys:
            user.last_name = user_data["last_name"]
        if "age" in keys:
            user.age = user_data["age"]
        if "email" in keys:
            user.email = user_data["email"]
        if "role" in keys:
            user.role = user_data["role"]
        if "phone" in keys:
            user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()
        user = User.query.get(uid)
        return jsonify(user_instance_to_dict(user)), 200

    elif request.method == 'DELETE':
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        return '', 204
