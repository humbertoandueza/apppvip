from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Correo Electronico'), unique=True)
    first_name = models.CharField(_('Nombre'), max_length=30, blank=True)
    last_name = models.CharField(_('Apellido'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Activo'), default=True)
    is_superuser = models.BooleanField(_('Superusuario'), default=False)
    is_administrador = models.BooleanField(_('Administrador'), default=False)
    is_programador = models.BooleanField(_('Programador'), default=False)
    is_iglesia = models.BooleanField(_('Iglesia'), default=False)

    is_staff = models.BooleanField(_('Staff'), default=True)



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class Notificacion(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contenido = models.CharField(max_length=450,verbose_name="Contenido de la notificacion")
    date = models.DateField(auto_now_add=True)
    est = (
        ('organizacion','organizacion'),
        ('programador','programador'),
        )
    tipo = models.CharField(max_length=200,choices=est)
    url = models.CharField(max_length=200,verbose_name="link a redireccionar",null=True)
    estatus = models.CharField(max_length=20,default="No leida")

    def __str__(self):
        return self.user.first_name