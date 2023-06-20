from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from model import User, Car, Cart

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("home.html")


@app.route("/cars")
def all_cars():
    """View all cars."""
    cars = Car.get_cars()
    return render_template("cars_page.html", cars=cars)


@app.route("/cars/<car_id>")
def show_car(car_id):
    """Show details on a car."""
    car = Car.get_car_by_id(car_id)
    return render_template("car_details.html", car=car)


@app.route("/users")
def all_users():
    """View all users."""
    users = User.get_users()
    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = User.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = User.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/add_to_cart/<car_id>", methods=["POST"])
def add_to_cart(car_id):
    """Add a car to the cart."""

    logged_in_email = session.get("user_email")
    user = None

    if logged_in_email is None:
        flash("You must log in to add a car to the cart.")
        return redirect("/")
    else:
        user = User.query.filter_by(email=logged_in_email).first()
        car = Car.query.get(car_id)

        if car is None:
            flash("Car not found.")
        elif user is None:
            flash("User not found. Please log in.")
        else:
            cart_item = Cart(user_id=user.user_id, car_id=car_id)
            db.session.add(cart_item)
            db.session.commit()

            flash(f"{car.make_model} added to the cart.")

    if user is not None:
        cart_items = Cart.query.filter_by(user_id=user.user_id).all()
        cars = [cart_item.car for cart_item in cart_items]
    else:
        cars = []

    return render_template("cart.html", cars=cars)

@app.route("/logout", methods=["POST"])
def logout():
    """Logout the user."""

    session.clear()

    return redirect("/")

@app.route("/empty_cart", methods=["POST"])
def empty_cart():
    """Empty the cart."""

    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to empty the cart.")
    else:
        user = User.query.filter_by(email=logged_in_email).first()

        if user.cart_items:           
            for item in user.cart_items:
                db.session.delete(item)
            db.session.commit()

            flash("Cart emptied.")
        else:
            flash("Your cart is already empty.")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)


