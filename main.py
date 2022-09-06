from flask import Flask
from blueprints.offer import offer_blueprint
from blueprints.order import order_blueprint
from blueprints.user import user_blueprint
from db.models import db
from tools import load_users, load_offers, load_orders


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config['JSON_AS_ASCII'] = False

db.app = app
db.init_app(app)

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(offer_blueprint)
app.register_blueprint(order_blueprint)

# Create DB
db.create_all()
session = db.session()

# Add data to DB
with session.begin():
    session.add_all(load_users())
    session.add_all(load_offers())
    session.add_all(load_orders())


if __name__ == '__main__':
    app.run(debug=True)
