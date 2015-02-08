from .models import Player, CommunicationOption, MediosComunication
from .functions import send_email

def create_player(strategy, details, response, is_new=False, user=None, *args, **kwargs):
	"""Update user details using data from provider."""
	if user and is_new:
		firstSurname, secondSurname = details['last_name'].split()
		Player.objects.create(user = user,
							  first_name = details['first_name'],
							  firstSurname = firstSurname,
							  secondSurname = secondSurname,
							  is_active = True)
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
		

def user_details(strategy, details, response, is_new=False, user=None, *args, **kwargs):
	"""Update user details using data from provider."""
	if user and is_new:
		changed = False  # flag to track changes
		protected = strategy.setting('PROTECTED_USER_FIELDS', [])
		keep = ('username', 'id', 'pk') + tuple(protected)

		for name, value in details.items():
			# do not update username, it was already generated
			# do not update configured fields if user already existed
			if name not in keep and hasattr(user, name):
				if value and value != getattr(user, name, None):
					try:
						setattr(user, name, value)
						changed = True
					except AttributeError:
						pass

		if changed:
			strategy.storage.user.changed(user)