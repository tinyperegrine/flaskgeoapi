from flask import request
from . import api_blueprint
from data import db
from data import User


@api_blueprint.route('/')
def index():
    return "route from api blueprint"


@api_blueprint.route('/add_user')
def add_user():
    name = request.args.get('name')
    email = request.args.get('email')
    u = User(username=name, email=email)
    db.session.add(u)
    db.session.commit()
    userstr = str(u)
    return '%s - %s' % (u.username, u.email)


@api_blueprint.route('/users')
def users():
    user_list = [user.username + ', ' + user.email for user in User.query.all()]
    if user_list:
        return '; '.join(user_list)
    else:
        return 'No users found'
