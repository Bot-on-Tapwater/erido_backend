# Skinsoko Project

Welcome to Skinsoko, an ecommerce platform specializing in Korean beauty products. This project is built with Django for the backend and Vue.js for the frontend.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Routes](#api-routes)
  - [Authentication and User Management](#authentication-and-user-management)
  - [Product Management](#product-management)
  - [User Profile](#user-profile)
  - [Shopping Cart](#shopping-cart)
  - [Order Management](#order-management)
  - [Category Management](#category-management)
  - [Reviews and Ratings](#reviews-and-ratings)
  - [Search Features](#search-features)
  - [Shipping and Address](#shipping-and-address)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- Product management
- Shopping cart functionality
- Order processing
- Payment integration
- Responsive design
- SEO-friendly URLs
- Optimized for performance

## Requirements

- Python 3.8+
- Django 3.2+
- Node.js 14+
- PostgreSQL 12+
- Redis (for caching and background tasks)
- Nginx (for serving static files and proxying requests)
- Gunicorn (for running the Django application)

## Installation

### Backend
Clone the repository:

`git clone https://github.com/Bot-on-Tapwater/skinsoko_project.git`

`cd skinsoko_project`

Create a virtual environment and activate it:

`python3 -m venv venv`
`source venv/bin/activate`

Install the required packages:

`pip install -r requirements.txt`

Set up the PostgreSQL database and update the DATABASES setting in settings.py:

>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

Apply the migrations:

`python manage.py migrate`

Create a superuser:

`python manage.py createsuperuser`

Collect static files:

`python manage.py collectstatic`

### Frontend
Navigate to the frontend directory and install dependencies:

`cd frontend`

`npm install`

Build the frontend application:

`npm run build`

## Configuration

### Environment Variables

Create a .env file in the project root and add the following:


`DEBUG=1
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://your_db_user:your_db_password@localhost/your_db_name
REDIS_URL=redis://localhost:6379/0`

## Usage
To run the Django server, use:

`python manage.py runserver`

## API Routes
### Authentication and User Management
- Login
  - Method: POST
  - Path: /login/
  - View: views.login_view
  - Description: Handles user login.
- Logout
  - Method: POST
  - Path: /logout/
  - View: views.logout_view
  - Description: Handles user logout.
- Register

  - Method: POST
  - Path: /register/
  - View: views.register_view
  - Description: Handles user registration.
- Password Reset

  - Request: POST /password_reset/request/ - Request password reset.
  - Request: POST /password_reset/validate/ - Validate reset token.
  - Request: POST /password_reset/reset/ - Reset password.
- User Status

  - Method: GET
  - Path: /user_status/
  - View: views.user_status
  - Description: Displays the logged-in user's ID.

### Product Management
- List All Products

  - Method: GET
  - Path: /products/
  - View: views.list_all_products
  - Description: Retrieves a list of all products.
- Get Product Details

  - Method: GET
  - Path: /products/<slug:slug>/
  - View: views.get_product_with_product_id
  - Description: Retrieves details of a specific product.

### User Profile
- Get User Profile Details

  - Method: GET
  - Path: /users/
  - View: views.get_user_with_user_id_profile_details
  - Description: Retrieves profile details of a specific user.
- List User Reviews

  - Method: GET
  - Path: /users/reviews/
  - View: views.list_reviews_created_by_user_with_user_id
  - Description: Retrieves reviews created by a user.
- List User Orders

  - Method: GET
  - Path: /users/orders/
  - View: views.list_orders_placed_by_user_with_user_id
  - Description: Retrieves a list of orders placed by a specific user.

### Shopping Cart
- Get Cart Contents

  - Method: GET
  - Path: /users/cart/
  - View: views.get_contents_of_shopping_cart_of_user
  - Description: Retrieves the contents of a user's shopping cart.
- Add Product to Cart

  - Method: POST
  - Path: /users/cart/add/<int:productId>/
  - View: views.add_product_to_user_cart
  - Description: Adds a product to a user's cart.
- Remove Product from Cart

  - Method: DELETE
  - Path: /users/cart/remove/<int:productId>/
  - View: views.remove_product_from_user_cart
  - Description: Removes a product from a user's cart.
- Clear Cart

  - Method: DELETE
  - Path: /users/cart/clear/
  - View: views.clear_entire_shopping_cart
  - Description: Clears the entire shopping cart.
- Update Product in Cart

  - Method: PUT
  - Path: /users/cart/update/<int:productId>/
  - View: views.update_product_in_user_cart
  - Description: Updates product details in the cart.

### Order Management
- List All Orders

  - Method: GET
  - Path: /orders/
  - View: views.get_list_of_all_orders
  - Description: Retrieves a list of all orders.
- Get Order Details

  - Method: GET
  - Path: /orders/<uuid:id>/
  - View: views.get_details_of_order_with_order_id
  - Description: Retrieves the details of a specific order.
- Create New Order

  - Method: POST
  - Path: /users/orders/create/
  - View: views.create_new_order
  - Description: Creates a new order for a user.
- Cancel Order

  - Method: DELETE
  - Path: /orders/<uuid:id>/cancel/
  - View: views.cancel_order_with_order_id
  - Description: Cancels a specific order.
- Order Items

  - Method: GET
  - Path: /orders/<uuid:id>/order_items/
  - View: views.get_order_items_for_order_with_order_id
  - Description: Retrieves items for a specific order.
- Update Order Status

  - Method: PUT
  - Path: /orders/<uuid:id>/deliver/
  - View: views.update_order_to_delivered_with_order_id
  - Description: Updates the status of an order to delivered.

### Category Management
- List All Main Categories

  - Method: GET
  - Path: /main-categories/
  - View: views.get_list_of_all_main_categories
  - Description: Retrieves a list of all main product categories.
- List Subcategories

  - Method: GET
  - Path: /subcategories/<str:main_category>/
  - View: views.get_list_of_all_sub_categories_in_a_main_category
  - Description: Retrieves subcategories for a given main category.
- List All Brands

  - Method: GET
  - Path: /brands/
  - View: views.get_list_of_all_brands
  - Description: Retrieves a list of all brands.

### Reviews and Ratings
- Get Product Reviews

  - Method: GET
  - Path: /products/<slug:slug>/reviews/
  - View: views.get_reviews_for_product_with_product_id
  - Description: Retrieves reviews for a specific product.
- Create Product Review

  - Method: POST
  - Path: /users/products/<slug:slug>/reviews/create/
  - View: views.creat_review_for_product_with_product_id
  - Description: Creates a review for a specific product.
- Delete User Review

  - Method: DELETE
  - Path: /users/reviews/<int:id>/delete/
  - View: views.user_delete_review
  - Description: Deletes a specific review created by a user.
### Search Features
- Search Products
  - Method: GET
  - Path: /search/
  - View: views.search
  - Description: Searches for products based on a query.
### Shipping and Address
- Get User Saved Addresses
  - Method: GET
  - Path: `/users/#

## Contributing
Contributions are welcome! Please follow these guidelines:

- Fork the repository and create your branch: git checkout -b feature.
- Commit your changes: git commit -am 'Add new feature'.
- Push to the branch: git push origin feature.
- Submit a pull request.

## License
For permission to use, modify, or distribute this project, please contact the author.