from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad

class AdModelTest(TestCase):
    def test_create_ad(self):
        user = User.objects.create_user(username='testuser', password='12345')
        ad = Ad.objects.create(
            user=user,
            title='Обменяю книгу',
            description='В хорошем состоянии',
            category='Книги',
            condition='used'
        )
        self.assertEqual(ad.title, 'Обменяю книгу')
