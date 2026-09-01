# E-Commerce Marketplace

A Django-based e-commerce marketplace developed as part of Task 19 - Django – eCommerce Application Part 2.

The application supports buyer and vendor accounts, vendor stores and products, shopping cart and checkout functionality, product reviews, and a protected Django REST Framework API.

## Features

- User registration with BUYER and VENDOR roles
- Vendor dashboard
- Vendor store creation, editing and deletion
- Vendor product creation
- Product listings and details
- Session-based shopping cart
- Checkout and orders
- Product reviews with purchase verification
- Login, logout and password reset
- REST API using Django REST Framework
- Token authentication for API clients
- Vendor-only API permissions for creating stores, adding products and retrieving reviews

## Technologies Used

- Python 3.14
- Django 6.1
- Django REST Framework 3.18
- MySQL
- HTML, CSS and Bootstrap
- Pillow
- mysqlclient

## Project Structure

```text
ecommerce_project/
├── manage.py
├── requirements.txt
├── README.md
├── Planning/
├── ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── store/
    ├── models.py
    ├── forms.py
    ├── serializers.py
    ├── views.py
    ├── api_urls.py
    ├── urls.py
    ├── tests.py
    ├── migrations/
    └── templates/
```

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd ecommerce_project
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure MySQL

Create a MySQL database called:

```text
ecommerce_db
```

Set the following environment variables before running Django:

Windows Command Prompt:

```cmd
set MYSQL_DATABASE=ecommerce_db
set MYSQL_USER=root
set MYSQL_PASSWORD=your_mysql_password
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
```

PowerShell:

```powershell
$env:MYSQL_DATABASE="ecommerce_db"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_mysql_password"
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
```

The project no longer stores a real database password in `settings.py`.

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Running Tests

Run the complete test suite with:

```bash
python manage.py test
```

The tests include:

- Store creation
- Vendor store creation through the API
- Vendor product creation through the API
- Rejection of unauthenticated API writes
- Retrieval of product reviews by an authenticated vendor

## REST API

The API is implemented with Django REST Framework.

The API uses token authentication. Authentication is required for the API endpoints, and only users with a VENDOR profile may create stores, add products, or retrieve reviews.

### Obtain an API token

First create a vendor account through the website or Django admin.

Then request a token:

```http
POST /api-token-auth/
```

Example JSON/form data:

```text
username=vendor
password=your_password
```

A successful response contains:

```json
{
    "token": "your-token-value"
}
```

Include the token in subsequent API requests:

```http
Authorization: Token your-token-value
```

### Stores

List stores:

```http
GET /api/stores/
```

Create a store as an authenticated vendor:

```http
POST /api/stores/
```

Example JSON:

```json
{
    "name": "Anime Store",
    "description": "Anime figures and collectibles."
}
```

The authenticated vendor is automatically assigned as the store owner.

### Products

List products:

```http
GET /api/products/
```

Create a product as an authenticated vendor:

```http
POST /api/products/
```

Example JSON:

```json
{
    "store": 1,
    "name": "Anime Figure",
    "description": "Collectible anime figure.",
    "price": "299.99",
    "stock": 10
}
```

A vendor can only add products to a store that belongs to that vendor.

### Reviews

Retrieve product reviews as an authenticated vendor:

```http
GET /api/reviews/
```

Example response:

```json
[
    {
        "id": 1,
        "buyer": "buyer1",
        "product": 1,
        "product_name": "Anime Figure",
        "rating": 5,
        "comment": "Excellent product.",
        "verified": true,
        "created_at": "2026-09-01T10:00:00Z"
    }
]
```

## API Security

The API uses Django REST Framework authentication and permissions.

- Unauthenticated clients cannot perform protected API operations.
- Vendor checks are performed before creating stores or products.
- A vendor cannot add a product to another vendor's store.
- API serializers prevent clients from assigning a different vendor as the store owner.
- Review retrieval is restricted to authenticated vendors.
- Database credentials are read from environment variables instead of being stored in source code.

## Useful URLs

Website:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

API stores:

```text
http://127.0.0.1:8000/api/stores/
```

API products:

```text
http://127.0.0.1:8000/api/products/
```

API reviews:

```text
http://127.0.0.1:8000/api/reviews/
```

API token:

```text
http://127.0.0.1:8000/api-token-auth/
```

Browsable API authentication:

```text
http://127.0.0.1:8000/api-auth/login/
```

## Notes

Do not commit passwords, API tokens, secret keys, database credentials, or other sensitive information to GitHub.

For production deployment, `DEBUG` should be disabled and a secure `DJANGO_SECRET_KEY` should be supplied through an environment variable.
