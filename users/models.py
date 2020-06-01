from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'), max_length=150, unique=True, help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_only.'), validators=[username_validator], error_messages={'unique': _("A user with that username already exists."),},)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    date_joined = models.DateTimeField('date_joined', default=timezone.now)
    student_id = models.CharField(max_length=7)
    gender_choice = (
        (0, '未選択'),
        (1, '男性'),
        (2, '女性'),
    )
    gender = models.IntegerField(choices=gender_choice, default=0, null=True)
    grade_choice = (
        (0, '未選択'),
        (1, '1年生'),
        (2, '2年生'),
        (3, '3年生'),
        (4, '4年生'),
        (5, '院生'),
        (6, '既卒'),
    )
    grade = models.IntegerField(choices=grade_choice, default=0, null=True)
    belong_university = models.CharField(max_length=100, default='沖縄国際大学')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['student_id']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
