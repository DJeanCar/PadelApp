from django.db import models

# class Equipo(models.Model):
# 	competicion = models.ForeignKey(Competicion)
# 	jugadores = models.ManyToManyField(Jugador, through = 'JugadorxEquipo')
# 	categoria = models.ForeignKey(Categoria,null=True)
# 	division = models.ForeignKey(Division,null=True)
# 	descripcion = models.CharField(max_length=50, null=False,blank=False)	
# 	preferencia_horaria = models.TextField(max_length=50,null=True,blank=True)
# 	nivel = models.IntegerField(null=True,blank=True)
# 	pagado = models.BooleanField(default=False)
# 	timpestamp = models.DateField(auto_now_add=True)
# 	activo = models.BooleanField(default=False)
# 	# campos adicionales que se pueden usar en la inscripcion del equipo de mas de 2 personas cuando se haga
# 	nombre_club = models.CharField(max_length=200, null=True)
# 	ubicacion_sede = models.CharField(max_length=200, null = True)
# 	localidad = models.CharField(max_length=100, null = True)
# 	dia_juego = models.CharField(max_length=10, null = True)
# 	hora_juego = models.CharField(max_length=5, null = True)


# class JugadorxEquipo(models.Model):
# 	jugador = models.ForeignKey(Jugador)
# 	equipo = models.ForeignKey(Equipo,related_name='Equipo(JugadorxEquipo)')
# 	capitan = models.BooleanField(default='False')
# 	activo = models.BooleanField(default='False') #false cuando se inscribe a un jugador que no es el mismo usuario y tiene cuenta en la aplicacion, true sera cuando lo confirme mediante el correo.
# 	lesionado = models.BooleanField(default=False)
# 	timpestamp = models.DateTimeField(auto_now=True)
