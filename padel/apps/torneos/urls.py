from django.conf.urls import patterns, url

from .views import CreateTorneoView

urlpatterns = patterns('',
	url(r'^crear-torneo/$', CreateTorneoView.as_view(), name="create_torneo"),

	

	#AJAX
	url(r'^crear-divisiones-ajax/$', 'apps.torneos.views.crear_division'),
	url(r'^tipo-competicion/$', 'apps.torneos.views.tipo_competicion'),
)
