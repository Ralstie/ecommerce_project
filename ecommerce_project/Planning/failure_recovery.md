# Failure and Recovery Plan

## Invalid Login

If incorrect login information is entered, the system
will display an error message.

## Invalid Registration

If registration information is invalid, the user will
receive validation errors.

## Product Does Not Exist

If a requested product does not exist, the system will
display a 404 page.

## Out of Stock

The system will prevent a buyer from purchasing more
products than are available.

## Invalid Cart

If a product in the session cart no longer exists,
the system will remove the invalid item.

## Database Failure

Database errors will be handled without exposing
technical information to the user.

## Email Failure

If an invoice email cannot be sent, the order should
not be silently lost. The error should be logged and
the system should notify the appropriate administrator.

## Password Reset Expired

If a password reset token has expired, the user will
be asked to request another password reset link.

## Unauthorized Access

Users attempting to access pages they do not have
permission to access will be denied.

## Checkout Failure

The cart should not be cleared until the order has
been successfully created.

Database transactions will be used where appropriate
to prevent incomplete orders.