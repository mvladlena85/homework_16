import json
from datetime import datetime, date
from db.models import Order, Offer, User


def load_data(path: str) -> dict:
    """
    Load data from file
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def str_to_date(str_date: str) -> date:
    """
    Convert string to date
    """
    date_object = datetime.strptime(str_date, '%m/%d/%Y').date()
    return date_object


def load_users() -> list[User]:
    """
    Create list of User objects from json
    """
    users = load_data('json_data/users.json')
    db_users = []
    for user in users:
        db_user = User(id=user['id'],
                       first_name=user['first_name'],
                       last_name=user['last_name'],
                       age=user['age'],
                       email=user['email'],
                       role=user['role'],
                       phone=user['phone'])
        db_users.append(db_user)
    return db_users


def load_offers() -> list[Offer]:
    """
    Create list of Offer objects from json
    """
    offers = load_data('json_data/offers.json')
    db_offers = []
    for offer in offers:
        db_offer = Offer(id=offer['id'],
                         order_id=offer['order_id'],
                         executor_id=offer['executor_id'])
        db_offers.append(db_offer)
    return db_offers


def load_orders() -> list[Order]:
    """
    Create list of Order objects from json
    """
    orders = load_data('json_data/orders.json')
    db_orders = []
    for order in orders:
        db_order = Order(id=order['id'],
                         name=order['name'],
                         description=order['description'],
                         start_date=str_to_date(order['start_date']),
                         end_date=str_to_date(order['end_date']),
                         address=order['address'],
                         price=order['price'],
                         customer_id=order['customer_id'],
                         executor_id=order['executor_id']
                         )
        db_orders.append(db_order)
    return db_orders


def user_instance_to_dict(user: User) -> dict:
    """
    Serialize implementation
    """
    return {"id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone}


def offer_instance_to_dict(offer: Offer) -> dict:
    """
        Serialize implementation
    """
    return {"id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id}


def order_instance_to_dict(order: Order) -> dict:
    """
    Serialize implementation
    """
    return {"id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id}
