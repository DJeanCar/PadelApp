#encoding=utf-8
from django import forms
from .models import User, Player


class LoginForm(forms.Form):

	email = forms.CharField(max_length=30, 
				widget = forms.TextInput(attrs = {
					'type' : 'email',
					'class' : 'form-control upperControl',
					'placeholder' : 'Email',
					'required' : 'True'
					}))
	password = forms.CharField(max_length=30,
	 			widget = forms.TextInput(attrs = {
	 				'type' : 'password',
	 				'class' : 'form-control lowerControl',
	 				'placeholder' : 'Contraseña',
	 				'required' : 'True'
	 				}))

	def clean(self):
		if self.cleaned_data.get("email") and self.cleaned_data.get("password"):
			email = self.cleaned_data.get("email")
			email_exist = User.objects.filter(email = email).exists()
			if email_exist:
				user = User.objects.get(email = email)
				if not user.check_password(self.cleaned_data.get("password")):
					self.add_error('password', 'Email y/o contraseña incorrectas')
			else:
				self.add_error('password', 'Email y/o contraseña incorrectas')


class UserCreationForm(forms.ModelForm):

	password2 = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'repeatPassword',
		 				'type' : 'password',
		 				'class' : 'form-control',
		 				'placeholder' : 'Repite la contraseña'
		 				}))
	cond = forms.CharField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	first_name = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'name',
		 				'class' : 'form-control',
		 				'placeholder' : 'Nombre'
		 				}))
	firstSurname = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'firstSurname',
		 				'class' : 'form-control',
		 				'placeholder' : 'Primer apellido'
		 				}))
	secondSurname = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'secondSurname',
		 				'class' : 'form-control',
		 				'placeholder' : 'Segundo apellido'
		 				}))
	birth_date = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'birthdate',
		 				'class' : 'form-control',
		 				'placeholder' : 'dd/mm/aaaa',
		 				'type' : 'date'
		 				}))
	phone = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'phone',
		 				'class' : 'form-control',
		 				'placeholder' : 'Teléfono',
		 				'type' : 'tel'
		 				}))
	notifications = forms.CharField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'notifications',
		 				'type' : 'checkbox'
		 				}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		widgets = {
			'username' : forms.TextInput(attrs={
					'id' : 'username',
					'class' : 'form-control',
					'placeholder': 'Elige tu identificador'
				}),
			'email' : forms.TextInput(attrs={
					'id' : 'email',
					'class' : 'form-control',
					'placeholder': 'Dirección de correo electrónico',
					'type' : 'email'
				}),
			'password' : forms.TextInput(attrs={
					'id' : 'password',
					'class' : 'form-control',
					'type' : 'password',
					'placeholder': 'Contraseña'
				})
		}

	def clean(self):
		cond = self.cleaned_data.get("cond")
		if cond != 'on':
			self.add_error('cond', 'Tiene que acerptar los terminos y condiciones')

		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password != password2:
			self.add_error('password', 'Las contraseñas no coinciden')

		email = self.cleaned_data.get("email")
		if User.objects.filter(email = email).exists():
			self.add_error('email', 'Este email ya existe')

		username = self.cleaned_data.get("username")
		if User.objects.filter(username = username).exists():
			self.add_error('username', 'Este username ya existe')


class UserUpdateForm(forms.Form):

	username = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'username',
		 				'class' : 'form-control',
		 				'placeholder' : 'Elige tu identificador'
		 				}))
	email = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'email',
		 				'class' : 'form-control',
		 				'placeholder' : 'Dirección de correo electrónico',
		 				'type' : 'email'
		 				}))
	image = forms.ImageField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'profileImg',
		 				'class' : 'form-control',
		 				'type' : 'file'
		 				}))
	password = forms.CharField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'Password',
		 				'type' : 'password',
		 				'class' : 'form-control',
		 				'placeholder' : 'Contraseña'
		 				}))
	password2 = forms.CharField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'repeatPassword',
		 				'type' : 'password',
		 				'class' : 'form-control',
		 				'placeholder' : 'Repite la contraseña'
		 				}))
	first_name = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'name',
		 				'class' : 'form-control',
		 				'placeholder' : 'Nombre'
		 				}))
	firstSurname = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'firstSurname',
		 				'class' : 'form-control',
		 				'placeholder' : 'Primer apellido'
		 				}))
	secondSurname = forms.CharField(max_length=30,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'secondSurname',
		 				'class' : 'form-control',
		 				'placeholder' : 'Segundo apellido'
		 				}))
	birth_date = forms.CharField(max_length=30, required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'birthdate',
		 				'class' : 'form-control',
		 				'placeholder' : 'dd/mm/aaaa',
		 				'type' : 'date'
		 				}))
	phone = forms.IntegerField(required=False,
		 			widget = forms.TextInput(attrs = {
		 				'id' : 'phone',
		 				'class' : 'form-control',
		 				'placeholder' : 'Teléfono',
		 				'type' : 'tel'
		 				}))
	torneos_participando = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	resumen_resultados = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	nuevos_torneos = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	email_com = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	sms = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))
	whatsapp = forms.BooleanField(required=False,
		 			widget = forms.CheckboxInput(attrs = {
		 				'type' : 'checkbox'
		 				}))

	def clean(self):
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password and password2:
			if password != password2:
				self.add_error('password', 'Las contraseñas no coinciden')


class EditPlayerForm(forms.ModelForm):

	class Meta:
		model = Player
		fields = ('first_name', 'firstSurname', 'secondSurname', 'birth_date', 'phone')
		widgets = {
			'first_name' : forms.TextInput(attrs={
					'id' : 'name',
		 			'class' : 'form-control',
		 			'placeholder' : 'Nombre'
				}),
			'firstSurname' : forms.TextInput(attrs={
					'id' : 'firstSurname',
		 			'class' : 'form-control',
		 			'placeholder' : 'Primer apellido'
				}),
			'secondSurname' : forms.TextInput(attrs={
					'id' : 'secondSurname',
		 			'class' : 'form-control',
		 			'placeholder' : 'Segundo apellido'
				}),
			'birth_date' : forms.TextInput(attrs = {
		 				'id' : 'birthdate',
		 				'class' : 'form-control',
		 				'placeholder' : 'dd/mm/aaaa',
		 				'type' : 'date'
		 				}),
			'phone' : forms.TextInput(attrs = {
		 				'id' : 'phone',
		 				'class' : 'form-control',
		 				'placeholder' : 'Teléfono',
		 				'type' : 'tel'
		 				})
		}