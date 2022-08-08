from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from PIL import Image
from django.conf import settings
import os
import time
from random import choice
from os.path import join as path_join
from os import listdir
from os.path import isfile


# Create your models here.
def user_directory_path(instance, filename):
    return 'accounts/user_{0}/{1}'.format(instance.username, filename)

# # Default Random Image
# def random_image():
#     # directory = os.path.join(settings.BASE_DIR, 'accounts/default_avatar')
#     directory = os.path.join(settings.BASE_DIR, 'static/accounts/default_avatar')
#     files = os.listdir(directory)
#     images = [file for file in files if os.path.isfile(os.path.join(directory, file))]
#     rand = choice(images)
#     return rand

def random_image():
    lst_arr = os.path.join(settings.BASE_DIR, 'static/accounts/default_avatar')
    print(lst_arr)
    return 'accounts/default_avatar/' + choice(lst_arr)

# def random_image():
#     dir_path = 'static/accounts/default_avatar'
#     files = [content for content in listdir(dir_path) if isfile(path_join(dir_path, content))]
#     return path_join(dir_path, choice(files))

class UserAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    USER_ROLE = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ]
    email       = models.EmailField(max_length=255, verbose_name="email address", unique=True)
    username    = models.CharField(max_length=150, verbose_name="Username", unique=True)
    first_name  = models.CharField(max_length=50, blank=True, null=True)
    last_name   = models.CharField(max_length=50, blank=True, null=True)
    picture     = models.FileField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')
    bio         = models.CharField(max_length=70, blank=True, null=True)
    about       = models.TextField(max_length=300, blank=True, null=True)
    is_staff    = models.BooleanField(default=True)
    role        = models.CharField(max_length=7, choices=USER_ROLE, default='student')
    is_active   = models.BooleanField(default=True)
    is_online   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    created_on  = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

class OnlineStatus(models.Model):
    ip                  = models.CharField(max_length=150, blank=True, null=True)
    is_member   = models.BooleanField(default=False)
    created_on   = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True, auto_now_add=False)
        
    class Meta:
        verbose_name_plural = "Online Status"

    def __str__(self):
        return f"{self.ip}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)
    instance.useraccount.save()