"""
The api Blueprint provides all the api routes for this application.
This Blueprint allows for the api to ...
"""
from flask import Blueprint
api_blueprint = Blueprint('api', __name__, template_folder='templates')
 
from . import routes

