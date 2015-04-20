from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.views.generic import FormView, TemplateView, DetailView
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin

from apps.users.models import Player
from .models import TipoCompeticion, ClasificacionCategoria_Categoria, DatosTipoCompeticion,ClasificacionNivel, Nivel, Competicion, Categoria, ClasificacionCategoria,Division, TipoInscripcion
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
		################# Nivel 
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
				else:
					break
		###########################
		####################CATEGORIA
		if form.cleaned_data.get('categoryClassification'):
			clasificacionCategoria = form.cleaned_data.get('categoryClassification')
		else:
			clasificacionCategoria = ClasificacionCategoria.objects.create(
					user = self.request.user,
					name = self.request.POST['categoryClassificationName']
				)
			for i in range(1,10):
				if "categoryName_%s" % i in self.request.POST:
					try:
						categoria = Categoria.objects.get(name__iexact = self.request.POST['categoryName_%s' % i])
					except:
						categoria = Categoria.objects.create(name = self.request.POST['categoryName_%s' % i])
					ClasificacionCategoria_Categoria.objects.create(
							clas_cat = clasificacionCategoria,
							category = categoria,
							orden = i
						)
				else:
					break
		########################
		competicion = Competicion.objects.create(
				categoria = clasificacionCategoria,
				admin = Player.objects.get(user = self.request.user),
				tipoCompeticion = form.cleaned_data['tournamentType'],
				tipoInscripcion = form.cleaned_data['tipoInscripcion'],
				clasificacionNivel = clasificacionNivel,
				name = form.cleaned_data['name'],
				urlTag = form.cleaned_data['urlTag'],
				logo = form.cleaned_data['logo'],
				fecha_inicio = form.cleaned_data['fecha_inicio'],
				fecha_fin = form.cleaned_data['fecha_fin'],
				price = form.cleaned_data['price'],
				division_bool = form.cleaned_data['division_bool'],
				nivel_bool = form.cleaned_data['nivel_bool']
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
		##################DIVISIONES
		clas_orden = ClasificacionCategoria_Categoria.objects.filter(clas_cat = clasificacionCategoria).order_by('orden')
		if "div-1Name_1" in self.request.POST:
			# Aqui se hacen las divisiones
			for clas in clas_orden:
				if "div-%sName_1" % clas.orden in self.request.POST:
					for i in range(1,10):
						if "div-%sName_%s" % (clas.orden, i) in self.request.POST:
							Division.objects.create(
									categoria = clas.category,
									competicion = competicion,
									name = self.request.POST["div-%sName_%s" % (clas.orden, i)]
								)
						else:
							break
					# Aqui hay que hacer otro for para las divisiones de cada categoria
		#################################
		return super(CreateTorneoView, self).form_valid(form)

	def form_invalid(self, form):
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


class TorneoListView(TemplateView):

	template_name = 'torneos/GestionTorneo.html'

	def get_context_data(self, **kwargs):
		context = super(TorneoListView, self).get_context_data(**kwargs)
		context['torneos'] = Competicion.objects.filter(admin = self.request.user)
		return context

class EditarTorneoView(DetailView):

	template_name = 'torneos/GestionTorneo.html'
	model = Competicion
	slug_field = "urlTag"

	def get_context_data(self, **kwargs):
		context = super(EditarTorneoView, self).get_context_data(**kwargs)
		context['torneos'] = Competicion.objects.filter(admin = self.request.user)
		context['slug'] = self.get_object().urlTag
		context['datosCompeticion'] = DatosTipoCompeticion.objects.get(competicion=self.get_object())
		context['categories'] = ClasificacionCategoria.objects.all()
		context['divisiones'] = ClasificacionNivel.objects.all()
		context['tipoInscripcion'] = TipoInscripcion.objects.all()
		context['price'] = str(self.get_object().price).replace("," , ".")
		return context

	def post(self, request, *args, **kwargs):
		competicion = self.get_object()
		datos_competicion = DatosTipoCompeticion.objects.get(competicion = competicion)
		if Competicion.objects.filter(urlTag = request.POST['url']).exists():
			if not request.POST['url'] == competicion.urlTag:
				dic = {
					'torneos' : Competicion.objects.filter(admin = self.request.user),
					'slug' : self.get_object().urlTag,
					'datosCompeticion' : DatosTipoCompeticion.objects.get(competicion=self.get_object()),
					'categories' : ClasificacionCategoria.objects.all(),
					'divisiones' : ClasificacionNivel.objects.all(),
					'tipoInscripcion' : TipoInscripcion.objects.all(),
					'price' : str(self.get_object().price).replace("," , "."),
					'object' : self.get_object(),
					'error' : "Ya existe la URL %s" % request.POST['url']
				}
				return render(request, 'torneos/GestionTorneo.html', dic)
		competicion.urlTag = request.POST['url']
		competicion.name = request.POST['name']
		competicion.fecha_inicio = request.POST['initDate']
		competicion.fecha_fin = request.POST['endDate']
		competicion.tipoInscripcion = TipoInscripcion.objects.get(id = request.POST['inscriptionType'])
		competicion.price = request.POST['priceLiga']
		if 'includeLevel' in request.POST:
			competicion.nivel_bool = request.POST['includeLevel']
		else:
			competicion.nivel_bool = False
		if 'includeDivision' in request.POST:
			competicion.division_bool = request.POST['includeDivision']
		else:
			competicion.division_bool = False
		if 'logoLiga' in request.POST:
			competicion.logo = request.POST['logoLiga']

		################# Datos Competicion
		datos_competicion.min_jugadores = request.POST['minPlayersLiga']
		datos_competicion.max_jugadores = request.POST['maxPlayersLiga']
		datos_competicion.min_equipos = request.POST['minTeamsLiga']
		datos_competicion.max_equipos = request.POST['maxTeamsLiga']
		datos_competicion.num_cuenta = request.POST['accountLiga']
		datos_competicion.fecha_sustitucion = request.POST['substitutionDateLiga']
		datos_competicion.fecha_limite = request.POST['inscriptionLimitDateLiga']
		datos_competicion.preferencia_horaria = request.POST['timePreferenceLiga']
		datos_competicion.save()
		################# Nivel 
		if request.POST.get('levelClassification'):
			clasificacionNivel = request.POST.get('levelClassification')
			competicion.clasificacionNivel = ClasificacionNivel.objects.get(id = clasificacionNivel)
			competicion.save()
		else:
			# Falta Probar esto
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
				else:
					break
		###########################
		####################CATEGORIA
		if request.POST.get('categoryClassification'):
			clasificacionCategoria = request.POST.get('categoryClassification')
			competicion.categoria = ClasificacionCategoria.objects.get(id = clasificacionCategoria)
			competicion.save()
		else:
			#Falta probar esto
			clasificacionCategoria = ClasificacionCategoria.objects.create(
					user = self.request.user,
					name = self.request.POST['categoryClassificationName']
				)
			for i in range(1,10):
				if "categoryName_%s" % i in self.request.POST:
					try:
						categoria = Categoria.objects.get(name__iexact = self.request.POST['categoryName_%s' % i])
					except:
						categoria = Categoria.objects.create(name = self.request.POST['categoryName_%s' % i])
					ClasificacionCategoria_Categoria.objects.create(
							clas_cat = clasificacionCategoria,
							category = categoria,
							orden = i
						)
				else:
					break
		########################
		return redirect('/editar-torneo/%s/' % competicion.urlTag)