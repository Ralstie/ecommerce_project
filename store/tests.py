"""Tests for the eCommerce application and REST API."""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Store, Product, Review, UserProfile


class StoreTest(APITestCase):
    """Test core store creation and protected API behaviour."""

    def setUp(self):
        """Create a vendor and an authenticated API client for each test."""
        self.user = User.objects.create_user(
            username='vendor',
            password='TestPassword123!'
        )
        UserProfile.objects.create(user=self.user, role='VENDOR')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

    def test_store_creation(self):
        """Verify that a store can be created for a vendor."""
        store = Store.objects.create(
            vendor=self.user,
            name='Anime Store',
            description='Anime products'
        )

        self.assertEqual(store.name, 'Anime Store')

    def test_vendor_can_create_store_through_api(self):
        """Verify that an authenticated vendor can create a store through the API."""
        response = self.client.post(
            reverse('api_stores'),
            {
                'name': 'API Anime Store',
                'description': 'Products created through the API.'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(Store.objects.first().vendor, self.user)

    def test_vendor_can_create_product_through_api(self):
        """Verify that a vendor can add a product only to their own store."""
        store = Store.objects.create(
            vendor=self.user,
            name='Anime Store',
            description='Anime products'
        )

        response = self.client.post(
            reverse('api_products'),
            {
                'store': store.id,
                'name': 'Anime Figure',
                'description': 'Collectible figure.',
                'price': '299.99',
                'stock': 5
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_unauthenticated_user_cannot_create_store(self):
        """Verify that unauthenticated clients cannot use protected API writes."""
        self.client.credentials()

        response = self.client.post(
            reverse('api_stores'),
            {
                'name': 'Unauthorised Store',
                'description': 'Should not be created.'
            },
            format='json'
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Store.objects.count(), 0)

    def test_vendor_can_retrieve_reviews(self):
        """Verify that an authenticated vendor can retrieve product reviews."""
        store = Store.objects.create(
            vendor=self.user,
            name='Anime Store',
            description='Anime products'
        )
        product = Product.objects.create(
            store=store,
            name='Figure',
            description='Figure',
            price='100.00',
            stock=2
        )
        buyer = User.objects.create_user(
            username='buyer',
            password='BuyerPassword123!'
        )
        Review.objects.create(
            buyer=buyer,
            product=product,
            rating=5,
            comment='Excellent product.',
            verified=True
        )

        response = self.client.get(reverse('api_reviews'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 5)
