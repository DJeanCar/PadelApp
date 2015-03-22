from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin

from apps.users.models import Player
from .models import TipoCompeticion, ClasificacionCategoria_Categoria, DatosTipoCompeticion,ClasificacionNivel, Nivel, Competicion
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
		if form.cleaned_data.get('ClasificacionNivel'):
			clasificacionNivel = form.cleaned_data.get('ClasificacionNivel')
		else:
			# Aqui tengo que guardar los niveles creados por el usuario
			clasificacionNivel = ClasificacionNivel.objects.create(
					user = self.request.user,
					name = self.request.POST['levelClassificationName']
				)
			for i in range(1,10):
				if "levelName_%s" % i in self.request.POST:
					try:
						nivel = Nivel.objects.get(name__iexact = self.request.POST['levelName_%s' % i])
					except:
						Nivel.objects.create(name = self.request.POST['levelName_%s' % i])
		competicion = Competicion.objects.create(
				# categoria = , Este campo faltaa!!!
				admin = Player.objects.get(user = self.request.user),
				tipoCompeticion = form.cleaned_data['tournamentType'],
				tipoInscripcion = form.cleaned_data['tipoInscripcion'],
				clasificacionNivel = clasificacionNivel,
				name = form.cleaned_data['name'],
				urlTag = form.cleaned_data['urlTag'],
				logo = form.cleaned_data['logo'],
				fecha_inicio = form.cleaned_data['fecha_inicio'],
				fecha_fin = form.cleaned_data['fecha_fin'],
				price = form.cleaned_data['price']
			)
		#El de abajo si funca
		DatosTipoCompeticion.objects.create(
				tipoCompeticion = form.cleaned_data['tournamentType'],
				competicion = competicion,
				min_jugadores = form.cleaned_data['min_jugadores'],
				max_jugadores = form.cleaned_data['max_jugadores'],
				min_equipos = form.cleaned_data['min_equipos'],
				max_equipos = form.cleaned_data['max_equipos'],
				num_cuenta = form.cleaned_data['num_cuenta'],
				fecha_sustitucion = form.cleaned_data['fecha_sustitucion'],
				fecha_limite = form.cleaned_data['fecha_limite'],
				preferencia_horaria = self.request.POST['timePreference']
			)
		return super(CreateTorneoView, self).form_valid(form)

	def form_invalid(self, form):
		print form.errors
		return super(CreateTorneoView, self).form_invalid(form)

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