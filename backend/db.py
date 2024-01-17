import hashlib
import bcrypt
import os
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    cart_items = db.relationship(
        "Product",
        cascade = "delete",
        secondary = "cart",
        back_populates = "cart_users"
    )

    # authentication
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # authentication session
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions, i.e.
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token

    def serialize(self):
        return {
            "userID": self.userID, 
            "username": self.username, 
            "email": self.email, 
            "cart_items": [s.serialize() for s in self.cart_items]
        }

        

class Product(db.Model):
    __tablename__ = "product"

    prodID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_users = db.relationship(
        "User",
        secondary = "cart",
        back_populates = "cart_items"
    )

    # basics
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    ingredients = db.Column(db.String)
    weight_oz = db.Column(db.Float)
    category = db.Column(db.String)
    picture = db.Column(db.LargeBinary)

    # dietary restrictions (for foods only)
    # kosher = db.Column(db.Bool)
    # dairy_free = db.Column(db.Bool)
    # gluten_free = db.Column(db.Bool)
    # vegan = db.Column(db.Bool)
    # organic = db.Column(db.Bool)

    def serialize(self):
        return {
            "prodID": self.prodID,
            "name": self.name, 
            "price": self.price, 
            "description": self.description, 
            "ingredients": self.ingredients, 
            "weight_oz": self.weight_oz,
            "category": self.category, 
            "picture": self.picture,
        }


class Cart(db.Model):
    cartID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    prodID = db.Column(db.Integer, db.ForeignKey('product.prodID'))
    quantity = db.Column(db.Integer, nullable=False)

    def __init__ (self, **kwargs):
        self.userID = kwargs.get("userID")
        self.prodID = kwargs.get("prodID")
        self.quantity = 1

    def serialize(self): 
        return {
            "cartID": self.cartID, 
            "userID": self.userID, 
            "prodID": self.prodID, 
            "quantity": self.quantity
        }