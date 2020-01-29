from flask_restplus import Resource
from api.restplus import api

ns = api.namespace('hello', description="API testing")

@ns.route('/')
class HelloCollection(Resource):
    @api.response(204, 'message succesfuly received')
    def get(self):
        """
        Returns hola que tal
        """
        return "Hola que tal"