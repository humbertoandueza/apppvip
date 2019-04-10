from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Actividades,Status,Iglesia,Entrenamiento,Grupo,Material,Photo,Album
from core.models import User
from django.http import JsonResponse

from django.http import HttpResponse

from django.core import serializers
from .forms import ActividadesForm,StatusForm,IglesiaForm,EntrenamientoForm,GrupoForm,PhotoForm
from django.template.loader import render_to_string
from datetime import datetime
import calendar
import time
from django.core.mail import send_mail
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired
from core.views import notificacions
from dateutil.relativedelta import relativedelta
# Create your views here.
class ActividadesView(ListView):
    model = Actividades
    template_name = 'actividades/listado.html'

def ActividadesJson(request):
    actividades = Actividades.objects.all()
    return JsonResponse(actividades,safe=False)

def AactividadesJson(request):
    actividades = Actividades.objects.all()
    json = serializers.serialize('json', actividades)
    return HttpResponse(json, content_type='application/json')

def ActividadesJson(request):
    dicts = []
    actividad = Actividades.objects.all()
    for i in actividad:
        if i.status.status == 'Suspendida':
            color = "#ffc100"
        if i.status.status == 'Realizada':
            color = "green"
        if i.status.status == 'Por Realizar':
            color = "#00B0F0"
        if i.status.status == 'No Realizada':
            color = "red"
        dicts.append({"color":color,"id":i.pk,"title":i.nombre,"start":str(i.fecha)+"T"+str(i.hora),"descripcion":i.descripcion,"lugar":i.lugar,"observacion":i.observacion,"estatus":i.status.status,"allDay":False})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)


