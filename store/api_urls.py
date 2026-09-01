"""URL routes for the eCommerce REST API."""

from django.urls import path

from . import views

urlpatterns = [
    path('stores/', views.api_stores, name='api_stores'),
    path('products/', views.api_products, name='api_products'),
    path('reviews/', views.api_reviews, name='api_reviews'),
]
