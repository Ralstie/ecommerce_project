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
    OrderItem
)

from .forms import (
    RegistrationForm,
    StoreForm,
    ProductForm,
    ReviewForm
)


# =============
# HOME PAGE
# =============

def home(request):

    return render(
        request,
        'store/home.html'
    )


# ===================
# USER REGISTRATION
# ===================

def register(request):

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