from django.shortcuts import render
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin

from .models import TipoCompeticion
from .forms import CrearTorneoForm

class CreateTorneoView(LoginRequiredMixin, FormView):

	template_name = 'torneos/CreacionTorneo.html'
	login_url = reverse_lazy('home')
	form_class = CrearTorneoForm
	success_url = reverse_lazy('create_torneo')

	def get_context_data(self, **kwargs):
		context = super(CreateTorneoView, self).get_context_data(**kwargs)
		context['tipocompeticion'] = TipoCompeticion.objects.all()
		return context

	def form_valid(self, form):
		print form.cleaned_data
		return super(CreateTorneoView, self).form_valid(form)
