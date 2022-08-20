from distutils.log import error
import os
from dotenv import load_dotenv 
from flask import Flask, request, jsonify, Response, make_response
from database.db import initialize_db
from resources.routes import initialize_routes
from flask_restful import Api
from settings import create_app

load_dotenv()
DB_URI = os.getenv("DB_URI")
SECRET_KEY = os.getenv("SECRET_KEY")



app = create_app()
# app = Flask(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['MONGODB_SETTINGS'] = {
#     'host' : DB_URI
#     }
api = Api(app)



initialize_db(app)
initialize_routes(api)


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"message": "forbidden"}),403

@app.errorhandler(404)
def forbidden(error):
    return jsonify({"message": "endpoint not found"}),404

# app.run()
if __name__ == '__main__':
    app.run(debug= True)