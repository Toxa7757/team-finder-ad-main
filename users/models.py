import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile

class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)

class Skill(models.Model):
    name = models.CharField(max_length=124, unique=True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12, unique=True)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True, null=True)
    
    # Вариант 2: навыки пользователя
    skills = models.ManyToManyField(Skill, related_name='users', blank=True)
    
    # Базовая функциональность: избранные проекты
    favorites = models.ManyToManyField('projects.Project', related_name='interested_users', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def save(self, *with_perm, **kwargs):
        # Генерируем аватарку перед первым сохранением, если её нет
        if not self.avatar:
            self.avatar = self.generate_avatar()
        super().save(*with_perm, **kwargs)

    def generate_avatar(self):
        # Простая генерация картинки 200x200 со случайным фоном и буквой
        bg_color = random.choice([(74, 144, 226), (46, 204, 113), (155, 89, 182), (230, 126, 34)])
        img = Image.new('RGB', (200, 200), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Берем первую букву имени в верхнем регистре
        letter = self.name[0].upper() if self.name else "U"
        
        # Чтобы не усложнять со шрифтами, используем дефолтный или стандартный
        try:
            font = ImageFont.load_default()
        except IOError:
            font = None
            
        # Рисуем текст по центру (упрощенно)
        draw.text((90, 80), letter, fill="white", font=font)
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        return ContentFile(buffer.getvalue(), name=f'{self.email}_avatar.jpg')