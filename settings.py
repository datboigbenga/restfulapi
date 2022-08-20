import os
from dotenv import load_dotenv 
from flask import Flask, request, jsonify, Response, make_response
load_dotenv()


DB_URI = os.getenv("DB_URI")
SECRET_KEY = os.getenv("SECRET_KEY")


def create_app():
    app =  Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MONGODB_SETTINGS'] = {
        'host' : DB_URI
        }
    
    return app