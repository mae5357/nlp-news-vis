# start flask by running "flask --app app --debug run" from repo root

import os
import pprint

from flask import Flask, render_template, jsonify, send_from_directory

pp = pprint.PrettyPrinter()

# boilerplate from the flask tuts
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #### ROUTES ####
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/viz')
    def samples():
        # Update filename to pull file from /static/data/ for display (must be list of json/objects)
        return send_from_directory(f'{app.static_folder}/data/', "newsdataio.nltk.doc2vec.pca.json")

    return app
