from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
#reverse_lazy
from django.urls import reverse_lazy
#Importo Vistas Genericas para Creacion,Edicion y Eliminar
from django.views.generic.edit import CreateView
#importo El modelo Persona
from .models import Persona
#Importo Formulario
from .forms import PersonaForm
#Importo Mixins Login
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired
#importo view notification
from core.views import notificacions

# Create your views here.
class PersonasView(LoginRequiredMixin,TemplateView):
	template_name = 'persona/listado.html'

#Retorno Formulario En Json para incrustarlo en Modal
class PersonaCreate(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    model = Persona
    template_name = 'persona/create.html'
    def get(self,request,*args,**kwargs):
        form = PersonaForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

#Class para guardar Persona y en caso de error retorno formulario en Json

class PersonasCreateView(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = PersonaForm(request.POST)
            if not Persona.objects.filter(cedula=request.POST['cedula']).exists():
                if form.is_valid():
                    nombre = len(request.POST['nombre'])
                    ofrenda = request.POST['nombre']
                    
                    if nombre <= 3:
                        data['error'] = "El nombre debe contener como minimo 3 caracteres"
                        data['form_is_valid'] = False

                    elif ofrenda.lower() == "ofrenda":
                        print (ofrenda)
                        data['error'] = "El nombre introducido no es valido"
                        data['form_is_valid'] = False
                    else:
                        form.save()
                        persona_saved = Persona.objects.latest('id')
                        print ("id:",persona_saved.pk)
                        notificacions(user=request.user,contenido="Persona registrada: <strong>"+str(request.POST['nombre'].upper())+"</strong>",url=request.POST['url']+"?id="+str(persona_saved.pk))
                        data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                data['error'] = 'Ya esta registrada esta cedula'
        else:
            form = PersonaForm()

        context = {'form': form}
        data['html_form'] = render_to_string('persona/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('persona:personas')


# funcion Ver persona
def ver_persona(request,pk):
    persona = get_object_or_404(Persona,pk=pk)
    json ={"persona":{"nombre":persona.nombre,"apellido":persona.apellido,"cedula":persona.cedula,"direccion":persona.direccion,"telefono":persona.telefono,"correo":persona.correo,"rol":persona.roles}}
    return JsonResponse(json) 
#Funcion Actualizar Persona

def persona_update(request, pk):
    data = dict()
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if not Persona.objects.filter(cedula=request.POST['cedula']).exists() or persona.cedula == request.POST['cedula'] :
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            data['error'] = 'Ya esta registrada esta cedula'
    else:
        form = PersonaForm(instance=persona)
    context = {'form': form}
    data['html_form'] = render_to_string('persona/update.html',
        context,
        request=request
    )
    return JsonResponse(data)

#Funcion Borrar Persona
def persona_delete(request, pk):
    data = dict()
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        persona.delete()
        data['form_is_valid'] = True
    else:
        context = {'persona':persona}
        data['html_form'] = render_to_string('persona/delete.html',
            context,
            request=request
    )
    return JsonResponse(data)

#Retorno Json para Imprimir con DataTables 
def PersonasJson(request):
    personas = Persona.objects.exclude(nombre="Ofrenda")
    json = serializers.serialize('json', personas)
    return HttpResponse(json, content_type='application/json')