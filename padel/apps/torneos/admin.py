from django.contrib import admin
from .models import Categoria, TipoCompeticion, Competicion, ClasificacionCategoria, ClasificacionCategoria_Categoria, TipoInscripcion


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