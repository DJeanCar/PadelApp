from django.conf.urls import patterns, url

from .views import CreateTorneoView

urlpatterns = patterns('',
	url(r'^crear-torneo/$', CreateTorneoView.as_view()),
)
