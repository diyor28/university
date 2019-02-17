from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    # email = models.EmailField(default='123abc@gmail.com', max_length=255)
    # USERNAME_FIELD = 'email'
    objects = CustomUserManager()


class Grades(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    chemistry = models.CharField(default='-', max_length=255)
    math = models.CharField(default='-', max_length=255)
    physics = models.CharField(default='-', max_length=255)
    geography = models.CharField(default='-', max_length=255)
    english = models.CharField(default='-', max_length=255)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.email