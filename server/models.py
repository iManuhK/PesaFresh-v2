from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_on = db.Column(db.DateTime, default=None, onupdate=db.func.now(), nullable=True)

    # Relationships
    credits = db.relationship('Credit', back_populates='user', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', back_populates='user', cascade='all, delete-orphan')
    production = db.relationship('Production', back_populates='user', cascade='all, delete-orphan')
    industry = db.relationship('Industry', back_populates='user', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-password', '-credits', '-transactions', '-production', '-industry',)

    def __repr__(self):
        return f'<User {self.id} {self.first_name} {self.last_name}>'

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_description = db.Column(db.String, nullable=True)

    # Relationships
    pricing = db.relationship('Pricing', back_populates='product')
    production = db.relationship('Production', back_populates='product')
    industry = db.relationship('Industry', back_populates='product')

    # Serialization rules
    serialize_rules = ('-pricing.product', '-production.product', '-industry.product',)

    def __repr__(self):
        return f'<Product {self.id} {self.product_name}>'


class Credit(db.Model, SerializerMixin):
    __tablename__ = 'credits'
    
    id = db.Column(db.Integer, primary_key=True)
    date_borrowed = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    amount_borrowed = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    production_id = db.Column(db.Integer, db.ForeignKey('production.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='credits')
    production = db.relationship('Production', back_populates='credits')

    # Serialization rules
    serialize_rules = ('-user.credits', '-production.credits',)

    def __repr__(self):
        return f'<Credit {self.id} {self.amount_borrowed}>'


class Production(db.Model, SerializerMixin):
    __tablename__ = 'production'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    production_in_UOM = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    pricing_id = db.Column(db.Integer, db.ForeignKey('pricing.id'), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='production')
    credits = db.relationship('Credit', back_populates='production')
    product = db.relationship('Product', back_populates = 'production')
    industry = db.relationship('Industry', back_populates='production')
    pricing = db.relationship('Pricing', back_populates='production')

    # Serialization rules
    serialize_rules = ('-user.production', '-credits.production', '-product.production', '-industry.production', '-pricing.production')

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
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
   
    # Relationships
    user = db.relationship('User', back_populates='industry')
    product = db.relationship('Product', back_populates='industry')
    production = db.relationship('Production', back_populates='industry')
    pricing = db.relationship('Pricing', back_populates='industry')

    # Serialization rules
    serialize_rules = ('-user.industry', '-product.industry', '-production.industry', '-pricing.industry',)

    def __repr__(self):
        return f'<Industry {self.id} {self.industry_name}>'

class Pricing(db.Model, SerializerMixin):
    __tablename__ = 'pricing'
    
    id = db.Column(db.Integer, primary_key=True)
    Unit_of_Measure = db.Column(db.String, nullable=False)
    Unit_Price = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)

    # Relationships
    product = db.relationship('Product', back_populates='pricing')
    industry = db.relationship('Industry', back_populates='pricing')
    production = db.relationship('Production', back_populates='pricing')

    # Serialization rules
    serialize_rules = ('-product.pricing', '-industry.pricing', '-production.pricing')
    def __repr__(self):
        return f"<Product {self.product_name}>"

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    # transaction_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
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
        return f"<Transaction {self.transaction_type} for User {self.user_id}>"
    