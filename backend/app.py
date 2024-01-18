import json
from flask import Flask, request
import json
import users_dao
import datetime
from db import db
from db import User, Product, Cart

# define db filename
db_filename = "us-tw.db"
app = Flask(__name__)

### setup config ###
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

### initialize app ###
db.init_app(app)
with app.app_context():
    db.create_all()

### generalized response formats ###
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

### extract tokens for authentication ###
def extract_token(request):
    """
    Helper function to extract token from header of request
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, failure_response("Missing authorization header.", 400)

    # Header looks like "Authorization: Bearer <Token>"
    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        return False, (failure_response("Invalid authorization header", 400))

    return True, bearer_token

################ Greeting routes ################
@app.route("/api/")
def greeting():
    """Endpoint for greeting user by reading from .env file"""
    return "Welcome"

### authentication routes ###
@app.route("/api/register/", methods=["POST"])
def register_account():
    """
    Endpoint for registering a new session
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Missing email or password", 400)
    
    username = body.get("username")

    if username is None:
        return failure_response("Missing required info", 400)

    success, user = users_dao.create_user(email, password, username)

    if not success:
        return failure_response("User already exists", 400)
    
    db.session.add(user)
    db.session.commit()

    return success_response(user.serialize(), 201)


@app.route("/api/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Missing email or password", 400)

    success, user = users_dao.verify_credentials(email, password)

    if not success:
        return failure_response("Incorrect email or password", 401)
    
    if user is None: 
        return failure_response("login error", 401)
    
    user.renew_session()
    db.session.commit()

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })


@app.route("/api/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    success, update_token = extract_token(request)

    if not success:
        return update_token

    success_session, user = users_dao.renew_session(update_token)

    if not success_session:
        return failure_response("Invalid update token", 400)

    db.session.commit()

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })


@app.route("/api/logout/", methods=["POST"])
def logout():
    """
    Endpoint for logging out
    """
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)

    user.session_token = ""
    user.session_expiration = datetime.datetime.now()
    user.update_token = ""

    db.session.commit()
    return success_response({"message": "You have successfully logged out."})


### user routes ###
@app.route("/api/user/", methods=["GET"])
def get_user():
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)

    return success_response(user.serialize())

@app.route("/api/user/", methods=['DELETE'])
def delete_user():
    """Endpoint to delete a user by id with verified credentials"""
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)

    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/user/username/", methods=["PUT"])
def update_username():
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    body = json.loads(request.data)
    user.username = body.get("username", user.username)

    db.session.commit()
    return success_response(user.serialize())


### product cart interactions ###
@app.route("/api/user/cart/all/", methods=["GET"])
def get_all_cart():
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)

    return success_response([d.serialize() for d in user.cart_items], 400)

@app.route("/api/user/cart/<int:cart_id>/", methods=["GET"])
def get_cart(cart_id):
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    item = Cart.query.filter_by(cartID=cart_id).first()
    if item is None: 
        return failure_response("item not found in cart!")
    
    return success_response(item.serialize())

@app.route("/api/user/cart/<int:product_id>/", methods=["POST"])
def add_user_cart(product_id):
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    product = Product.query.filter_by(prodID=product_id).first()
    if product is None:
        return failure_response("product not found! ")
    
    if product in user.cart_items: 
        return failure_response("product already in cart")
    
    item = Cart(userID = user.userID, prodID = product.prodID)

    db.session.add(item)

    # user.cart_items.append(item)
    
    db.session.commit()

    return success_response(user.serialize())

@app.route("/api/user/cart/<int:cart_id>/quantity/", methods=["PUT"])
def change_quantity(cart_id):
    """
    Change quantity of an item in cart by `quantity` amout
    """
    success, session_token = extract_token(request)

    if not success:
        return failure_response("Could not extract session token", 400)

    user = users_dao.get_user_by_session_token(session_token)
    if user is None or not user.verify_session_token(session_token):
        return failure_response("Invalid session token", 400)
    
    item = Cart.query.filter_by(cartID = cart_id).first()

    if item is None:
        return failure_response("Item not in cart")
    
    body = json.loads(request.data)

    quantity = body.get("quantity")
    item.quantity = item.quantity + quantity

    db.session.commit()

    return success_response(item.serialize())


### product routes ###
@app.route("/api/products/", methods=["GET"])
def get_all_products():
    return success_response({"products": [c.serialize() for c in Product.query.all()]})

@app.route("/api/products/<int:prod_id>/", methods=["GET"])
def get_product(prod_id):
    product = Product.query.get(prod_id).first()

    if product is None:
        return failure_response("Product not found")
    else: 
        return success_response(product.serialize())
    
@app.route("/api/products/", methods=["POST"])
def add_product():
    body = json.loads(request.data)

    new_product = Product()
    
    name = body.get("name")
    price = body.get("price")
    if name is None or price is None: 
        return failure_response("Some necessary info are not provided", 400)
    
    new_product.name = name
    new_product.price = price
    new_product.description = body.get("description")
    new_product.ingredients = body.get("ingredients")
    new_product.weight_oz = body.get("weight_oz")
    new_product.category = body.get("cateogry")
    new_product.picture = body.get("picture")
    
    db.session.add(new_product)
    db.session.commit()
    return success_response(new_product.serialize(), 201)

@app.route("/api/products/<int:product_id>/", methods=["PUT"])
def update_product(product_id): 
    body = json.loads(request.data)

    product = Product.query.filter_by(prod_id = product_id).first()
    
    if product is None:
        return failure_response("Product not found")
    
    product.name = body.get("name", product.name)
    product.description = body.get("description", product.description)
    product.ingredients = body.get("ingredients", product.ingredients)
    product.weight_oz = body.get("weight_oz", product.weight_oz)
    product.category = body.get("category", product.category)
    product.picture = body.get("picture", product.picture)
    
    db.session.commit()
    return success_response(product.serialize())

### Endpoints for testing ###
@app.route("/api/user/all/", methods=["GET"])
def get_all_user():
    return [c.serialize() for c in User.query.all()]


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)