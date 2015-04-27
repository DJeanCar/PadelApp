from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView

from apps.torneos.models import Competicion
from apps.users.models import User

class InscripcionTorneo(DetailView):

	model = Competicion
	slug_field = 'urlTag'
	template_name = 'inscriptions/RegistroPareja.html'

	def get_context_data(self, **kwargs):
		context = super(InscripcionTorneo, self).get_context_data(**kwargs)
		if self.request.GET.get('error') == 'True':
			context['error'] = "Las credenciales del usuario son incorrectas"
		return context


class UserInscription(TemplateView):

	def post(self, request, *args, **kwargs):
		user = User.objects.filter(username = request.POST['username']).exists()
		if not user:
			return redirect('/inscripcion/%s/?error=True' % request.POST['slug'])
		user = User.objects.get(username = request.POST['username'])
		if not user.check_password(request.POST['password']):
			return redirect('/inscripcion/%s/?error=True' % request.POST['slug'])
			