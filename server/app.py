#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify,send_from_directory
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Pricing, Product, Production, Credit, Transaction, Industry
import os, uuid, logging, random
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'PesaFresh.db')}")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your_secret_key")
app.config["SECRET_KEY"] = "s6hjx0an2mzoret"+str(random.randint(1,1000000000))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['ACCESS_TOKEN_EXPIRES'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Setup logging
logging.basicConfig(filename=os.path.join(BASE_DIR, 'logs/PesaFresh.log'),
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error: {str(e)}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred"}), 500

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

class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(jsonify(products), 200)
    
    def post(self):
        try:
            data = request.json
            new_product = Product(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                quantity=data['quantity'],
                image=data.get('image', '')
            )

            db.session.add(new_product)
            db.session.commit()

            product_dict = new_product.to_dict()
            response_body = {'success': 'Product created successfully', 'product': product_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create product. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)

api.add_resource(Products, '/products')

class ProductsByID(Resource):
    def get(self, id):
         product = Product.query.filter_by(id=id).first()
         if product:
            product_dict = product.to_dict()
            
            return make_response(product_dict, 200)
         
         else:
            response_body = {
                'message' : 'Product does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
        
    def patch(self, id):
         product = Product.query.filter_by(id=id).first()
         if product:
            try:
                for attr in request.json:
                    setattr(product, attr, request.json.get(attr))

                db.session.add(product)
                db.session.commit()

                product_dict = product.to_dict()
                return make_response(product_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
         else:
            response_body = {
                'message' : 'Product you are trying to Edit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
         
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        if product:
            db.session.delete(product)
            db.session.commit()

            response_body = {
                'message': 'Product deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Product does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(ProductsByID, '/products/<int:id>')

class Transactions(Resource):
    def get(self):
        transactions = [transaction.to_dict() for transaction in Transaction.query.all()]
        return make_response(jsonify(transactions), 200)
    
    def post(self):
        try:
            data = request.json
            new_transaction = Transaction(
                user_id=data['user_id'],
                product_id=data['product_id'],
                quantity=data['quantity'],
                price=data['price'],
                status=data['status']
            )

            db.session.add(new_transaction)
            db.session.commit()

            transaction_dict = new_transaction.to_dict()
            response_body = {'success': 'Transaction created successfully', 'transaction': transaction_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create transaction. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)
        

api.add_resource(Transactions, '/transactions')

class TransactionsByID(Resource):
    def get(self, id):
         transaction = Transaction.query.filter_by(id=id).first()
         if transaction:
            transaction_dict = transaction.to_dict()
            
            return make_response(transaction_dict, 200)
         
         else:
            response_body = {
                'message' : 'Transaction does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
         
    def patch(self, id):
         transaction = Transaction.query.filter_by(id=id).first()
         if transaction:
            try:
                for attr in request.json:
                    setattr(transaction, attr, request.json.get(attr))

                db.session.add(transaction)
                db.session.commit()

                transaction_dict = transaction.to_dict()
                return make_response(transaction_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
         else:
            response_body = {
                'message' : 'Transaction you are trying to Edit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
         
    def delete(self, id):
        transaction = Transaction.query.filter_by(id=id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()

            response_body = {
                'message': 'Transaction deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Transaction does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(TransactionsByID, '/transactions/<int:id>')

class Productions(Resource):
    def get(self):
        productions = [production.to_dict() for production in Production.query.all()]
        return make_response(jsonify(productions), 200)
    
    def post(self):
        try:
            data = request.json
            new_production = Production(
                product_id=data['product_id'],
                quantity=data['quantity'],
                date=data['date']
            )

            db.session.add(new_production)
            db.session.commit()

            production_dict = new_production.to_dict()
            response_body = {'success': 'Production created successfully', 'production': production_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create production. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)
        
api.add_resource(Productions, '/productions')

class ProductionsByID(Resource):
    def get(self, id):
         production = Production.query.filter_by(id=id).first()
         if production:
            production_dict = production.to_dict()
            
            return make_response(production_dict, 200)
         
         else:
            response_body = {
                'message' : 'Production does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
    
    def patch(self, id):
        production = Production.query.filter_by(id=id).first()
        if production:
            try:
                for attr in request.json:
                    setattr(production, attr, request.json.get(attr))

                db.session.add(production)
                db.session.commit()

                production_dict = production.to_dict()
                return make_response(production_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
                return make_response(jsonify(response_body), 400)
            except Exception as e:
                response_body = {'error': str(e)}
                return make_response(jsonify(response_body), 400)
         
    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if production:
            db.session.delete(production)
            db.session.commit()

            response_body = {
                'message': 'Production deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Production does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(ProductionsByID, '/productions/<int:id>')

class myTransactions(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user != id:
            logging.warning(f"User {current_user} attempted to access transactions {id} without permission.")
            return make_response(jsonify({"message": "Forbidden"}), 403)
        
        transactions = [transaction.to_dict() for transaction in Transaction.query.filter_by(user_id=id).all()]
        if transactions:
            logging.info(f"User {current_user} accessed all their transactions.")
            return make_response(jsonify(transactions), 200)
        else:
            logging.warning(f"User {current_user} tried to access transactions {id} that do not exist.")
            return make_response(jsonify({"message": "Transaction not found"}), 404)

api.add_resource(myTransactions, '/my-transactions/user/<int:id>')

class myProductions(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user!= id:
            logging.warning(f"User {current_user} attempted to access productions {id} without permission.")
            return make_response(jsonify({"message": "Forbidden"}), 403)
        
        productions = [production.to_dict() for production in Production.query.filter_by(product_id=id).all()]
        if productions:
            logging.info(f"User {current_user} accessed all their productions.")
            return make_response(jsonify(productions), 200)
        else:
            logging.warning(f"User {current_user} tried to access productions {id} that do not exist.")
            return make_response(jsonify({"message": "Product not found"}), 404)

api.add_resource(myProductions, '/my-productions/user/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
