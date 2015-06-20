from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, UpdateView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from random import choice
from braces.views import LoginRequiredMixin

from .forms import LoginForm, UserCreationForm, UserUpdateForm, EditPlayerForm
from .models import User, Player, CommunicationOption, MediosComunication
from .functions import Login, send_email

class HomeView(LoginRequiredMixin, TemplateView):

	template_name = 'users/EntradaUsuario.html'
	login_url = '/login/'

class LoginView(FormView):

	template_name = 'users/login.html'
	form_class = LoginForm
	success_url = reverse_lazy('home')

	def make_random_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
		return ''.join([choice(allowed_chars) for i in range(length)])

	def post(self, request, *args, **kwargs):
		if self.request.POST.get("email_recuperar"):
			try:
				usuario = User.objects.get(email=request.POST['email_recuperar'])
				password = self.make_random_password()
				# usuario.set_password(password)
				# usuario.save()
				# enviar_email_acceso(usuario.username,password,usuario.email) Falta el Email
				mensaje = "Hemos enviado tus datos de acceso a  %s" % request.POST['email_recuperar']
				form = LoginForm()
			except:
				mensaje = "Email %s no registrado" & request.POST['email_recuperar']
			return render(request,'users/login.html',{'mensaje' : mensaje, 'form' : form})
		else:
			Login(request, request.POST['email'], request.POST['password'])
		return super(LoginView, self).post(request, *args, **kwargs)

class RegisterUserView(FormView):

	template_name = 'users/CreacionCuenta.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('welcome')

	def form_valid(self, form):
		user = User.objects.create(username = form.cleaned_data['username'],
								email = form.cleaned_data['email'],
								password = form.cleaned_data['password'])
		user.set_password(form.cleaned_data['password'])
		user.save()
		Player.objects.create(user = user, first_name = form.cleaned_data['first_name'],
						firstSurname = form.cleaned_data['firstSurname'],
						secondSurname = form.cleaned_data['secondSurname'],
						birth_date = form.cleaned_data['birth_date'],
						phone = form.cleaned_data['phone'],
						is_active = True)
		if form.cleaned_data['notifications'] == 'on':
			CommunicationOption.objects.create(
						user = user,
						torneos_participando = True,
						resumen_resultados = True,
						nuevos_torneos = True
				)
		else:
			CommunicationOption.objects.create(
						user = user,
						torneos_participando = False,
						resumen_resultados = False,
						nuevos_torneos = False
				)
		MediosComunication.objects.create(
						user = user,
						email = True,
						sms = False,
						whatsapp = False
			)
		send_email(
				template = 'Bienvenida',
				# token = token,
				subject = 'Bienvenidos a Padel',
				email = user.email,
			)
		return super(RegisterUserView, self).form_valid(form)


class WelcomeView(LoginRequiredMixin, TemplateView):

	login_url = reverse_lazy('home')

	def get(self, request, *args, **kwargs):
		if request.user.welcome:
			return redirect(reverse('home'))
		else:
			request.user.welcome = True
			request.user.save()
			# Aqui falta enviar un mail
			return render(request, 'users/CreacionOK.html')

def Logout(request):
	logout(request)
	return redirect(reverse_lazy('home'))


