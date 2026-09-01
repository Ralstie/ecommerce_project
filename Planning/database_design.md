# Database Design

## 1. Overview

The eCommerce application uses a relational database to store information about users, vendors, stores, products, orders, reviews and shopping carts.

The database is designed to keep the information organised and to create relationships between the different parts of the application.

## 2. Main Database Tables

### User

Django's built-in User model is used to store user account information.

Main fields:
- id
- username
- email
- password

A user can be a buyer or a vendor.

### UserProfile

The UserProfile table stores additional information about each user.

Main fields:
- id
- user
- role

The role can be:
- BUYER
- VENDOR

Each UserProfile belongs to one User.

### Store

The Store table stores information about stores created by vendors.

Main fields:
- id
- vendor
- name
- description

A vendor can have a store.

### Product

The Product table stores the products available for sale.

Main fields:
- id
- store
- name
- description
- price
- stock
- image

Each product belongs to a store.

A store can contain many products.

### Order

The Order table stores customer orders.

Main fields:
- id
- buyer
- created_at
- status
- total

A buyer can have many orders.

### OrderItem

The OrderItem table stores the individual products included in an order.

Main fields:
- id
- order
- product
- quantity
- price

An order can contain multiple order items.

### Review

The Review table stores reviews written by customers about products.

Main fields:
- id
- product
- user
- rating
- comment
- created_at

A product can have multiple reviews.

## 3. Relationships

The main relationships are:

- User → UserProfile: One-to-One
- UserProfile → Store: One-to-Many for vendors
- Store → Product: One-to-Many
- User → Order: One-to-Many
- Order → OrderItem: One-to-Many
- Product → OrderItem: One-to-Many
- User → Review: One-to-Many
- Product → Review: One-to-Many

## 4. Database Structure

The basic relationship structure is:

User
│
├── UserProfile
│   └── Store
│       └── Product
│           └── Review
│
└── Order
    └── OrderItem
        └── Product

## 5. Data Integrity

Foreign keys are used to connect related records.

For example, a Product is connected to its Store using a foreign key. This helps prevent products from existing without a related store.

The database also uses appropriate field types such as:
- Integer fields for IDs and quantities
- Decimal fields for product prices
- Text fields for descriptions and comments
- Date/time fields for dates and timestamps

## 6. Django Database

The application uses Django models to define the database structure.

Django migrations are used to create and update the database tables.

The database can be updated using:

    python manage.py makemigrations
    python manage.py migrate

## 7. Conclusion

The database design provides a structured way to manage the main information required by the eCommerce application.

The relationships between users, stores, products, orders and reviews allow the application to manage both vendor and buyer activities.