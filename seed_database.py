"""Seed database."""

import os
import json
from random import choice
from datetime import datetime
from model import db, Car,User, Cart
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

with open("data/cars.json") as f:
    car_data = json.loads(f.read())

 

cars_in_db = []
users_in_db = User.query.all()
for car in car_data:
    make_model = car["make_model"]
    description = car["description"]
    image_url = car["image_url"]
    year = datetime.strptime(car["year"], "%Y-%m-%d")

    db_car = Car(make_model=make_model, description=description, year=year, image_url=image_url)
    cars_in_db.append(db_car)

db.session.add_all(cars_in_db)
db.session.commit()


for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = User(email=email, password=password)
    db.session.add(user)
    for _ in range(10):
        user_id = choice(users_in_db)
        random_car_id = choice(cars_in_db)

        cart_item = Cart(user_id=user_id, car_id=random_car_id)
        db.session.add(cart_item)

db.session.commit()