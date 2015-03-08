#encoding=utf-8
from django import forms
from .models import Competicion, TipoCompeticion, ClasificacionCategoria


class CrearTorneoForm(forms.ModelForm):

	tournamentType = forms.ModelChoiceField(queryset=TipoCompeticion.objects.all(), to_field_name="slug",
		widget = forms.Select(attrs = {
				'class' : 'form-control',
				'id' : 'tournamentType'
			}))

	categoryClassification = forms.ModelChoiceField(queryset=ClasificacionCategoria.objects.all(),
		widget = forms.Select(attrs = {
				'class' : 'form-control',
				'id' : 'categoryClassification'
			}))

	max_jugadores = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'players'
			}))
	num_pistas = forms.IntegerField(
		widget = forms.TextInput(attrs = {
				'type' : 'number',
				'class' : 'form-control',
				'id' : 'courts'
			}))

	class Meta:
		model = Competicion
		fields = ('name', 'urlTag', 'logo',
					'fecha_inicio','fecha_fin', 'price')
		widgets = {
			'name' : forms.TextInput(attrs={
					'id' : 'name',
					'class' : 'form-control',
					'placeholder': 'Nombre del torneo'
				}),
			'urlTag' : forms.TextInput(attrs={
					'id' : 'url',
					'class' : 'form-control',
					'placeholder': 'URL corta'
				}),
			'price' : forms.TextInput(attrs = {
					'type' : 'number', 
					'class' : 'form-control',
					'id' : 'price',
					'pattern' : '[0-9]+([\.|,][0-9]+)?',
					'step' : '0.01',
					'placeholder' : 'Precio'
				}),
			'fecha_inicio' : forms.TextInput(attrs = {
					'type' : 'date',
					'class' : 'form-control',
					'id' : 'initDate',
					'placeholder' : 'dd/mm/aaaa'
				}),
			'fecha_fin' : forms.TextInput(attrs = {
					'type' : 'date',
					'class' : 'form-control',
					'id' : 'endDate',
					'placeholder' : 'dd/mm/aaaa'
				})	
		}