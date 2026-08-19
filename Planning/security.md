# Security and Access Control

## Authentication

The application will use Django's built-in authentication system.

Users must log in before accessing protected functionality.

## User Roles

The system will contain:

- Buyer
- Vendor
- Administrator

## Buyer Permissions

Buyers can:

- Browse products
- Add products to their cart
- Checkout
- View their orders
- Leave reviews

Buyers cannot:

- Create stores
- Edit other users' stores
- Add products to stores they do not own

## Vendor Permissions

Vendors can:

- Create stores
- Edit their stores
- Delete their stores
- Add products to their stores
- Edit their products
- Delete their products

Vendors cannot modify another vendor's stores or products.

## Password Security

Passwords will be handled by Django's authentication
system and will not be stored as plain text.

## CSRF Protection

Django's CSRF protection will be used on forms.

## Database Security

The Django ORM will be used to prevent SQL injection.

## Password Reset

Password reset links will use secure tokens and will
expire after a limited period.

## Data Validation

The application will validate:

- Prices
- Quantities
- Email addresses
- User input
- Product stock
- Required fields