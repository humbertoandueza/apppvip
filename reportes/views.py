from django.views.generic import View
from django.utils import timezone
from persona.models import Persona
from .render import Render
from django.shortcuts import get_object_or_404

class Persona_general(View):

    def get(self, request):
        persona = Persona.objects.all()
        today = timezone.now()
        params = {
            'today': today,
            'personas': persona,
            'request': request
        }
        return Render.render('reportes/persona/general.html', params)

class Persona_detalle(View):

    def get(self, request,id):
        persona = get_object_or_404(Persona,id=id)
        today = timezone.now()
        params = {
            'today': today,
            'persona': persona,
            'request': request
        }
        return Render.render('reportes/persona/detalle.html', params)