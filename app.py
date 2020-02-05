import time

from anytree.exporter import DotExporter
from flask import Flask, Blueprint, render_template, send_file
from pip._vendor import requests
from anytree import Node, RenderTree
import settings
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import patoolib
import zipfile
from io import BytesIO
import sys
import os
import spotipy
from spotipy import util

app = Flask(__name__)
Bootstrap(app)
nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'Home',
        View('Home', 'index'),
    )

def cerca(id, node, jason):

    results = jason['results']
    trobat = False
    for x in results:
        if x['destination'] == id:
            trobat = True
            fill = Node(x['origin'], parent = node)
            cerca(x['origin'], fill, jason)
    if not trobat:
        print("no trobat")
        return "tope"

def getRequisits(id):
    r = requests.get(url + '/assignatures/requisits' + pack).json()
    assig = Node(id)
    resultat = cerca(id, assig, r)
    print(assig)
    print(RenderTree(assig))
    DotExporter(assig).to_picture("tree.png")


def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    util.prompt_for_user_token(username, scope, client_id='your-spotify-client-id',
                               client_secret='your-spotify-client-secret', redirect_uri='your-app-redirect-url')

    nav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/return-file/')
def return_file():
    patoolib.create_archive("test.rar", ("demo.txt",))
    return send_file("test.rar", attachment_filename='oso.jpg')

@app.route('/file-download/')
def file_downloads():
    return render_template('download.html')

@app.route('/descargaroo')
def descargar():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "covers_{}.zip".format(timestr)
    memory_file = BytesIO()
    file_path = "data"
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                zipf.write(os.path.join(root,file))
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename=fileName,as_attachment=True)


@app.route('/covers')
def covers():
    return 3


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG, port = 80)


if __name__ == "__main__":
    main()

