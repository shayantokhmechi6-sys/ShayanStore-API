# ShayanStore API

ShayanStore API is a backend REST API for an online store, built with FastAPI and SQLAlchemy.

## Features

- User registration and login
- JWT authentication
- User profile management
- Admin role and access control
- Product management
- Shopping cart management
- Order management
- Payment simulation
- Stock management
- Role-based authorization
- Input validation with Pydantic
- SQLite database with SQLAlchemy
- Docker support
- Swagger API documentation

## Technologies

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT
- Argon2
- Docker
- Uvicorn
- Swagger UI


## Project Structure

```text
ShayanStore-API/
└── backend/
    ├── database.py
    ├── dependencies.py
    ├── models.py
    ├── schemas.py
    ├── security.py
    ├── main.py
    ├── requirements.txt
    ├── Dockerfile
    └── .dockerignore
```

## Installation

### Using Docker

Build the Docker image:

```bash
docker build -t shayanstore-api ./backend
```

Create a Docker volume for the database:

```bash
docker volume create shayanstore-data
```

Run the Docker container:

```bash
docker run -p 8000:8000 -e SECRET_KEY="your-secret-key" -v shayanstore-data:/app/data shayanstore-api
```

The API will be available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

## Authentication & Authorization

ShayanStore API uses JWT-based authentication.

- Users can register and log in.
- Passwords are securely hashed using Argon2.
- JWT tokens are used to authenticate protected endpoints.
- Users can access and manage their own resources.
- Admin-only endpoints are protected with role-based authorization.


## API Endpoints

### Authentication

- `POST /users` — Register a new user
- `POST /login` — Login and receive a JWT token
- `GET /profile` — Get the current user's profile

### Users

- `GET /users` — Get all users (Admin only)
- `GET /users/{user_id}` — Get a user's profile
- `PUT /users/{user_id}` — Update a user's profile
- `DELETE /users/{user_id}` — Delete a user

### Products

- `POST /products` — Create a product (Admin only)
- `GET /products` — Get all products
- `GET /product/{product_id}` — Get a product
- `PUT /products/{product_id}` — Update a product (Admin only)
- `DELETE /products/{product_id}` — Delete a product (Admin only)

### Cart

- `POST /cart` — Create a shopping cart
- `GET /cart` — Get the current user's cart
- `POST /cart-item` — Add a product to the cart
- `GET /cart_items` — Get cart items
- `GET /cart_items/{cart_item_id}` — Get a cart item
- `PUT /cart_items/{cart_item_id}` — Update cart item quantity
- `DELETE /cart_items/{cart_item_id}` — Delete a cart item

### Orders

- `POST /order` — Create an order
- `GET /order` — Get the current user's orders
- `GET /order/{order_id}` — Get an order
- `GET /order/{order_id}/items` — Get order items
- `PUT /order/{order_id}/cancel` — Cancel a pending order
- `DELETE /order/{order_id}` — Delete an order

### Payments

- `POST /payment` — Create a payment
- `GET /payments` — Get the current user's payments
- `GET /payment/{payment_id}` — Get a payment
- `PUT /payment/{payment_id}/verify` — Verify a pending payment
- `DELETE /payment/{payment_id}` — Delete a payment

## API Documentation

Interactive API documentation is available through Swagger UI.

When running the project locally:

http://localhost:8000/docs