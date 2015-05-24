import json
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from braces.views import LoginRequiredMixin

from apps.torneos.models import Competicion, ClasificacionCategoria_Categoria, Division, ClasificacionNivel_Nivel, Categoria, Nivel
from apps.users.models import User, Player, CommunicationOption
from .models import Equipo, JugadorxEquipo


class InscripcionTorneo(DetailView):

	model = Competicion
	slug_field = 'urlTag'
	template_name = 'inscriptions/RegistroPareja.html'

	def get_context_data(self, **kwargs):
		context = super(InscripcionTorneo, self).get_context_data(**kwargs)
		context['categorias'] = ClasificacionCategoria_Categoria.objects.filter(clas_cat = self.get_object().categoria)
		context['divisiones'] = Division.objects.filter(competicion = self.get_object())
		context['niveles'] = ClasificacionNivel_Nivel.objects.filter(clas_niv = self.get_object().clasificacionNivel)
		if self.request.GET.get('error') == 'True':
			context['error'] = "Las credenciales del usuario son incorrectas"
		if self.request.GET.get('error') == 'username':
			context['error'] = "El username ya existe"
		if self.request.GET.get('error') == 'email':
			context['error'] = "El email ya existe"
		if self.request.GET.get('error') == 'password':
			context['error'] = "Los password no son iguales"
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			if User.objects.filter(username = request.POST['username']).exists():
				# Error en el username
				return redirect('/inscripcion/%s/?error=username' % request.POST['slug'])
			if User.objects.filter(email = request.POST['email']).exists():
				# Error en el email
				return redirect('/inscripcion/%s/?error=email' % request.POST['slug'])
			if not request.POST['password'] == request.POST['repeatPassword']:
				# Error en los password
				return redirect('/inscripcion/%s/?error=password' % request.POST['slug'])
			######### Aqui esta mall!! :/
			user = User.objects.create(
					username = request.POST['username'],
					email = request.POST['email'],
					password = request.POST['password']
				)
			user.set_password(user.password)
			user.save()
			player = Player.objects.create(
				user = user,
				first_name = request.POST['name'],
				firstSurname = request.POST['surname1'],
				secondSurname = request.POST['surname2'],
				birth_date = request.POST['birthdate'],
				phone = request.POST['phone'],
				is_active = True
			)
		else:
			user = request.user
		if 'notifications' in request.POST:
			CommunicationOption.objects.create(
					user = user,
					torneos_participando = True,
					resumen_resultados = True,
					nuevos_torneos = True
				)
		else:
			CommunicationOption.objects.create(
					user = user
				)
		equipo = Equipo.objects.create(
				competicion = Competicion.objects.get(id = request.POST['id_competicion']),
				categoria = Categoria.objects.get(id = request.POST['category']),
				division = Division.objects.get(id = request.POST['division']),
				preferencia_horaria = request.POST['timePreference'],
				nivel = Nivel.objects.get(id = request.POST['level']),
			)
		if not Player.objects.filter(email = request.POST['memberEmail_2_1']).exists():
			player = Player.objects.create(
					user = user,
					first_name = request.POST['memberName_2_1'],
					firstSurname = request.POST['memberSurname1_2_1'],
					secondSurname = request.POST['memberSurname2_2_1'],
					email = request.POST['memberEmail_2_1']
				)
		else:
			player = Player.objects.get(email = request.POST['memberEmail_2_1'])
		JugadorxEquipo.objects.create(
				jugador = player,
				equipo = equipo,
			)
		return redirect('/inscrito/')

class UserInscription(TemplateView):

	def post(self, request, *args, **kwargs):
		user = User.objects.filter(username = request.POST['username']).exists()
		if not user:
			return redirect('/inscripcion/%s/?error=True' % request.POST['slug'])
		user = User.objects.get(username = request.POST['username'])
		if not user.check_password(request.POST['password']):
			return redirect('/inscripcion/%s/?error=True' % request.POST['slug'])
		equipo = Equipo.objects.create(
				competicion = Competicion.objects.get(id = request.POST['id_competicion']),
				categoria = Categoria.objects.get(id = request.POST['category']),
				division = Division.objects.get(id = request.POST['division']),
				preferencia_horaria = request.POST['timePreference'],
				nivel = Nivel.objects.get(id = request.POST['level']),
			)
		if not Player.objects.filter(email = request.POST['memberEmail_1_1']).exists():
			player = Player.objects.create(
					user = user,
					first_name = request.POST['memberName_1_1'],
					firstSurname = request.POST['memberSurname1_1_1'],
					secondSurname = request.POST['memberSurname2_1_1'],
					email = request.POST['memberEmail_1_1']
				)
		else:
			player = Player.objects.get(email = request.POST['memberEmail_1_1'])
		JugadorxEquipo.objects.create(
				jugador = player,
				equipo = equipo,
			)
		return redirect('/inscrito/')

class InscritoFelicidades(TemplateView):

	template_name = 'inscriptions/inscripcionOK.html'


class GetDivision(TemplateView):

	def get(self, request, *args, **kwargs):
		divisiones = Division.objects.filter(categoria__id = request.GET['cat_id'])
		data = serializers.serialize('json', divisiones)
		return HttpResponse(data, content_type="application/json")