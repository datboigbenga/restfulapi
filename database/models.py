from .db import db
import datetime
from functools import wraps
from flask import Flask, request, jsonify
import jwt
from settings import create_app

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "gbenga"
app = create_app()

class users(db.Document):
    public_id = db.StringField(primary_key=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)



class templates(db.Document):
    template_name = db.StringField(required=True)
    subject = db.StringField(required=True)
    body = db.StringField(required=True)


def token_required(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        token = None
        if 'x-access-token'in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token  required'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users.objects(public_id = data['public_id'])

        except Exception as Ex:
            print(Ex)
            return jsonify({'message':'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorate
