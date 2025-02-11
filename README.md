# Microservices Order Management

This is a simple microservice-based order management system, deployed across two virtual machines (VMs), implemented using Python Flask for the backend services and HTML for the frontend.

## Architecture

The system is made up of two main services:

1. **User Service (VM1)**: Manages user registration, login, and token validation.
2. **Order Service (VM2)**: Handles order placement, order retrieval, and order management.

These services interact with each other over HTTP requests. The frontend HTML page provides an interface for users to create an account, log in, and place orders.

### Technologies Used:
- **Backend**:
  - Python
  - Flask (REST API framework)
  - Flask-CORS (Cross-Origin Resource Sharing)
  - Requests (for HTTP requests between services)

- **Frontend**:
  - HTML, CSS, JavaScript (AJAX for making requests)

- **Deployment**:
  - VirtualBox (for creating virtual machines)
  - Two VMs running Ubuntu (Lubuntu used for VMs)

## Features

- **User Service**:
  - Create new users with name, email, password, and address.
  - Login and retrieve an authentication token.
  - Validate user authentication tokens.

- **Order Service**:
  - Place orders with an item description.
  - Retrieve orders placed by a logged-in user.

- **Frontend**:
  - Simple web interface to manage users and orders.

## Setup Instructions

### Prerequisites

- **VirtualBox** installed on the host machine.
- **Two virtual machines (VMs)** running Lubuntu (2024MB RAM, 30GB Disk each).
- Basic knowledge of setting up Python environments and Flask apps.

### Steps to Deploy the Project

1. **Set up VirtualBox and VMs**:
   - Install **VirtualBox** on your host machine.
   - Create two VMs with Lubuntu (2024MB RAM, 30GB Disk each).
   - Ensure that the VMs are on the same network and can communicate with each other.

2. **Deploy User Service on VM1**:
   - Clone this repository on **VM1**.
   - Install Python dependencies:  
     ```bash
     pip install -r requirements.txt
     ```
   - Start the User Service:
     ```bash
     python app.py
     ```

3. **Deploy Order Service on VM2**:
   - Clone this repository on **VM2**.
   - Install Python dependencies:  
     ```bash
     pip install -r requirements.txt
     ```
   - Start the Order Service:
     ```bash
     python app.py
     ```

4. **Deploy the Frontend**:
   - Clone this repository on your local machine or VM.
   - Open the `index.html` file in your browser.

5. **Configure Networking**:
   - Make sure the User Service on **VM1** is accessible from **VM2** and your browser. 
   - In the `frontend/index.html`, replace the URLs for the services to point to the correct IP addresses of VM1 and VM2.

### How to Use the Application

1. **Create a User**:
   - Enter the user's name, email, password, and address in the "Create User" section.
   - A new user will be created if the information is valid.

2. **Login**:
   - Enter the email and password of the registered user to log in.
   - Upon successful login, you will receive an authentication token.

3. **Create an Order**:
   - After logging in, enter the item name in the "Create Order" section to place an order.
   - The order will be linked to the user based on the authentication token.

4. **View Orders**:
   - After logging in, you can view all your orders under the "Orders" section.

### API Endpoints

- **User Service (VM1)**:
  - `POST /users`: Create a new user.
  - `POST /users/login`: Login and get a token.
  - `GET /users/token/<token>`: Validate the token.

- **Order Service (VM2)**:
  - `POST /orders`: Create a new order.
  - `GET /orders`: Fetch all orders for the logged-in user.
  - `GET /orders/<order_id>`: Fetch a specific order by ID.

