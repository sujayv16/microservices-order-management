from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for orders by user token
orders_by_user = {}

# URL of the User Service on VM1
USER_SERVICE_URL = "http://192.168.56.101:5001/users/"

# Helper function to validate user login token
def validate_user(token):
    response = requests.get(f"{USER_SERVICE_URL}token/{token}")
    return response.status_code == 200

@app.route('/orders', methods=['POST'])
def add_order():
    """Place a new order."""
    order_data = request.get_json()
    token = order_data.get('token')
    
    if not token or not validate_user(token):
        return jsonify({"error": "Invalid or missing authentication token!"}), 401
    
    if 'item' not in order_data:
        return jsonify({"error": "Order item is required!"}), 400
    
    # If no orders for this user, create an empty list
    if token not in orders_by_user:
        orders_by_user[token] = []

    # Create the order
    order = {
        "order_id": len(orders_by_user[token]) + 1,
        "item": order_data['item'],
        "status": "Pending",
        "user_token": token
    }
    
    # Add the order to the user's list of orders
    orders_by_user[token].append(order)
    
    return jsonify({"message": "Order placed successfully!"}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    """Fetch orders for the logged-in user."""
    token = request.args.get('token')  # Expect the token to be passed in query parameters
    
    if not token or not validate_user(token):
        return jsonify({"error": "Invalid or missing authentication token!"}), 401
    
    # Return the orders for this user
    user_orders = orders_by_user.get(token, [])
    return jsonify({"orders": user_orders})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Fetch a specific order by ID for the logged-in user."""
    token = request.args.get('token')
    
    if not token or not validate_user(token):
        return jsonify({"error": "Invalid or missing authentication token!"}), 401
    
    # Find the order for the logged-in user
    user_orders = orders_by_user.get(token, [])
    order = next((order for order in user_orders if order['order_id'] == order_id), None)
    
    if order:
        return jsonify(order)
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)

