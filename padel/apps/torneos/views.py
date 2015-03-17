from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin

from .models import TipoCompeticion, ClasificacionCategoria_Categoria
from .forms import CrearTorneoForm

class CreateTorneoView(LoginRequiredMixin, FormView):

	template_name = 'torneos/CreacionTorneo2.html'
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

	def form_invalid(self, form):
		print "asdas"
		print form.errors
		return super(CreateTorneoView, self).form_invalid(form)

	def get_initial(self):
		from .models import ClasificacionCategoria
		category = ClasificacionCategoria.objects.all()
		print category
		print category[0].id
		dic = {
				'tournamentType' : [cat.id for cat in category]
		}
		return dic

def crear_division(request):
	if request.is_ajax():
		divisiones = ClasificacionCategoria_Categoria.objects.values('category__name').filter(clas_cat__id = request.GET['id']).order_by('orden')
		lista_divisiones = []
		for a in divisiones:
			lista_divisiones.append(a['category__name'])
		return JsonResponse({'lista_divisiones' : lista_divisiones})
	else:
		raise Http404

def tipo_competicion(request):
	if request.is_ajax():
		slug_competicion = request.GET['slug_competicion']
		return JsonResponse({'tipo_competicion' : slug_competicion})
	else:
		raise Http404