from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), default="")
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String, default="", nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(30), nullable=True, default="user")
    active = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, default=None, onupdate=db.func.now(), nullable=True)
    national_id = db.Column(db.Integer, unique=True, nullable=False)

    # Relationships
    transactions = db.relationship('Transaction', back_populates='user', cascade='all, delete-orphan')
    production = db.relationship('Production', back_populates='user', cascade='all, delete-orphan')
    credits = db.relationship('Credit', back_populates='user', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='user', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-password', '-credits', '-transactions', '-production','-payments',)

    def __repr__(self):
        return f'<User {self.id} {self.first_name} {self.last_name}>'


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    unit_of_measure = db.Column(db.String, nullable=False)
    product_description = db.Column(db.String, nullable=True)

    # Relationships
    production = db.relationship('Production', back_populates='product')
    industry = db.relationship('Industry', back_populates='product')

    # Serialization rules
    serialize_rules = ('-production', '-industry',)

    def __repr__(self):
        return f'<Product {self.id} {self.product_name}>'

# Credit model
class Credit(db.Model, SerializerMixin):
    __tablename__ = 'credits'
    
    id = db.Column(db.Integer, primary_key=True)
    date_borrowed = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    currency = db.Column(db.String, nullable=False)
    amount_borrowed = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='credits')
    payment = db.relationship('Payment', back_populates='credits')

    # Serialization rules
    serialize_rules = ('-user.credits', '-payment.credits',)

    def __repr__(self):
        return f'<Credit {self.id} {self.amount_borrowed}>'

# Payment model
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    currency = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    credit_id = db.Column(db.Integer, db.ForeignKey('credits.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='payments')
    credits = db.relationship('Credit', back_populates='payment')
    # credits = db.relationship('Credit', back_populates='payment', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-user.payments', '-credits.payment',)

    def __repr__(self):
        return f'<Payment {self.id} {self.amount}>'

class Production(db.Model, SerializerMixin):
    __tablename__ = 'production'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    production_in_UOM = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='production')
    product = db.relationship('Product', back_populates = 'production')
    industry = db.relationship('Industry', back_populates='production')
   
    # serialize_only = ('id', 'date', 'production_in_UOM', 'user_id.user.name', 'industry_id', 'product_id')
    serialize_rules = ('-user.production', '-product.production', '-industry.production', )

    def __repr__(self):
        return f'<Production {self.id} {self.production_in_UOM}>'

class Industry(db.Model, SerializerMixin):
    __tablename__ = 'industries'
    
    id = db.Column(db.Integer, primary_key=True)
    industry_name = db.Column(db.String, nullable=False)
    industry_type = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    collection_point = db.Column(db.String, nullable=False)
    contact_person = db.Column(db.String, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
   
    # Relationships
    product = db.relationship('Product', back_populates='industry')
    production = db.relationship('Production', back_populates='industry')

    #Association proxy relationship
    user = association_proxy('production','user',
                             creator=lambda user_obj: Production(user=user_obj)
                             )

    # Serialization rules
    serialize_rules = ('-product', '-production',)

    def __repr__(self):
        return f'<Industry {self.id} {self.industry_name}>'
    
class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    transaction_type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='transactions')

    # Serialization rules
    serialize_rules = ('-user.transactions',)
    

    def __repr__(self):
        return f'<Transaction {self.id} {self.transaction_type}>'

def calculate_credit_limit(user_id):
    # Get the start of the current month
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    # Query to get the cumulative production for the current month for the user
    total_production = db.session.query(func.sum(Production.production_in_UOM)).filter(
        Production.user_id == user_id,
        Production.date >= start_of_month
    ).scalar()

    # Default to 0 if no production is found
    if total_production is None:
        total_production = 0

    # Example calculation for credit limit based on total production
    # You can adjust this formula based on your specific business rules
    credit_limit = total_production * 10  # Example multiplier

    return credit_limit