class ActividadCreate(TemplateView):
    model = Actividades
    template_name = 'actividades/create.html'
    def get(self,request,*args,**kwargs):
        form = ActividadesForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class ActividadesCreateView1(TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        estatus_id = get_object_or_404(Status,status="Por Realizar")
        if request.method == 'POST':
            form = ActividadesForm(request.POST)
            print(request.POST['fecha'])
            if form.is_valid():
                data['form_is_valid'] = True
                data['lugar'] = request.POST['lugar']
                data['start'] = str(request.POST['fecha_submit'])+"T"+str(request.POST['hora'])
                data['descripcion'] = request.POST['descripcion']
                data['title'] = request.POST['nombre']
                data['color'] = "#00B0F0"
                status_p = form.save(commit=False)
                status_p.status = estatus_id
                actividad = form.save()
                notificacions(user=request.user,contenido="Se ha planificado una nueva actividad titulada: <strong>"+str(request.POST['nombre'])+"</strong>, fecha: <strong>"+str(request.POST['fecha_submit'])+"</strong>",url="")

                data['id'] = actividad.pk
            else:
                data['form_is_valid'] = False
        else:
            form = ActividadesForm()

        context = {'form': form}
        data['html_form'] = render_to_string('actividades/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:home')


def Status_update(request, pk):
    data = dict()
    estatus = get_object_or_404(Actividades, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=estatus)
        fecha = ''
        for i in request.POST:
            print (request.POST)
            if i == 'fecha_submit':
                estatus_id = get_object_or_404(Status,status="Por Realizar")
                fecha = request.POST['fecha_submit']
                hora = request.POST['hora']
                print ('obtengo la fecha a actualizar ',fecha )
        if fecha:
            #Nuevo registro
            if estatus.entrenamiento:
                entrenamiento= estatus.entrenamiento
            else:
                entrenamiento = None
            estatus.suspended = True
            estatus.save()
            actividad_new = Actividades(nombre = estatus.nombre,descripcion = estatus.descripcion,fecha=fecha,hora=hora,lugar = estatus.lugar,persona = estatus.persona,status = estatus_id,tipo = estatus.tipo,entrenamiento=entrenamiento)
            actividad_new.save()
            data['id'] = actividad_new.pk
            status_p = form.save(commit=False)
            data['create'] =True
            data['lugar'] = estatus.lugar
            data['descripcion'] = estatus.descripcion
            data['observacion'] = estatus.observacion
            data['title'] = estatus.nombre
            data['color'] = "#00B0F0"
            data['start'] = str(fecha)+"T"+str(hora)
            data['estatus'] = estatus_id.status
            data['form_is_valid'] = True
            notificacions(user=request.user,contenido="Actividad titulada: <strong>"+estatus.nombre+"</strong> actualizada a una nueva fecha: <p style='color:green;display: contents;'><strong>"+str(estatus.fecha)+"</strong></p>",url="")


        else:
            if form.is_valid():
                save = form.save()

                if estatus.status.status == 'Suspendida':
                    color = "#ffc100"
                    print ("Suspendida")
                if estatus.status.status == 'Realizada':
                    color = "green"
                    print (color)
                if estatus.status.status == 'Por Realizar':
                    color = "#00B0F0"
                if estatus.status.status == 'No Realizada':
                    color = "red"

                data['form_is_valid'] = True
                data['color'] = color
                notificacions(user=request.user,contenido="Actividad titulada: <strong>"+estatus.nombre+"</strong> actualizada a: <p style='color:"+color+";display: contents;'><strong>"+estatus.status.status+"</strong></p>",url="")
                data['observacion'] = save.observacion
                data['estatus'] = estatus.status.status
    else:
        form = StatusForm(instance=estatus)
    context = {'form': form,'actividad':estatus}
    data['html_form'] = render_to_string('actividades/update.html',
        context,
        request=request
    )
    return JsonResponse(data)

def chart(request):
    data = []
    MesActual = datetime.now()
    month = relativedelta(months=3)
    hace_tres_meses = MesActual-month
    print(MesActual,hace_tres_meses)
    #Hace_tre = datetime.now().month-3
    #ano = datetime.now().year
    #dias = calendar.monthrange(ano,MesActual)
    #hace_tres_meses = str(ano)+"-"+str(Hace_tre)+"-01"
    #mes_actual = str(ano)+"-"+str(MesActual)+"-"+str(dias[1])

    activividades = Actividades.objects.filter(fecha__range=[hace_tres_meses,MesActual]).exclude(status__status="Por Realizar").count()
    suspendida = Actividades.objects.filter(status__status="Suspendida",fecha__range=[hace_tres_meses,MesActual]).count()
    realizada = Actividades.objects.filter(status__status="Realizada",fecha__range=[hace_tres_meses,MesActual]).count()
    no_realizada = Actividades.objects.filter(status__status="No Realizada",fecha__range=[hace_tres_meses,MesActual]).count()
    print(activividades,suspendida,realizada,no_realizada)
    if suspendida:
        por_sus = (100*suspendida)/activividades
        data.append({"value": round(por_sus, 2),"label":"Suspendidas"})
    if realizada:
        por_rea = (100*realizada)/activividades
        data.append({"value": round(por_rea, 2),"label":"Realizadas"})
    if no_realizada:
        por_no_rea = (100*no_realizada)/activividades
        data.append({"value": round(por_no_rea, 2),"label":"No Realizadas"})
    print (activividades)
    return JsonResponse(data,safe=False)


class EstadisticasView(TemplateView):
    template_name = 'actividades/estadisticas.html'


#iglesia registro
class IglesiaCreate(TemplateView):
    model = Iglesia
    template_name = 'iglesia/create.html'
    def get(self,request,*args,**kwargs):
        form = IglesiaForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class IndexIglesiasView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'iglesia/listado.html')

def IglesiasJson(request):
    dicts = []
    iglesia = Iglesia.objects.all()
    for i in iglesia:
        dicts.append({"model":"model.iglesia","pk":i.pk,"fields":{"nombre":i.nombre,"pastor":i.pastor,"direccion":i.direccion,"telefono":i.telefono,}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)

class IglesiaCreateView(TemplateView,SuperUserMixinRequired):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = IglesiaForm(request.POST)
            if form.is_valid():
                user, created = User.objects.get_or_create(email=request.POST['email'])
                if created:
                    user.first_name = request.POST['nombre']
                    user.is_iglesia = True
                    nombre = request.POST['nombre'].lower().replace(" ", "")
                    print("nombre: ",nombre)
                    password = nombre+'1'
                    content = 'Hola te damos la bienvenida. su usuario de acceso es: '+request.POST['email']+" y su clave es: "+password
                    send_mail(
                        'Registro APPVIP',
                        content,
                        'humbertoanduezaa@gmail.com',
                        [request.POST['email']],
                        fail_silently=False,
                    )
                    user.set_password(password) # This line will hash the password

                    user.save() #DO NOT FORGET THIS LINE
                    form.save()
                    data['form_is_valid'] = True
                else:
                    data['form_is_valid'] = False
            else:
                data['form_is_valid'] = False
        else:
            form = IglesiaForm()

        context = {'form': form}
        data['html_form'] = render_to_string('iglesia/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:index_iglesia')

#entrenamiento
class EntrenamientoCreate(TemplateView):
    model = Entrenamiento
    template_name = 'entrenamiento/create.html'
    def get(self,request,*args,**kwargs):
        form = EntrenamientoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class IndexEntrenamientoView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'entrenamiento/listado.html')

