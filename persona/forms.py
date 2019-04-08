from django import forms

from .models import Persona

class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = ('cedula', 
        'nombre',
        'apellido','roles',
        'telefono',
        'direccion',
        'correo')

    