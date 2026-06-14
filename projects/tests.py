from django.test import TestCase
from .models import Project
from users.models import User

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', name='T', surname='T', password='pass')
        self.project = Project.objects.create(name='Test Project', owner=self.user)

    def test_project_creation(self):
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(self.project.name, 'Test Project')
