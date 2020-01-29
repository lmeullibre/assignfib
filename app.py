from flask import Flask, Blueprint, render_template
from pip._vendor import requests

from api.restplus import api
import settings
from api.endpoints.hello import ns as hello_namespace

app = Flask(__name__)


def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(hello_namespace)
    flask_app.register_blueprint(blueprint)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/course/', methods= ['GET'])
def hello():
    print("holaaa")
    r = requests.get('https://api.fib.upc.edu/v2/competencies/?client_id=4Prn0YdaE8beYA9PpdeBJS46vmBVshrjbpn4LAbH&format=json')
    print(r.json())
    return r.json()





def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG, port = 80)


if __name__ == "__main__":
    main()

