from flask import request
from . import api_blueprint
from data import db
from data import User
from data import CoffeeShop


@api_blueprint.route('/')
def index():
    return "home page for api"


@api_blueprint.route('/add_user1')
def add_user():
    name = request.args.get('name')
    email = request.args.get('email')
    u = User(username=name, email=email)
    db.session.add(u)
    db.session.commit()
    userstr = str(u)
    return '%s - %s' % (u.username, u.email)


@api_blueprint.route('/users1')
def users():
    user_list = [user.username + ', ' + user.email for user in User.query.all()]
    if user_list:
        return '; '.join(user_list)
    else:
        return 'No users found'


@api_blueprint.route('/coffeeshops1')
def coffee_shops():
    coffee_shop_list = [
        shop.name + ' - ' + shop.zip + ' ' + str(shop.to_geojson())
        for shop in CoffeeShop.query.all()
    ]
    if coffee_shop_list:
        return '; '.join(coffee_shop_list)
    else:
        return 'No coffee shops found'
