# database name is capstone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
    @classmethod
    def create_user(cls, email, password):
        """Create and return a new user."""
        user = cls(email=email, password=password)
        return user

    @classmethod
    def get_users(cls):
        """Return all users."""
        return cls.query.all()

    @classmethod
    def get_user_by_id(cls, user_id):
        """Return a user by primary key."""
        return cls.query.get(user_id)

    @classmethod
    def get_user_by_email(cls, email):
        """Return a user by email."""
        return cls.query.filter(cls.email == email).first()


class Car(db.Model):
    """A car."""

    __tablename__ = "cars"

    car_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    make_model = db.Column(db.String)
    description = db.Column(db.Text)
    year = db.Column(db.DateTime)
    image_url = db.Column(db.String)

    def __repr__(self):
        return f"<Car car_id={self.car_id} make_model={self.make_model}>"
    
    @classmethod
    def create_car(cls, make_model, description, year, image_url):
        """Create and return a new car."""
        car = cls(
            make_model=make_model,
            description=description,
            year=year,
            image_url=image_url
        )
        return car

    @classmethod
    def get_cars(cls):
        """Return all cars."""
        return cls.query.all()

    @classmethod
    def get_car_by_id(cls, car_id):
        """Return a car by primary key."""
        return cls.query.get(car_id)

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('cart_items', cascade='all, delete-orphan'))
    car = db.relationship('Car', backref=db.backref('cart_items', cascade='all, delete-orphan'))

    @classmethod
    def create_item(cls, user_id, car_id):
        cart_item = cls(user_id=user_id, car_id=car_id)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item


def connect_to_db(flask_app, db_uri="postgresql://postgres:123@localhost:5432/capstone", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app, echo=False)