from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
	url(r'^inscripcion/(?P<slug>[-\w]+)/$', views.InscripcionTorneo.as_view()),
	url(r'^inscribir-torneo/$', views.UserInscription.as_view()),


)
