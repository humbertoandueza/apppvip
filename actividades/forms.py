from django import forms

from .models import *
import datetime
from django.conf import settings
class ActividadesForm(forms.ModelForm):


    class Meta:
        model = Actividades
        fields = ('nombre','descripcion','lugar','persona','tipo','fecha','hora','entrenamiento')
        widget = {
            'hora':forms.TimeField(),
        }

    def __init__(self,*args,**kwargs):
        super (ActividadesForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['fecha'].input_formats=(settings.DATE_INPUT_FORMATS)
        self.fields['persona'].queryset = Persona.objects.filter(roles="Lider")
        self.fields['tipo'].queryset = Tipo_actividad.objects.exclude(tipo="Entrenamiento")



class StatusForm(forms.ModelForm):

    class Meta:
        model =  Actividades
        fields = ('status','observacion','statuss')


class FechaForm(forms.ModelForm):

    class Meta:
        model =  Actividades
        fields = ('fecha',)

    def __init__(self,*args,**kwargs):
        super (FechaForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['fecha'].input_formats=(settings.DATE_INPUT_FORMATS)


class IglesiaForm(forms.ModelForm):
    class Meta:
        model = Iglesia
        fields = ('nombre','pastor','direccion','email','telefono')

class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ('iglesia','grupo')

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ('nombre','descripcion')


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file','album' )
