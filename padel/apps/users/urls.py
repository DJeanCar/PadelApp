from django.conf.urls import patterns, url

from .views import LoginView, RegisterUserView, WelcomeView, HomeView, UserProfileView,PlayerProfileView

urlpatterns = patterns('',
	url(r'^$', HomeView.as_view(), name="home"),
	url(r'^login/$', LoginView.as_view(), name="login"),
	url(r'^perfil/$', UserProfileView.as_view(), name='user_profile'),
	url(r'^perfil/jugador-asociado/$', PlayerProfileView.as_view(), name='player_profile'),
	url(r'^registrar/$', RegisterUserView.as_view(), name="register_user"),
	url(r'^bienvenido/$', WelcomeView.as_view(), name="welcome"),
	url(r'^salir/$', 'apps.users.views.Logout', name="logout"),
)
