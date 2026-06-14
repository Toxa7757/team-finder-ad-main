import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_finder.settings')
django.setup()

from users.models import User
from projects.models import Project

# Clear existing data
Project.objects.all().delete()
User.objects.all().delete()

# Create superuser
User.objects.create_superuser('admin@yandex.ru', 'Admin', 'Adminov', 'admin', phone='+79991112233')

# Create users
maria = User.objects.create_user('maria@yandex.ru', 'Maria', 'Ivanova', 'password', phone='+79992223344')
ivan = User.objects.create_user('ivan@yandex.ru', 'Ivan', 'Petrov', 'password', phone='+79993334455')

# Create projects
p1 = Project.objects.create(name='TeamFinder', description='Cool platform for developers', owner=maria)
p1.participants.add(maria)

p2 = Project.objects.create(name='AI Assistant', description='Open-source AI helper', owner=ivan)
p2.participants.add(ivan)
p2.participants.add(maria)

print("Database populated successfully.")
print("Admin: admin@yandex.ru / admin")
print("User 1: maria@yandex.ru / password")
print("User 2: ivan@yandex.ru / password")
