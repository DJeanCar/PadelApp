#encoding=utf-8
from django import forms
from .models import Competicion, TipoCompeticion, ClasificacionCategoria, ClasificacionNivel


class CrearTorneoForm(forms.ModelForm):

	tournamentType = forms.ModelChoiceField(queryset=TipoCompeticion.objects.all(), to_field_name="slug",
		widget = forms.Select(attrs = {
				'class' : 'form-control',
				'id' : 'tournamentType',
				'required':'True'
			}))

	categoryClassification = forms.ModelChoiceField(required=False, queryset=ClasificacionCategoria.objects.all(),
	 	widget = forms.Select(attrs = {
	 			'class' : 'form-control',
	 			'id' : 'categoryClassification',
	 			'required':'True'
	 		}))

	ClasificacionNivel = forms.ModelChoiceField(required=False, queryset=ClasificacionNivel.objects.all(),
		widget = forms.Select(attrs = {
				'class' : 'form-control',
				'id' : 'categoryClassification',
				'required':'True'
			}))

	max_jugadores = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'max_jugadores',
				'required':'True'
			}))
	min_jugadores = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'min_jugadores',
				'required':'True'
			}))
	min_equipos = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'min_equipos',
				'required':'True'
			}))
	max_equipos = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'max_equipos',
				'required':'True'
			}))
	num_cuenta = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'num_cuenta',
				'required':'True'
			}))
	fecha_sustitucion = forms.DateField(
		widget = forms.TextInput(attrs = {
				'type' : 'date',
				'class' : 'form-control',
				'id' : 'fecha_sustitucion',
				'required':'True'
			}))
	fecha_limite = forms.DateField(
		widget = forms.TextInput(attrs = {
				'type' : 'date',
				'class' : 'form-control',
				'id' : 'fecha_limite',
				'required':'True'
			}))

	class Meta:
		model = Competicion
		fields = ('name', 'urlTag', 'logo',
					'fecha_inicio','fecha_fin', 'price', 'tipoInscripcion', 'nivel_bool', 'division_bool')
		widgets = {
			'name' : forms.TextInput(attrs={
					'id' : 'name',
					'class' : 'form-control',
					'placeholder': 'Nombre del torneo',
					'required':'True'
				}),
			'urlTag' : forms.TextInput(attrs={
					'id' : 'url',
					'class' : 'form-control',
					'placeholder': 'URL corta',
					'required':'True'
				}),
			'price' : forms.TextInput(attrs = {
					'type' : 'number', 
					'class' : 'form-control',
					'id' : 'price',
					'pattern' : '[0-9]+([\.|,][0-9]+)?',
					'step' : '0.01',
					'placeholder' : 'Precio',
					'required':'True'
				}),
			'fecha_inicio' : forms.TextInput(attrs = {
					'type' : 'date',
					'class' : 'form-control',
					'id' : 'initDate',
					'placeholder' : 'dd/mm/aaaa',
					'required':'True'
				}),
			'fecha_fin' : forms.TextInput(attrs = {
					'type' : 'date',
					'class' : 'form-control',
					'id' : 'endDate',
					'placeholder' : 'dd/mm/aaaa',
					'required':'True'
				}),
			'tipoInscripcion' : forms.Select(attrs = {
				'class' : 'form-control',
				'id' : 'tipoInscripcion',
				'required':'True'
				})
		}

class ChecksTorneo(forms.ModelForm):

	class Meta:
		model = Competicion
		fields = ('nivel_bool','division_bool')