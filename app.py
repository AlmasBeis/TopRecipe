# app.py
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Database file will be created in the project folder
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    num_ratings = db.Column(db.Integer, default=0)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image = db.Column(db.Text, default="https://m.media-amazon.com/images/I/517gfFg6I6L._AC_.jpg")
    description = db.Column(db.Text, default="...")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return self.name


with app.app_context():
    db.create_all()


# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400
#
#     if User.query.filter_by(username=username).first():
#         return jsonify({'message': 'Username already exists'}), 400
#
#     new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'}), 201


# Endpoint to authenticate a user
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     user = User.query.filter_by(username=username).first()
#
#     if not user:
#         return jsonify({'message': 'User not found'}), 401
#
#     if not check_password_hash(user.password, password):
#         return jsonify({'message': 'Incorrect password'}), 401
#
#     return jsonify({'message': 'Login successful'}), 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        existing_user = User.query.filter_by(username=request.form["username"]).first()

        if existing_user:
            flash("Username already exists. Please choose a different username.", "error")
            return redirect(url_for("user_create"))
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        user = User(
            username=request.form["username"],
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")


@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)


@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)


if __name__ == '__main__':
    app.run()
# @app.route('/signup_user', methods=['POST'])
# def signup_user():
#     username = request.form.get('signupUsername').lower()
#     user = User.query.filter_by(username=username).first()
#
#     if user is None:
#         new_user = User(
#             username=username,
#             hashed_password=generate_password_hash(request.form.get('signupPassword'), method='sha256'),
#             firstname=request.form.get('firstName'),
#             lastname=request.form.get('lastName')
#         )
#
#         db.session.add(new_user)
#         db.session.commit()
#
#         return "success"
#     else:
#         return "fail"
#
# # User Login
# @app.route('/login_user', methods=['POST'])
# def login_user():
#     username = request.form.get('loginUsername').lower()
#     user = User.query.filter_by(username=username).first()
#
#     if user:
#         if check_password_hash(user.hashed_password, request.form.get('loginPassword')):
#             session['username'] = user.username
#             session['userid'] = user.id
#             session['isLoggedin'] = True
#
#             message = "Welcome back, " + user.username + ". You will be redirected to your MyRecipes page."
#             response = {
#                 "username": user.username,
#                 "_id": user.id,
#                 "message": message
#             }
#             return jsonify(response)
#         else:
#             return "1"  # Wrong password
#     else:
#         return "2"  # No user by that username
#
# if __name__ == '__main__':
#     app.run(debug=True)
