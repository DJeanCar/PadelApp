from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Player, CommunicationOption, MediosComunication

@admin.register(User)
class UserAdmin(UserAdmin):
	"""
		Administrador del Modelo de Usuarios
	"""
	list_display = ('username', 'email', 'created', 'modified')
	list_filter = ("is_superuser", "groups")
	search_fields = ("email", "username")
	ordering = ("username",)
	filter_horizontal = ("groups", "user_permissions")
	fieldsets = (
		('User', {"fields": ("username", "password")}),
		("Personal info", {"fields": ("username", "email", "avatar","confirmation_code")}),
		("Permissions", {"fields": ("is_active",
									"is_staff",
									"is_superuser",
									"groups",
									"user_permissions")}),
	)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	pass

@admin.register(CommunicationOption)
class PlayerAdmin(admin.ModelAdmin):
	pass

@admin.register(MediosComunication)
class PlayerAdmin(admin.ModelAdmin):
	pass