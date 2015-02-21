from django.shortcuts import render
from django.views.generic import TemplateView

class CreateTorneoView(TemplateView):

	template_name = 'torneos/CreacionTorneo.html'