from django.db import models
from django.contrib.auth.models import (
    User, AbstractBaseUser, BaseUserManager
)
from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, password, first_name="", last_name="", email="email.email@email.com", bio="", profilo_pubblico=False, is_staff=False, is_admin=False, active=True):
        if not password or not username:
            raise ValueError("Devi inserire sia username che password")
        user_obj = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            bio=bio,
            profilo_pubblico=profilo_pubblico,
            is_active=True,
            is_admin=is_admin,
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj
        
    def create_superuser(self, username, password, email):
        user_obj = self.create_user(
            username,
            password,
            email=email,
            is_admin=True
        )
        user_obj.is_active=True
        return user_obj


class Autore(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    data_registrazione = models.DateField(default=datetime.date.today, editable=False)
    bio = models.TextField(blank=True)
    profilo_pubblico = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    #staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_id(self):
        return self.get_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username + ", " + self.first_name + " " + self.last_name  
    
    class Meta: 
        get_latest_by  = ['first_name', 'last_name']
        verbose_name_plural = 'Autori'
"""
class Autore(models.Model):
    user = models.OneToOneField(MyUser, primary_key=True, on_delete=models.CASCADE)
    data_registrazione = models.DateField(default=datetime.date.today, editable=False)
    bio = models.TextField(blank=True)
    profilo_pubblico = models.BooleanField(default=False)

    class Meta:
        get_latest_by  = ['-self.user.first_name', '-self.user.last_name']
        verbose_name_plural = 'Autori'

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ", " + self.user.username

User.profile = property(lambda u: Autore.objects.get_or_create(user=u)[0])
""" 

