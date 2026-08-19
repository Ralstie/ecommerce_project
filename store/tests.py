from django.test import TestCase
from django.contrib.auth.models import User

from .models import Store


class StoreTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='vendor',
            password='TestPassword123!'
        )

    def test_store_creation(self):

        store = Store.objects.create(
            vendor=self.user,
            name='Anime Store',
            description='Anime products'
        )

        self.assertEqual(
            store.name,
            'Anime Store'
        )