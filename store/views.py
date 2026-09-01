from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.db import transaction

from .models import (
    UserProfile,
    Store,
    Product,
    Order,
    OrderItem,
    Review
)

from .forms import (
    RegistrationForm,
    StoreForm,
    ProductForm,
    ReviewForm
)

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    StoreSerializer,
    ProductSerializer,
    ReviewSerializer,
)


# =============
# HOME PAGE
# =============

def home(request):

    'Render the marketplace home page.'
    return render(
        request,
        'store/home.html'
    )


# ===================
# USER REGISTRATION
# ===================

def register(request):

    'Register a new buyer or vendor and log the user in.'
    if request.method == 'POST':

        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect('home')

    else:

        form = RegistrationForm()

    return render(
        request,
        'store/register.html',
        {
            'form': form
        }
    )


# ===================
# VENDOR DASHBOARD
# ===================

@login_required
def vendor_dashboard(request):

    'Display the authenticated vendor’s stores.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    stores = Store.objects.filter(
        vendor=request.user
    )

    return render(
        request,
        'store/vendor_dashboard.html',
        {
            'stores': stores
        }
    )


# ==============
# CREATE STORE
# ==============

@login_required
def store_create(request):

    'Allow an authenticated vendor to create a store they own.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    if request.method == 'POST':

        form = StoreForm(
            request.POST
        )

        if form.is_valid():

            store = form.save(
                commit=False
            )

            store.vendor = request.user

            store.save()

            return redirect(
                'vendor_dashboard'
            )

    else:

        form = StoreForm()

    return render(
        request,
        'store/store_form.html',
        {
            'form': form
        }
    )


# ============
# EDIT STORE
# ============

@login_required
def store_edit(request, store_id):

    'Allow an authenticated vendor to edit one of their own stores.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    store = get_object_or_404(
        Store,
        id=store_id,
        vendor=request.user
    )

    if request.method == 'POST':

        form = StoreForm(
            request.POST,
            instance=store
        )

        if form.is_valid():

            form.save()

            return redirect(
                'vendor_dashboard'
            )

    else:

        form = StoreForm(
            instance=store
        )

    return render(
        request,
        'store/store_form.html',
        {
            'form': form,
            'store': store
        }
    )


# ==============
# DELETE STORE
# ==============

@login_required
def store_delete(request, store_id):

    'Allow an authenticated vendor to delete one of their own stores.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    store = get_object_or_404(
        Store,
        id=store_id,
        vendor=request.user
    )

    if request.method == 'POST':

        store.delete()

        return redirect(
            'vendor_dashboard'
        )

    return render(
        request,
        'store/store_confirm_delete.html',
        {
            'store': store
        }
    )


# ================
# VENDOR PRODUCTS
# ================

@login_required
def vendor_products(request, store_id):

    'Display the products belonging to one of the vendor’s stores.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    store = get_object_or_404(
        Store,
        id=store_id,
        vendor=request.user
    )

    products = Product.objects.filter(
        store=store
    )

    return render(
        request,
        'store/vendor_products.html',
        {
            'store': store,
            'products': products
        }
    )


# ===============
# CREATE PRODUCT
# ===============

@login_required
def product_create(request, store_id):

    'Allow an authenticated vendor to add a product to their own store.'
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != 'VENDOR':

        return redirect('home')

    store = get_object_or_404(
        Store,
        id=store_id,
        vendor=request.user
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            product.store = store

            product.save()

            return redirect(
                'vendor_products',
                store_id=store.id
            )

    else:

        form = ProductForm()

    return render(
        request,
        'store/product_form.html',
        {
            'form': form,
            'store': store
        }
    )


# ===================
# BUYER PRODUCT LIST
# ===================

def product_list(request):

    'Display all products available to buyers.'
    products = Product.objects.all()

    return render(
        request,
        'store/product_list.html',
        {
            'products': products
        }
    )


# ================
# PRODUCT DETAILS# ================

def product_detail(request, product_id):

    'Display the details of one product.'
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )


# ============
# ADD TO CART
# ============

def add_to_cart(request, product_id):

    'Add one unit of a product to the current session cart.'
    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get(
        'cart',
        {}
    )

    product_id = str(
        product.id
    )

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session['cart'] = cart

    request.session.modified = True

    return redirect(
        'cart'
    )


# ======
# CART
# ======

def cart(request):

    'Display the current session cart and calculate its total.'
    cart = request.session.get(
        'cart',
        {}
    )

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []

    total = 0

    for product in products:

        quantity = cart[
            str(product.id)
        ]

        item_total = (
            product.price * quantity
        )

        total += item_total

        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            }
        )

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


# =========
# CHECKOUT
# =========

@login_required
@transaction.atomic
def checkout(request):

    'Create an order from the current cart and reduce product stock.'
    cart = request.session.get(
        'cart',
        {}
    )

    if not cart:

        return redirect('cart')

    products = Product.objects.filter(
        id__in=cart.keys()
    )

    total = 0

    for product in products:

        quantity = cart[
            str(product.id)
        ]

        if quantity > product.stock:

            return render(
                request,
                'store/checkout_error.html',
                {
                    'product': product
                }
            )

        total += (
            product.price * quantity
        )

    order = Order.objects.create(
        buyer=request.user,
        total=total,
        status='Completed'
    )

    for product in products:

        quantity = cart[
            str(product.id)
        ]

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        product.stock -= quantity

        product.save()

    request.session['cart'] = {}

    request.session.modified = True

    return redirect(
        'order_success',
        order_id=order.id
    )


# ==============
# ORDER SUCCESS
# ==============

@login_required
def order_success(request, order_id):

    'Display an order confirmation for the authenticated buyer.'
    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user
    )

    return render(
        request,
        'store/order_success.html',
        {
            'order': order
        }
    )


# ===========
# ADD REVIEW
# ===========

@login_required
def add_review(request, product_id):

    'Allow a buyer to submit a review for a product.'
    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.buyer = request.user

            review.product = product

            purchased = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product
            ).exists()

            review.verified = purchased

            review.save()

            return redirect(
                'product_detail',
                product_id=product.id
            )

    else:

        form = ReviewForm()

    return render(
        request,
        'store/review_form.html',
        {
            'form': form,
            'product': product
        }
    )

# =========================
# REST API
# =========================

def _is_vendor(user):
    'Return whether the authenticated user has a vendor profile.'
    return UserProfile.objects.filter(user=user, role='VENDOR').exists()


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def api_stores(request):
    'List stores or allow an authenticated vendor to create a store.'
    if request.method == 'GET':
        stores = Store.objects.select_related('vendor').all()
        serializer = StoreSerializer(stores, many=True, context={'request': request})
        return Response(serializer.data)

    if not _is_vendor(request.user):
        return Response(
            {'detail': 'Only authenticated vendors can create stores.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = StoreSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(vendor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def api_products(request):
    'List products or allow a vendor to add a product to their own store.'
    if request.method == 'GET':
        products = Product.objects.select_related('store').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)

    if not _is_vendor(request.user):
        return Response(
            {'detail': 'Only authenticated vendors can create products.'},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = ProductSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def api_reviews(request):
    'Return product reviews to authenticated vendors.'
    if not _is_vendor(request.user):
        return Response(
            {'detail': 'Only authenticated vendors can retrieve reviews.'},
            status=status.HTTP_403_FORBIDDEN
        )

    reviews = Review.objects.select_related('buyer', 'product').all()
    serializer = ReviewSerializer(
        reviews, many=True, context={'request': request}
    )
    return Response(serializer.data)
