from django.conf.urls import patterns, url

from .views import CreateTorneoView, EditarTorneoView, TorneoListView

urlpatterns = patterns('',
	url(r'^crear-torneo/$', CreateTorneoView.as_view(), name="create_torneo"),

	url(r'^editar-torneo/$', TorneoListView.as_view(), name="edit_torneo"),
	url(r'^editar-torneo/(?P<slug>[-\w]+)/', EditarTorneoView.as_view(), name="editar_torneo"),

	#AJAX
	url(r'^crear-divisiones-ajax/$', 'apps.torneos.views.crear_division'),
	url(r'^tipo-competicion/$', 'apps.torneos.views.tipo_competicion'),
)
