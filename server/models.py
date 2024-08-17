from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from sqlalchemy import MetaData, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Naming convention for foreign keys
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
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(30), nullable=True, default="user")
    active = db.Column(db.Boolean, default=True)

    # Relationships
    credits = db.relationship('Credit', back_populates='user')
    produce = db.relationship('Production', back_populates='user')

    # Serialization rules
    serialize_rules = ('-password', '-credits.user', '-produce.user',)

class Package(db.Model, SerializerMixin):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Credit(db.Model, SerializerMixin):
    __tablename__ = 'credits'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    credit_date = db.Column(db.DateTime, default=func.now())
    credit_amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='credits')
    package = db.relationship('Package')

    # Serialization rules
    serialize_rules = ('-user.credits', '-package.credits')

class Production(db.Model, SerializerMixin):
    __tablename__ = 'produce'

    id = db.Column(db.Integer, primary_key=True)
    produce = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=func.now())
    production_in_kilos = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='produce')
    industry = db.relationship('Industry')

    # Serialization rules
    serialize_rules = ('-user.produce', '-industry.produce')

class Industry(db.Model, SerializerMixin):
    __tablename__ = 'industries'

    id = db.Column(db.Integer, primary_key=True)
    industry_type = db.Column(db.String, nullable=False)
    industry_name = db.Column(db.String, nullable=False)
    Address = db.Column(db.String, nullable=False)
    collection_point = db.Column(db.String, nullable=False)
    contact_person = db.Column(db.String, nullable=False)

    # Relationships
    produce = db.relationship('Production', back_populates='industry')

    def __repr__(self):
        return f"<Industry {self.industry_name}>"
