from django.contrib import admin
from .models import *


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(TipoCompeticion)
class TipoCompeticionAdmin(admin.ModelAdmin):
	pass

@admin.register(Competicion)
class CompeticionAdmin(admin.ModelAdmin):
	pass

@admin.register(ClasificacionCategoria)
class ClasificacionCategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(ClasificacionCategoria_Categoria)
class ClasificacionCategoria_CategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(TipoInscripcion)
class TipoInscripcionAdmin(admin.ModelAdmin):
	pass

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
	pass

@admin.register(ClasificacionNivel)
class ClasificacionNivelAdmin(admin.ModelAdmin):
	pass

@admin.register(ClasificacionNivel_Nivel)
class ClasificacionNivel_NivelAdmin(admin.ModelAdmin):
	pass

@admin.register(DatosTipoCompeticion)
class DatosTipoCompeticionAdmin(admin.ModelAdmin):
	pass