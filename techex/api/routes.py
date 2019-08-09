from . import api_blueprint


@api_blueprint.route('/')
def index():
    return "route from api blueprint"

