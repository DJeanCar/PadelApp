from django.db import models
from django.template.defaultfilters import slugify

from apps.users.models import Player, User


class Categoria(models.Model):

	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class ClasificacionCategoria(models.Model):

	user = models.ForeignKey(User) # Uusuario que lo ha creado
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class ClasificacionCategoria_Categoria(models.Model):

	clas_cat = models.ForeignKey(ClasificacionCategoria)
	category = models.ForeignKey(Categoria)
	orden = models.IntegerField()

	def __unicode__(self):
		return self.category.name

class Nivel(models.Model):

	name = models.CharField(max_length=50) # Alto , Medio, Bajo

	def __unicode__(self):
		return self.name

class ClasificacionNivel(models.Model):

	user = models.ForeignKey(User) # Uusuario que lo ha creado
	name = models.CharField(max_length=100) # Alto/Medio/Bajo

	def __unicode__(self):
		return self.name

class ClasificacionNivel_Nivel(models.Model):

	clas_niv = models.ForeignKey(ClasificacionNivel)
	nivel = models.ForeignKey(Nivel)
	orden = models.IntegerField()

	def __unicode__(self):
		return self.clas_niv.name



class TipoCompeticion(models.Model):

	name = models.CharField(max_length=100, null=False,blank=False)
	slug = models.SlugField()

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		'''
		Esta funcion nos ayuda a guardar el slug de acuerdo al titulo.
		'''
		if not self.id:
			self.slug = slugify(self.name)
		super(TipoCompeticion, self).save(*args, **kwargs)


class TipoInscripcion(models.Model):

	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name
		

class Competicion(models.Model):
	"""
		Logo y precio ( agregar ), permitir_nivel, permitir_division
	"""
	categoria = models.ForeignKey(ClasificacionCategoria)
	admin = models.ForeignKey(Player) # administrador del torneo
	tipoCompeticion = models.ForeignKey(TipoCompeticion) # tipo de competicion
	tipoInscripcion = models.ForeignKey(TipoInscripcion)
	clasificacionNivel = models.ForeignKey(ClasificacionNivel)
	
	name = models.CharField(max_length=50) # descripcion
	urlTag = models.CharField(max_length=50,unique=True) # url corta
	
	logo = models.ImageField(upload_to = 'competicion')	
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	
	price = models.FloatField()
	estado = models.BooleanField(default=True)
	
	nivel_bool = models.BooleanField(default = False)
	division_bool = models.BooleanField(default = False)

	def __unicode__(self):
		return self.name

class DatosTipoCompeticion(models.Model):

	tipoCompeticion = models.ForeignKey(TipoCompeticion)
	competicion = models.ForeignKey(Competicion)
	min_jugadores = models.IntegerField(null=True, blank=True)
	max_jugadores = models.IntegerField(null=True, blank=True)
	min_equipos = models.IntegerField(null=True, blank=True)
	max_equipos = models.IntegerField(null=True, blank=True)
	num_cuenta = models.CharField(max_length=100, null=True, blank=True)
	fecha_sustitucion = models.DateField(null=True, blank=True)
	fecha_limite = models.DateField(null=True, blank=True)
	preferencia_horaria = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.tipoCompeticion.name


class Division(models.Model):
	categoria = models.ForeignKey(Categoria)
	competicion = models.ForeignKey(Competicion)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name
