#!/usr/bin/env python3

# Standard library imports
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
from datetime import timedelta
import random, os

# Add your model imports
from models import db, User, Package
from dotenv import load_dotenv
load_dotenv()

# Instantiate app, set attributes
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

app.config["JWT_SECRET_KEY"] = "dcvbgftyukns6qad"+str(random.randint(1,10000000000))
app.config["SECRET_KEY"] = "s6hjx0an2mzoret"+str(random.randint(1,1000000000))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['ACCESS_TOKEN_EXPIRES'] = False


migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Home(Resource):
    def get(self):
        response_body = {
            'message': 'Welcome to PesaFresh App'
        }
        return make_response(response_body, 200)

api.add_resource(Home, '/')

class Login(Resource):
    def post(self):
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
        
            response_body = {
                'access_token' : f'{access_token}'
                }
            return make_response(response_body, 200)
        
        else:
            response_body = {
                'error' : 'Username or Password incorrect'
                }
            return make_response(response_body, 401)
    
api.add_resource(Login, '/login')

class Current_User(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user:
            current_user_dict = current_user.to_dict()
            return make_response(current_user_dict, 200)
        else:
            response_body = {
                'message': 'User not current user'
            }
            return make_response(response_body, 404)
        
api.add_resource(Current_User, '/current_user')
BLACKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()['jti']
            BLACKLIST.add(jti)
            response_body = {'success': 'Logout successful'}
            return make_response(response_body, 200)
        except Exception as e:
            response_body = {'error': 'Logout failed'}
            return make_response(response_body, 500)

api.add_resource(Logout, '/logout')

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)
    
    def post(self):
        try:
            data = request.json
            new_user = User(
                first_name=data['first_name'],
                last_name=data.get('last_name', ''),
                role=data.get('role', 'user'),
                username=data['username'],
                email=data['email'],
                password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                active=data.get('active', True)
            )

            db.session.add(new_user)
            db.session.commit()

            user_dict = new_user.to_dict()
            response_body = {'success': 'User created successfully', 'user': user_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create user. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)

api.add_resource(Users, '/users')


class UsersByID(Resource):
    def get(self,id):
         user = User.query.filter_by(id=id).first()
         if user:
            user_dict = user.to_dict()
            
            return make_response(user_dict, 200)
         
         else:
            response_body = {
                'message' : 'User does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
        
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()

            response_body = {
                'message': 'User deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'User does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
        
    def patch(self,id):
         user = User.query.filter_by(id=id).first()
         if user:
            try:
                for attr in request.json:
                    setattr(user, attr, request.json.get(attr))

                db.session.add(user)
                db.session.commit()

                user_dict = user.to_dict()
                return make_response(user_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
         else:
            response_body = {
                'message' : 'User you are trying to Edit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
         
api.add_resource(UsersByID, '/users/<int:id>')
class Packages(Resource):
    def get(self):
        packages = [package.to_dict() for package in Package.query.all()]
        return make_response(jsonify(packages), 200)
    def post(self):
        try:
            data = request.json
            new_package = Package(
                package_name = data['package_name'],
                rate = data['rate'],
                amount = data['amount'],
            )

            db.session.add(new_package)
            db.session.commit()

            package_dict = new_package.to_dict()
            response_body = {'success': 'Package created successfully', 'package': package_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create package. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(response_body, 500)
api.add_resource(Packages, '/loans')

class PackagesByID(Resource):
    def get(self,id):
         package = Package.query.filter_by(id=id).first()
         if package:
            package_dict = package.to_dict()
            
            return make_response(package_dict, 200)
         
         else:
            response_body = {
                'message' : 'Package unavailable! Check the id again.'
            }

            return make_response(response_body, 404)
    def delete(self, id):
        package = Package.query.filter_by(id=id).first()
        if package:
            db.session.delete(package)
            db.session.commit()

            response_body = {
                'message': 'Package deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Package Not Available! Check the id again.'
            }

            return make_response(response_body, 404)
        
    def patch(self,id):
         package = Package.query.filter_by(id=id).first()
         if package:
            try:
                for attr in request.json:
                    setattr(package, attr, request.json.get(attr))

                db.session.add(package)
                db.session.commit()

                package_dict = package.to_dict()
                return make_response(package_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
         else:
            response_body = {
                'message' : 'Package you are trying to Edit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
         
api.add_resource(PackagesByID, '/loans/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
