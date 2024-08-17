#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, User, Package, Credit, Production, Industry
import random

fake = Faker()

def delete_existing_data():
    try:
        # Delete data in the correct order to handle foreign key constraints
        Credit.query.delete()
        Production.query.delete()
        Package.query.delete()
        Industry.query.delete()
        User.query.delete()
        db.session.commit()
        print("Existing data deleted.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while deleting existing data: {e}")

def seed_users():
    try:
        users = []
        for _ in range(3):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=random.choice(['user', 'admin']),
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password=fake.password(),
                active=True
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        print("Users seeded.")
        return users
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding users: {e}")
        return []

def seed_packages():
    try:
        package_names = ['Platinum', 'Gold', 'Silver', 'Bronze', 'Mwananchi']
        packages = []
        for name in package_names:
            package = Package(
                package_name=name,
                rate=round(fake.random_number(digits=2), 2),
                amount=fake.random_number(digits=5)
            )
            packages.append(package)
        db.session.add_all(packages)
        db.session.commit()
        print("Packages seeded.")
        return packages
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding packages: {e}")
        return []

def seed_industries():
    try:
        industries = []
        for _ in range(5):
            industry = Industry(
                industry_type=fake.word(),
                industry_name=fake.company(),
                Address=fake.address(),
                collection_point=fake.city(),
                contact_person=fake.name()
            )
            industries.append(industry)
        db.session.add_all(industries)
        db.session.commit()
        print("Industries seeded.")
        return industries
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding industries: {e}")
        return []

def seed_credits(users, packages):
    try:
        credits = []
        for _ in range(20):
            credit = Credit(
                package_id=random.choice(packages).id,
                credit_amount=round(fake.random_number(digits=3), 2),
                user_id=random.choice(users).id
            )
            credits.append(credit)
        db.session.add_all(credits)
        db.session.commit()
        print("Credits seeded.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding credits: {e}")

def seed_productions(users, industries):
    try:
        productions = []
        for _ in range(20):
            production = Production(
                produce=fake.word(),
                production_in_kilos=fake.random_number(digits=2),
                sale_price=fake.random_number(digits=2),
                user_id=random.choice(users).id,
                industry_id=random.choice(industries).id
            )
            productions.append(production)
        db.session.add_all(productions)
        db.session.commit()
        print("Productions seeded.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while seeding productions: {e}")

def seed_database():
    with app.app_context():
        delete_existing_data()
        
        users = seed_users()
        packages = seed_packages()
        industries = seed_industries()
        
        if users and packages:
            seed_credits(users, packages)
        
        if users and industries:
            seed_productions(users, industries)
        
        print("Seeding completed!")

if __name__ == "__main__":
    seed_database()