class UserProfileView(LoginRequiredMixin, FormView):

	template_name = 'users/PerfilEdicion.html'
	login_url = reverse_lazy('home')
	form_class = UserUpdateForm
	success_url = reverse_lazy('user_profile')

	def get_context_data(self, **kwargs):
		context = super(UserProfileView, self).get_context_data(**kwargs)
		context['players'] = Player.objects.filter(is_active = False, user=self.request.user)
		player_active = Player.objects.get(user = self.request.user, is_active=True)
		context['lang'] = player_active.language
		if self.request.session.get('update'):
			context['update'] = True
			self.request.session['update'] = False
		return context

	def post(self, request, *args, **kwargs):
		form = UserUpdateForm(request.POST, request.FILES)
		dic = {
			'form' : form
		}
		if form.is_valid():
			# Usuario
			reset = False
			user = User.objects.get(email = request.user.email)
			if request.POST['username'] != request.user.username:
				if not User.objects.filter(username = request.POST['username']):
					user.username = request.POST['username']
				else:
					dic['username_error'] = "Este username ya existe"
			if request.POST['email'] != request.user.email:
				if not User.objects.filter(email = request.POST['email']):
					user.email = request.POST['email']
				else:
					dic['email_error'] = "Este email ya existe"
			if request.POST['password']:
				user.set_password(request.POST['password'])
				reset = True
				username = request.user.username
				password = request.POST['password']
			if request.FILES.get('image'):
				user.avatar = request.FILES['image']
			user.save()
			dic['user'] = user
			# Jugador activo
			player = Player.objects.get(user = request.user)
			player.first_name = request.POST['first_name']
			player.firstSurname = request.POST['firstSurname']
			player.secondSurname = request.POST['secondSurname']
			player.language = request.POST['language']
			dic["lang"] = player.language
			if request.POST['birth_date']:
				player.birth_date = request.POST['birth_date']
			if request.POST['phone']:
				player.phone = request.POST['phone']
			player.save()
			# Opciones de Comunicacion
			communication = CommunicationOption.objects.get(user = self.request.user)
			communication.torneos_participando = bool(request.POST.get('torneos_participando'))
			communication.resumen_resultados = bool(request.POST.get('resumen_resultados'))
			communication.nuevos_torneos = bool(request.POST.get('nuevos_torneos'))
			communication.save()
			# Medios
			medios = MediosComunication.objects.get(user = self.request.user)
			medios.email = bool(request.POST.get('email_com'))
			medios.sms = bool(request.POST.get('sms'))
			medios.whatsapp = bool(request.POST.get('whatsapp'))
			medios.save()
			dic["update"] = True
			if reset:
				logout(request)
				Login(request, username, password)
				request.session['update'] = True
				return redirect('/perfil/')
		return render(request, 'users/PerfilEdicion.html', dic)

	def get_initial(self):
		player_active = Player.objects.get(user = self.request.user, is_active=True)
		communication = CommunicationOption.objects.get(user = self.request.user)
		medios = MediosComunication.objects.get(user = self.request.user)
		data = {
			'username' : self.request.user.username,
			'image' : self.request.user.avatar,
			'first_name' : player_active.first_name,
			'firstSurname' : player_active.firstSurname,
			'secondSurname' : player_active.secondSurname,
			'birth_date' : player_active.birth_date,
			'phone' : player_active.phone,
			'email' : self.request.user.email,
			'torneos_participando' : communication.torneos_participando,
			'resumen_resultados' : communication.resumen_resultados,
			'nuevos_torneos' : communication.nuevos_torneos,
			'email_com' : medios.email,
			'sms' : medios.sms,
			'whatsapp' : medios.whatsapp
		}
		return data


class PlayerProfileView(LoginRequiredMixin, FormView):

	template_name = 'users/JugadoresAsociados.html'
	form_class = EditPlayerForm
	login_url = reverse_lazy('home')

	def get(self, request, *args, **kwargs):
		player = get_object_or_404(Player, pk = request.GET.get('jugador'))
		if player.user != request.user:
			raise Http404
		return super(PlayerProfileView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(PlayerProfileView, self).get_context_data(**kwargs)
		context['player'] = Player.objects.get(id = self.request.GET.get('jugador'))
		context['players'] = Player.objects.filter(is_active = False)
		return context

	def form_valid(self, form):
		player = get_object_or_404(Player, pk = self.request.GET.get('jugador'))
		form = EditPlayerForm(self.request.POST , instance=player)
		form.instance.user = self.request.user
		form.save()
		return super(PlayerProfileView, self).form_valid(form)

	def get_success_url(self):
		return '/perfil/jugador-asociado/?jugador=%s' % self.request.GET.get('jugador')

	def get_initial(self):
		player = Player.objects.get(pk = self.request.GET.get('jugador'))
		data = {
			'first_name' : player.first_name,
			'firstSurname' : player.firstSurname,
			'secondSurname' : player.secondSurname,
			'birth_date' : player.birth_date,
			'phone' : player.phone,
		}
		return data


class DeleteAccountView(LoginRequiredMixin, TemplateView):

	login_url = '/login/'

	def get(self, request, *args, **kwargs):
		if int(request.user.id) == int(request.GET['id']):
			logout(request)
			User.objects.get(id = request.GET['id']).delete()
			return '/login/'
		else:
			raise Http404