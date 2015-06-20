from django.db import models
from apps.torneos.models import Competicion, Categoria, Division, Nivel
from apps.users.models import Player

class Equipo(models.Model):
	competicion = models.ForeignKey(Competicion)
	jugadores = models.ManyToManyField(Player, through = 'JugadorxEquipo')
	categoria = models.ForeignKey(Categoria,null=True)
	division = models.ForeignKey(Division,null=True)
	descripcion = models.CharField(max_length=50, null=False,blank=False)	
	preferencia_horaria = models.TextField(max_length=50,null=True,blank=True)
	nivel = models.ForeignKey(Nivel, null=True,blank=True) # Cambiado antes era un IntergerField
	pagado = models.BooleanField(default=False)
	timpestamp = models.DateField(auto_now_add=True)
	activo = models.BooleanField(default=False)
	# campos adicionales que se pueden usar en la inscripcion del equipo de mas de 2 personas cuando se haga
	nombre_club = models.CharField(max_length=200, null=True)
	ubicacion_sede = models.CharField(max_length=200, null = True)
	localidad = models.CharField(max_length=100, null = True)
	dia_juego = models.CharField(max_length=10, null = True)
	hora_juego = models.CharField(max_length=5, null = True)

	def __unicode__(self):
		return "%s" % (self.jugadores.all())


class JugadorxEquipo(models.Model):
	jugador = models.ForeignKey(Player)
	equipo = models.ForeignKey(Equipo)
	capitan = models.BooleanField(default='False')
	activo = models.BooleanField(default='False') #false cuando se inscribe a un jugador que no es el mismo usuario y tiene cuenta en la aplicacion, true sera cuando lo confirme mediante el correo.
	lesionado = models.BooleanField(default=False)
	timpestamp = models.DateTimeField(auto_now=True)