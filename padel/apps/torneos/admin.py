from django.contrib import admin
from .models import Categoria, TipoCompeticion, Competicion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	pass

@admin.register(TipoCompeticion)
class TipoCompeticionAdmin(admin.ModelAdmin):
	pass

@admin.register(Competicion)
class CompeticionAdmin(admin.ModelAdmin):
	pass