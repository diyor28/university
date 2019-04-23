from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)

        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin

        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_admin=True)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(default='123abc@gmail.com', max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class Grades(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(default='Subject', max_length=255)
    first_semester = models.CharField(default='-', max_length=30)
    second_semester = models.CharField(default='-', max_length=30)
    overall = models.CharField(default='-', max_length=30)


# class Subject(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     subject = models.CharField(default='Subject', max_length=255)
#     semester1 = models.CharField(default='-', max_length=30)
#     semester2 = models.CharField(default='-', max_length=30)
#     overall = models.CharField(default='-', max_length=30)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default/default.png', blank=True)

    def __str__(self):
        return self.user.email



