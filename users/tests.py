from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(email='test@test.com', name='T', surname='T', password='pass')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('pass'))
