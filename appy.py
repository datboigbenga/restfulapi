from encodings import utf_8
from enum import unique
import json
from turtle import update
import tkinter as TK
import _tkinter
import uuid
import jwt
import pymongo
from flask import Flask, request, jsonify, Response, make_response
from database.db import initialize_db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
from bson.objectid import ObjectId
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = "gbenga"

# database_name = "test"
DB_URI = "mongodb+srv://gbenga:gbenga@cluster0.bdkpoct.mongodb.net/?retryWrites=true&w=majority"
app.config['MONGODB_SETTINGS'] = {
    'host' : DB_URI
    }

initialize_db(app)



    # def to_json(self){

    # }



#token setup
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
            current_user = db.users.find({'public_id': data['public_id']})

        except Exception as Ex:
            print(Ex)
            return jsonify({'message':'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorate


# A welcome message to test our server
@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Test server!</h1>"


#  register a user    
@app.route('/register', methods=['POST'])
def register_user():
    try:
        user = request.get_json()
        hash_pass = generate_password_hash(user["password"], method="sha256")
        pub_id = str(uuid.uuid1())
        user_input= {
                "public_id":pub_id,
                "first_name" : user["first_name"],
                "last_name" : user["last_name"],
                "email" : user["email"],
                "password" : hash_pass
              }

        if(users.objects(email = user_input["email"])):
            return jsonify({"message":"email aleady in use"}), 401
        
        dbResponse = users(**user_input).save()
        return make_response(jsonify({"message":"user {} created".format(user_input["first_name"])}), 200)
        
  
    except Exception as Ex:
        print("error")
        print(Ex)
        return make_response(jsonify({"message":"unable to process"}), 500)



# login to user
@app.route('/login', methods=['POST'])
def login_user():
    try:
        auth = request.get_json()
        if not auth or not auth["email"] or not auth["password"]:
            return make_response(jsonify({'message': 'username and password required'}), 401)
 
        user = users.objects(email = auth["email"])
        print(user)
        if not user:
            return make_response(jsonify({'message': 'user does not exist'}), 401)

        for user_det in user:
                # print(pl)
            print(user_det)
            if not user_det:
                return Response("could not verify", 401, {'www-authenticate': 'Basic-realm="login required"'})
            # if check_password_hash(user_det['password'], auth.password):
            if check_password_hash(user_det['password'], auth["password"]):

                token = jwt.encode({'public_id':user_det['public_id'],  'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                # token_d = token.decode("UTF-8")
                return jsonify({'token': token})

            return Response("could not verify", 401, {'www-authenticate': 'Basic-realm="login required"'})

    except Exception as ex:
        print(ex)
        print("unable to login")
        return Response("could not verify", 401, {'www-authenticate': 'Basic-realm="login required"'})

    # return ""


#create template
@app.route('/template', methods=['POST'])
@token_required
def temp(current_user):
    try:
        template = request.get_json()
        dbResponse = db.templates.insert_one(template)
        return jsonify({'message':'template added'})

    except Exception as Ex:
        print(Ex)
        return jsonify({'message':'template not added'})


#get templates
@app.route('/template', methods=['GET'])
@token_required
def temp_get_all(current_user):
    # print("Gbemga")
    try:
        # template = request.get_json()
        dbResponse = db.templates.find()
        temps = list(dbResponse)
        for temp in temps:
            temp['_id'] = str(temp['_id'])
            print(temp)
        return json.dumps({'templates':temps})

    except Exception as Ex:
        print(Ex)
        return jsonify({'message':'templates not retrieved'})
    # return ""

#get a template
@app.route('/template/<template_id>', methods=['GET'])
@token_required
def temp_get_one_temp(current_user, template_id):
# def temp_get_one_temp(template_id):

    try:
        query = {"_id":ObjectId(template_id)}
        dbResponse = db.templates.find(query)
        temps = list(dbResponse)
        print(temps)
        for temp in temps:
            temp['_id'] = str(temp['_id'])
        # return json.dumps({'template':temps})
        return jsonify({'template':temps})
            
    except Exception as Ex:
        print(Ex)
        return jsonify({'message':'template not retrieved'})
   

#update a template
@app.route('/template/<template_id>', methods=['PUT'])
@token_required
def temp_update(current_user, template_id):
    try:
        updater = request.get_json()
        query = {"_id":ObjectId(template_id)}
        # Update_query = {"$set": {"template_name":request.form['template_name'], "subject":request.form['subject'], "body":request.form['body']}}
        # print(updater)
        Update_query = {"$set": updater}
        dbResponse = db.templates.update_one(query, Update_query)
        # dbResponse = db.templates.find_one_and_update(query, Update_query)


        if dbResponse.modified_count == 1:
            return jsonify({"message":"template updated"})
        
        return jsonify({"message":"nothing to update"})
    except Exception as Ex:
        print(Ex)
        print("unable to update")
        return jsonify({"message":"unable to update"})


    # return template_id


#delete a template
@app.route('/template/<template_id>', methods=['DELETE'])
@token_required
def temp_del(current_user, template_id):
    try:
        query = {"_id":ObjectId(template_id)}
        dbResponse = db.templates.delete_one(query)
        if dbResponse.deleted_count == 1:
            return jsonify({"message":"template deleted", "id":template_id})
        
        return jsonify({"message":"nothing to delete"})

    except Exception as Ex:
        print(Ex)
        print("unable to delete")
        return jsonify({"message":"unable to delete"})

    # return ""

if __name__ == '__main__':
    app.run(debug= True)
