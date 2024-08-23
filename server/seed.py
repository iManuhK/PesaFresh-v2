#!/usr/bin/env python3

from faker import Faker
from datetime import datetime
from models import db, User, Product, Credit, Production, Industry, Transaction, Payment
from app import app

faker = Faker()

def delete_existing_data():
    try:
        Transaction.query.delete()
        Payment.query.delete()
        Credit.query.delete()
        Production.query.delete()
        Industry.query.delete()
        Product.query.delete()
        User.query.delete()
        db.session.commit()
        print("Existing data deleted.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while deleting existing data: {e}")

def seed_users(n):
    users = []
    for _ in range(n):
        user = User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            national_id=faker.unique.random_number(digits=8),
            username=faker.unique.user_name(),
            email=faker.unique.email(),
            phone=faker.phone_number(),
            password=faker.password(),
            role='user',
            active=True,
            created_on=faker.date_time_this_decade(),
            updated_on=faker.date_time_this_decade()
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users

def seed_products(n):
    products = []
    for _ in range(n):
        product = Product(
            product_name=faker.word(),
            product_description=faker.text(max_nb_chars=200),
            unit_of_measure=faker.random_element(elements=('kg', 'ltr', 'piece')),

        )
        products.append(product)
        db.session.add(product)
    db.session.commit()
    return products

def seed_industries(n, users, products):
    industries = []
    for _ in range(n):
        industry = Industry(
            industry_name=faker.company(),
            industry_type=faker.bs(),
            address=faker.address(),
            collection_point=faker.address(),
            contact_person=faker.name(),
            unit_price=faker.random_number(digits=2),
            product_id=faker.random_element(products).id,
        )
        industries.append(industry)
        db.session.add(industry)
    db.session.commit()
    return industries

def seed_production(n, users, products, industries):
    productions = []
    for _ in range(n):
        production = Production(
            date=faker.date_time_this_year(),
            production_in_UOM=faker.random_number(digits=3),
            user_id=faker.random_element(users).id,
            product_id=faker.random_element(products).id,
            industry_id=faker.random_element(industries).id,
        )
        productions.append(production)
        db.session.add(production)
    db.session.commit()
    return productions

def seed_credits(n, users):
    credits = []
    for _ in range(n):
        credit = Credit(
            date_borrowed=faker.date_time_this_year(),
            currency=faker.currency_code(),
            amount_borrowed=faker.random_number(digits=5),
            user_id=faker.random_element(users).id,
            payment_status=faker.random_element(elements=('pending', 'processing','disbursed', 'cancelled'))
        )
        credits.append(credit)
        db.session.add(credit)
    db.session.commit()
    return credits

def seed_transactions(n, users):
    transactions = []
    for _ in range(n):
        transaction = Transaction(
            transaction_date=faker.date_time_this_year(),
            transaction_type=faker.random_element(elements=('debit', 'credit')),
            description = faker.text(max_nb_chars=70),
            currency=faker.currency_code(),
            amount=faker.random_number(digits=3),
            user_id=faker.random_element(users).id
        )
        transactions.append(transaction)
        db.session.add(transaction)
    db.session.commit()
    return transactions

def seed_payments(n, users, credits):
    payments = []
    for _ in range(n):
        payment = Payment(
            payment_date=faker.date_time_this_year(),
            description=faker.text(max_nb_chars=70),
            currency=faker.currency_code(),
            amount=faker.random_number(digits=3),
            user_id=faker.random_element(users).id,
            credit_id=faker.random_element(credits).id if credits else None
        )
        payments.append(payment)
        db.session.add(payment)

    db.session.commit()
    return payments


def seed_database():
    delete_existing_data()
    users = seed_users(10)
    products = seed_products(10)
    industries = seed_industries(10, users, products)
    productions = seed_production(10, users, products, industries)
    credits = seed_credits(10, users)
    seed_payments(10, users, credits)
    seed_transactions(10, users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()
        print("Database seeded successfully")
