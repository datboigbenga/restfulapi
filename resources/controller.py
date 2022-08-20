from flask import Flask, request, jsonify, Response, make_response
from database.models import users, templates, token_required
from flask_restful import Resource
import json
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from bson.objectid import ObjectId
from settings import create_app

# def initialize_secretkey(app):
#     init_app(app)
# app = Flask(__name__)
# app.config['SECRET_KEY'] = "gbenga"

app = create_app()


class index(Resource):
    def get(self):
        return "<h1>Welcome to API Test server!</h1>"

class userRegister(Resource):
    def post(self):
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



class userLogin(Resource):
    def post(self):
        try:
            auth = request.get_json()
            if not auth or not auth["email"] or not auth["password"]:
                return make_response(jsonify({'message': 'username and password required'}), 401)
    
            user = users.objects(email = auth["email"])
            print(user)
            if not user:
                return make_response(jsonify({'message': 'user does not exist'}), 401)

            for user_det in user:
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


class add_get_Temp(Resource):
    @token_required
    def post(self, current_user):
        try:
            template = request.get_json()
            dbResponse = templates(**template).save()
            return make_response(jsonify({'message':'template added'}), 201)

        except Exception as Ex:
            print(Ex)
            return make_response(jsonify({'message':'template not added'}), 401)

    @token_required
    def get(self, current_user):
        try:
            dbResponse = templates.objects()
            return make_response(jsonify({'templates': dbResponse}), 201)
   
        except Exception as Ex:
            print(Ex)
            return make_response(jsonify({'message':'templates not retrieved'})),401


class get_upd_del_Temp(Resource):
    @token_required
    def get(self, current_user, template_id):
        try:
            dbResponse = templates.objects.get(id=template_id)
            return make_response(jsonify({'template':dbResponse}), 201)
            
        except Exception as Ex:
            print(Ex)
            return make_response(jsonify({'message':'template not retrieved, does not exist'}), 401)

    @token_required
    def put(self, current_user, template_id):
        try:
            updater = request.get_json()
            dbResponse = templates.objects(id=template_id).update(**updater)
            return make_response(jsonify({"message":"template id: {} updated".format(template_id)}), 201)

        except Exception as Ex:
            print(Ex)
            print("unable to update")
            return make_response(jsonify({"message":"unable to update"}), 401)


    @token_required
    def delete(self, current_user, template_id):
        try:
            dbResponse = templates.objects(id=template_id).delete()
            return make_response(jsonify({"message":"template id: {} deleted".format(template_id)}), 201)

        except Exception as Ex:
            print(Ex)
            print("unable to delete")
            return make_response(jsonify({"message":"unable to delete"}), 401)
