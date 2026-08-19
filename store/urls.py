from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # ========
    # HOME
    # ========

    path(
        '',
        views.home,
        name='home'
    ),


    # ==============
    # REGISTRATION
    # ==============

    path(
        'register/',
        views.register,
        name='register'
    ),


    # ==========
    # LOGIN
    # ==========

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='store/login.html'
        ),
        name='login'
    ),


    # ============
    # LOGOUT
    # ============

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),


    # ==================
    # VENDOR DASHBOARD
    # ==================

    path(
        'vendor/dashboard/',
        views.vendor_dashboard,
        name='vendor_dashboard'
    ),


    # ===============
    # CREATE STORE
    # ===============

    path(
        'vendor/store/create/',
        views.store_create,
        name='store_create'
    ),


    # ==============
    # EDIT STORE
    # ==============

    path(
        'vendor/store/<int:store_id>/edit/',
        views.store_edit,
        name='store_edit'
    ),


    # =================
    # DELETE STORE
    # =================

    path(
        'vendor/store/<int:store_id>/delete/',
        views.store_delete,
        name='store_delete'
    ),


    # ======================
    # VIEW VENDOR PRODUCTS
    # ======================

    path(
        'vendor/store/<int:store_id>/products/',
        views.vendor_products,
        name='vendor_products'
    ),


    # ==================
    # CREATE PRODUCT
    # ==================

    path(
        'vendor/store/<int:store_id>/products/create/',
        views.product_create,
        name='product_create'
    ),


    # =====================
    # BUYER PRODUCT LIST
    # =====================

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),


    # ================
    # PRODUCT DETAILS
    # ================

    path(
        'products/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),


    # ============
    # ADD TO CART
    # ============

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),


    # =========
    # CART
    # =========

    path(
        'cart/',
        views.cart,
        name='cart'
    ),


    # ===========
    # CHECKOUT
    # ===========

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),


    # ===============
    # ORDER SUCCESS
    # ===============

    path(
        'order/success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),


    # ============
    # REVIEWS
    # ============

    path(
        'products/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),


    # ===============
    # PASSWORD RESET
    # ===============

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='store/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='store/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='store/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='store/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]