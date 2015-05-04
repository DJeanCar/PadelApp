#encoding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager, models.Manager):

	def _create_user(self, username, email, password, is_staff,
				is_superuser, **extra_fields):

		email = self.normalize_email(email)
		if not email:
			raise ValueError('El email debe ser obligatorio')
		user = self.model(username = username, email=email, is_active=True,
				is_staff = is_staff, is_superuser = is_superuser, **extra_fields)
		user.set_password(password)
		user.save( using = self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		return self._create_user(username, email, password, False,
				False, **extra_fields)

	def create_superuser(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password, True,
				True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

	username = models.CharField(max_length=100, unique=True)
	email = models.EmailField(unique=True)
	avatar = models.ImageField(upload_to="users", blank=True, null=True)
	confirmation_code = models.CharField(max_length=250,blank=True, null=True)
	welcome = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = UserManager()

	def get_short_name(self):
		return self.username


class Player(models.Model):

	languages = (
			('es', 'Español'),
			('en', 'Ingles')
		)

	user = models.ForeignKey(settings.AUTH_USER_MODEL)   
	first_name = models.CharField(max_length=250)
	firstSurname = models.CharField(max_length=250)
	secondSurname = models.CharField(max_length=250)
	birth_date = models.DateField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True) # Agregado
	phone = models.BigIntegerField(null=True, blank=True)
	edad = models.IntegerField(null=True, blank=True)
	language = models.CharField(max_length=50 ,null=True, blank=True,choices = languages)

	is_active = models.BooleanField(default=False)

	def __unicode__(self):
		return self.first_name


class CommunicationOption(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	torneos_participando = models.BooleanField(default = False)
	resumen_resultados = models.BooleanField(default = False)
	nuevos_torneos = models.BooleanField(default = False)

	def __unicode__(self):
		return self.user.username

class MediosComunication(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	email = models.BooleanField(default = False)
	sms = models.BooleanField(default = False)
	whatsapp = models.BooleanField(default = False)

	def __unicode__(self):
		return self.user.username