def EntrenamientoJson(request):
    dicts = []
    entrenamiento = Entrenamiento.objects.all()
    for i in entrenamiento:
        dicts.append({"model":"model.entrenamiento","pk":i.pk,"fields":{"iglesia":i.iglesia.nombre,"pastor":i.iglesia.pastor}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)

class EntrenamientoCreateView(TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = EntrenamientoForm(request.POST)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            form = EntrenamientoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('entrenamiento/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:index_iglesia')



class IndexGrupoView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'grupo/listado.html')

def GrupoJson(request):
    dicts = []
    grupo = Grupo.objects.all()
    for i in grupo:
        dicts.append({"model":"model.grupo","pk":i.pk,"fields":{"nombre":i.nombre,"descripcion":i.descripcion}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)

class GrupoCreate(TemplateView):
    model = Grupo
    template_name = 'grupo/create.html'
    def get(self,request,*args,**kwargs):
        form = GrupoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})


class GrupoCreateView(TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = GrupoForm(request.POST)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True

            else:
                data['form_is_valid'] = False
                context = {'form': form}
                data['html_form'] = render_to_string('grupo/create.html',
                    context,
                    request=request
                )
                return JsonResponse(data)
        else:
            form = GrupoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('grupo/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:index_grupo')



class IndexMaterialView(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'material/listado.html')

def MaterialJson(request):
    dicts = []
    iglesia = Iglesia.objects.get(nombre=request.user.first_name)
    entrenamiento = Entrenamiento.objects.get(iglesia=iglesia)
    for i in entrenamiento.material.all():
        dicts.append({"model":"model.material","pk":i.pk,"fields":{"nombre":i.nombre,"url":i.url,'grupo':i.grupo.nombre}})
    return JsonResponse(dicts,safe=False)


class ProgressBarUploadView(TemplateView):
    def get(self, request):
        photos_list = Photo.objects.all().order_by('-id')[:6]
        print (photos_list)
        json = serializers.serialize('json', photos_list)
        return HttpResponse(json, content_type='application/json')

    def post(self, request):
        print ("id: ",request.POST['id'])
        ids = request.POST['id']
        actividad = get_object_or_404(Actividades,pk=ids)
        album = Album.objects.get_or_create(actividad=actividad)
        token = request.POST['csrfmiddlewaretoken']
        al = album[0].id
        arr = {"csrfmiddlewaretoken":token,"album":al}
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(arr, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class Album_get(TemplateView):
    def get(self,request):
        album = Album.objects.all()
        albumes =[]
        for i in album:
            photo = Photo.objects.filter(album=i.id).order_by('-id')[:1]
            albumes.append({"album":{"id":i.id,"nombre":str(i.actividad.nombre),"ult_imagen":str(photo[0])}})
            #albumes["actividad"] = i.actividad.nombre

        #json = serializers.serialize('json', album)
        return JsonResponse(albumes,safe=False)

class Album_tem(TemplateView):
    def get(self,request,**kwargs):
        return render(request,'core/landing_page/albumes.html')

class Photo_get(TemplateView):
    def get(self,request,pk):
        album = Album.objects.get(id=pk)
        photos =[]
        photo = Photo.objects.filter(album=album)
        for i in photo:
            print (i)
            photos.append({"imagen":str(i.file)})
            #photos["actividad"] = i.actividad.nombre

        #json = serializers.serialize('json', album)
        return JsonResponse(photos,safe=False)

class Photos_tem(TemplateView):
    def get(self,request,pk,**kwargs):
        album = Album.objects.get(id=pk)
        return render(request,'core/landing_page/photos.html',{'id':pk,'actividad':album.actividad.nombre})