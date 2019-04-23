from flask import Blueprint
from flask_restful import Api
from resources.hello import Hello
from resources.category import Category

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/hello')
api.add_resource(Category, '/properties')
