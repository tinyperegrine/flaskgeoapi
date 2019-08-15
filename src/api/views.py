from flask import make_response, jsonify, abort
from flask.views import MethodView
from data import db
from data import User
from . import exceptions


class UserAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            # return a list of users
            user_list = [{
                user.username: user.email
            } for user in User.query.all()]
            if user_list:
                return make_response(jsonify(user_list), 200)
            else:
                abort(404, description="No Users found")
        else:
            # expose a single user
            user = User.query.get(user_id)
            if user:
                return make_response(jsonify({user.username: user.email}), 200)
            else:
                abort(404, description="User not found, id: {}".format(user_id))

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
