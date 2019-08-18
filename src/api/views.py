from sqlalchemy import exc
from flask import request, make_response, jsonify, abort
from flask.views import MethodView
from data import db
from data import User
from . import exceptions
from webargs import fields, validate
from webargs.flaskparser import parser


class UserAPI(MethodView):

    # class constant for web field validation
    WEBARGS = {
        "username": fields.Str(required=True),
        "email": fields.Str(required=True, validate=validate.Email())
    }

    # curl -i -X GET http://localhost:5000/api/v1/users/
    # curl -i -X GET http://localhost:5000/api/v1/users/2
    def get(self, user_id):
        if user_id is None:
            # return a list of users
            user_list = [user.to_dict() for user in User.query.all()]
            if user_list:
                return make_response(jsonify(user_list), 200)
            else:
                abort(404, description="No Users found")
        else:
            # return a single user
            user = User.query.get(user_id)
            if user:
                return make_response(jsonify(user.to_dict()), 200)
            else:
                abort(404, description="User not found, id: {}".format(user_id))

    # curl -i -X POST -H 'Content-Type: application/json' -d '{"username": "Naveed10", "email": "naveed10@yahoo.com"}' http://localhost:5000/api/v1/users/
    def post(self):
        args = parser.parse(UserAPI.WEBARGS, request)
        try:
            user = User.create(args["username"], args["email"])
            return make_response(jsonify(user.to_dict()), 200)
        except exc.IntegrityError as e:
            errorInfo = e.orig.args
            error_message = errorInfo[0]
            raise exceptions.APIException(message='Unable to create user, duplicates found: {}'.format(error_message))

    # curl -i -X DELETE http://localhost:5000/api/v1/users/6
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            deleted = user.delete()
            if deleted:
                return make_response(jsonify({user.username: "deleted"}), 200)
            else:
                raise exceptions.APIException(message='Unable to delete user: {}'.format(user.username))
        else:
            abort(404, description="User not found, id: {}".format(user_id))

    # curl -i -X PUT -H 'Content-Type: application/json' -d '{"username": "Naveed11", "email": "naveed11@yahoo.com"}' http://localhost:5000/api/v1/users/3
    def put(self, user_id):
        # update a single user
        user = User.query.get(user_id)
        if user:
            args = parser.parse(UserAPI.WEBARGS, request)
            try:
                updated_user = user.update(args["username"], args["email"])
                if updated_user:
                    return make_response(jsonify(user.to_dict()), 200)
                else:
                    return make_response(jsonify({user.username: "no changes"}), 200)
            except exc.IntegrityError as e:
                errorInfo = e.orig.args
                error_message = errorInfo[0]
                raise exceptions.APIException(message='Unable to update user, duplicates found: {}'.format(error_message))
        else:
            abort(404, description="User not found, id: {}".format(user_id))
