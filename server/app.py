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
                transaction_type=data['transaction_type'],
                currency=data['currency'],
                description=data['description'],
                amount=data['amount']
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
                production_in_UOM=data['production_in_UOM'],
                pricing_id=data['pricing_id'],
                industry_id=data['industry_id'],
                user_id=data['user_id']
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

class MyTransactions(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        transactions = [transaction.to_dict() for transaction in Transaction.query.filter_by(user_id=current_user).all()]

        if transactions:
            logging.info(f"User {current_user} accessed all their transactions.")
            return make_response(jsonify(transactions), 200)
        else:
            logging.warning(f"User {current_user} tried to access transactions but none were found.")
            return make_response(jsonify({"message": "Transaction not found"}), 404)

api.add_resource(MyTransactions, '/my-transactions')

class MyProductions(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        productions = [production.to_dict() for production in Production.query.filter_by(user_id=current_user).all()]
        
        if productions:
            logging.info(f"User {current_user} accessed all their productions.")
            return make_response(jsonify(productions), 200)
        else:
            logging.warning(f"User {current_user} tried to access productions but none were found.")
            return make_response(jsonify({"message": "Productions not found"}), 404)

api.add_resource(MyProductions, '/my-productions')

class Credits(Resource):
    def get(self):
        credits = [credit.to_dict() for credit in Credit.query.all()]
        return make_response(jsonify(credits), 200)
    
    def post(self):
        try:
            data = request.json
            new_credit = Credit(
                user_id=data['user_id'],
                credit_limit=data['credit_limit'],
                credit_balance=data['credit_balance'],
                currency=data['currency']
            )

            db.session.add(new_credit)
            db.session.commit()

            credit_dict = new_credit.to_dict()
            response_body = {'success': 'Credit created successfully', 'credit': credit_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create credit. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)
        
api.add_resource(Credits, '/credits')

class CreditsByID(Resource):
    def get(self, id):
        credit = Credit.query.filter_by(id=id).first()
        if credit:
            credit_dict = credit.to_dict()
            
            return make_response(credit_dict, 200)
         
        else:
            response_body = {
                'message' : 'Credit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
    
    def patch(self, id):
        credit = Credit.query.filter_by(id=id).first()
        if credit:
            try:
                for attr in request.json:
                    setattr(credit, attr, request.json.get(attr))

                db.session.add(credit)
                db.session.commit()

                credit_dict = credit.to_dict()
                return make_response(credit_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
                return make_response(jsonify(response_body), 400)
            except Exception as e:
                response_body = {'error': str(e)}
                return make_response(jsonify(response_body), 400)
    
    def delete(self, id):
        credit = Credit.query.filter_by(id=id).first()
        if credit:
            db.session.delete(credit)
            db.session.commit()

            response_body = {
               'message': 'Credit deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Credit does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(CreditsByID, '/credits/<int:id>')


class Pricing(Resource):
    def get(self):
        pricing = [pricing.to_dict() for pricing in Pricing.query.all()]
        return make_response(jsonify(pricing), 200)
    
    def post(self):
        try:
            data = request.json
            new_pricing = Pricing(
                product_id=data['product_id'],
                industry_id=data['industry_id'],
                price=data['price'],
                currency=data['currency']
            )

            db.session.add(new_pricing)
            db.session.commit()

            pricing_dict = new_pricing.to_dict()
            response_body = {'success': 'Pricing created successfully', 'pricing': pricing_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create pricing. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)

api.add_resource(Pricing, '/pricing')

class PricingByID(Resource):
    def get(self, id):
        pricing = Pricing.query.filter_by(id=id).first()
        if pricing:
            pricing_dict = pricing.to_dict()
            
            return make_response(pricing_dict, 200)
         
        else:
            response_body = {
                'message' : 'Pricing does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
    
    def patch(self, id):
        pricing = Pricing.query.filter_by(id=id).first()
        if pricing:
            try:
                for attr in request.json:
                    setattr(pricing, attr, request.json.get(attr))

                db.session.add(pricing)
                db.session.commit()

                pricing_dict = pricing.to_dict()
                return make_response(pricing_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
                return make_response(jsonify(response_body), 400)
            except Exception as e:
                response_body = {'error': str(e)}
                return make_response(jsonify(response_body), 400)
    
    def delete(self, id):
        pricing = Pricing.query.filter_by(id=id).first()
        if pricing:
            db.session.delete(pricing)
            db.session.commit()

            response_body = {
               'message': 'Pricing deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Pricing does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(PricingByID, '/pricing/<int:id>')

class Industry(Resource):
    def get(self):
        industries = [industry.to_dict() for industry in Industry.query.all()]
        return make_response(jsonify(industries), 200)
    
    def post(self):
        try:
            data = request.json
            new_industry = Industry(
                name=data['name']
            )

            db.session.add(new_industry)
            db.session.commit()

            industry_dict = new_industry.to_dict()
            response_body = {'success': 'Industry created successfully', 'industry': industry_dict}
            return make_response(jsonify(response_body), 201)
        
        except KeyError:
            response_body = {'error': 'Could not create industry. Required fields missing.'}
            return make_response(jsonify(response_body), 400)
        
        except Exception as e:
            response_body = {'error': str(e)}
            return make_response(jsonify(response_body), 400)

api.add_resource(Industry, '/industries')

class IndustryByID(Resource):
    def get(self, id):
        industry = Industry.query.filter_by(id=id).first()
        if industry:
            industry_dict = industry.to_dict()
            
            return make_response(industry_dict, 200)
         
        else:
            response_body = {
                'message' : 'Industry does not exist! Check the id again.'
            }

            return make_response(response_body, 404)
    
    def patch(self, id):
        industry = Industry.query.filter_by(id=id).first()
        if industry:
            try:
                for attr in request.json:
                    setattr(industry, attr, request.json.get(attr))

                db.session.add(industry)
                db.session.commit()

                industry_dict = industry.to_dict()
                return make_response(industry_dict, 200)
            
            except ValueError:
                response_body = {
                    'error': 'error occured'
                }
                return make_response(jsonify(response_body), 400)
            except Exception as e:
                response_body = {'error': str(e)}
                return make_response(jsonify(response_body), 400)
    
    def delete(self, id):
        industry = Industry.query.filter_by(id=id).first()
        if industry:
            db.session.delete(industry)
            db.session.commit()

            response_body = {
               'message': 'Industry deleted Successfully'
            }
            return make_response(response_body, 200)
        else:
            response_body = {
                'message' : 'Industry does not exist! Check the id again.'
            }

            return make_response(response_body, 404)

api.add_resource(IndustryByID, '/industries/<int:id>')

@app.route('/calculate-credit-limit', methods=['GET'])
def add_production(self,user_id, production_data):
    # Create new production record
    new_production = Production(
        user_id=user_id,
        **production_data
    )
    db.session.add(new_production)
    db.session.commit()

    # Recalculate and update credit limit
    credit_limit = self.calculate_credit_limit(user_id)
    user = User.query.get(user_id)
    user.credit_limit = credit_limit
    db.session.commit()

    return new_production

                     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
