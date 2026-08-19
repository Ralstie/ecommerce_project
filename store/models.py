from django.contrib.auth.models import User
from django.db import models


# =============================================
# USER PROFILE
# Stores whether the user is a BUYER or VENDOR
# =============================================

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('BUYER', 'Buyer'),
        ('VENDOR', 'Vendor'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =========================================
# STORE
# Each vendor can have one or more stores
# =========================================

class Store(models.Model):

    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stores'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# =================================
# PRODUCT
# Each product belongs to a Store
# =================================

class Product(models.Model):

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# ==============
# ORDER
# ==============

class Order(models.Model):

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        default='Completed'
    )

    def __str__(self):
        return f"Order #{self.id}"


# ==================
# ORDER ITEM
# ==================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x {self.quantity}"


# =================
# REVIEW
# =================

class Review(models.Model):

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product} - {self.rating}/5"