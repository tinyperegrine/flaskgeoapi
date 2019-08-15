"""
The api Blueprint provides all the api routes for this application.
This Blueprint allows for the api to ...
"""
from flask import Blueprint, make_response, jsonify
api_blueprint = Blueprint('api', __name__, template_folder='templates')

from . import exceptions
from . import routes
from . import views

user_view = views.UserAPI.as_view('user_api')
api_blueprint.add_url_rule('/users/',
                           defaults={'user_id': None},
                           view_func=user_view,
                           methods=[
                               'GET',
                           ])
api_blueprint.add_url_rule('/users/', view_func=user_view, methods=[
    'POST',
])
api_blueprint.add_url_rule('/users/<int:user_id>',
                           view_func=user_view,
                           methods=['GET', 'PUT', 'DELETE'])


@api_blueprint.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error=str(e)), 404)


@api_blueprint.errorhandler(403)
def resource_forbidden(e):
    return make_response(jsonify(error=str(e)), 403)


@api_blueprint.errorhandler(410)
def resource_deleted(e):
    return make_response(jsonify(error=str(e)), 410)


@api_blueprint.errorhandler(500)
def internal_error(e):
    return make_response(jsonify(error=str(e)), 500)


@api_blueprint.errorhandler(exceptions.APIException)
def handle_api_exception(error):
    return make_response(jsonify(error.to_dict()), error.status_code)
