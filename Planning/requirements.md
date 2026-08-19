# eCommerce Application Requirements

## System Description

The system will be a Django-based eCommerce marketplace.
Users will be able to register as either buyers or vendors.

## Buyers

Buyers will be able to:

1. Register an account.
2. Log in and log out.
3. View stores.
4. View products.
5. Search for products.
6. Add products to a shopping cart.
7. Update product quantities.
8. Remove products from the cart.
9. Checkout.
10. Receive an invoice by email.
11. View their orders.
12. Leave product reviews.
13. Leave verified or unverified reviews.
14. Recover a forgotten password.

## Vendors

Vendors will be able to:

1. Register as a vendor.
2. Log in and log out.
3. Create stores.
4. View their stores.
5. Edit their stores.
6. Delete their stores.
7. Add products.
8. View products.
9. Edit products.
10. Delete products.

## Administrators

Administrators will be able to:

1. Manage users.
2. Manage vendors.
3. Manage buyers.
4. Manage stores.
5. Manage products.
6. Manage reviews.

## Shopping Cart

The shopping cart will use Django sessions.

## Checkout

The checkout process will:

1. Validate the cart.
2. Create an order.
3. Create order items.
4. Calculate the total.
5. Update product stock.
6. Create an invoice.
7. Email the invoice to the buyer.
8. Remove the products from the session cart.

## Reviews

A review will be marked as verified if the buyer
has previously purchased the product.

Reviews from buyers who have not purchased the
product will be marked as unverified.

## Password Recovery

Users will be able to request a password reset email.
The reset link will contain a secure token and will expire
after a limited period.