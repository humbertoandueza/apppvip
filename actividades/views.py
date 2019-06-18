from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import Actividades,Status,Iglesia,Entrenamiento,Grupo,Material,Photo,Album,Tipo_actividad,AsignarMaterial
from persona.models import Persona
from core.models import User
from django.http import JsonResponse

from django.http import HttpResponse

from django.core import serializers
from .forms import ActividadesForm,StatusForm,IglesiaForm,EntrenamientoForm,GrupoForm,PhotoForm,FechaForm
from django.template.loader import render_to_string
from datetime import datetime
import calendar
import time
import datetime
from django.core.mail import send_mail
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired,ProgramadorMixinRequired
from core.views import notificacions
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import json
# Create your views here.
class ActividadesView(LoginRequiredMixin,ProgramadorMixinRequired,ListView):
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
        dicts.append(
            {"color":color,
            "id":i.pk,
            "title":i.nombre,
            "start":str(i.fecha)+"T"+str(i.hora),
            "descripcion":i.descripcion,
            "lugar":i.lugar,
            "observacion":i.observacion,
            "estatus":i.status.status,
            "estatuss":i.statuss,
            "tipo":i.tipo.tipo,
            "allDay":False})
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
        data = []

        estatus_id = get_object_or_404(Status,status="Por Realizar")
        if request.method == 'POST':
            data1 = json.loads(request.POST['data'])
            for i in data1:
                tipo = get_object_or_404(Tipo_actividad,pk=i['tipo'])
                fecha = i['fecha']
                from datetime import datetime
                ht = i['hora'].split(':')
                hora = datetime.strptime(str(ht[0])+str(ht[1]),"%H%M")
                if tipo.tipo == 'Series':
                    acti = Actividades.objects.filter(fecha=fecha,tipo=tipo).exists()
                    
                    if acti:

                        err = {
                           'form_is_valid':False,
                           'error':'Ya existe una serie planificada para esa fecha, por favor seleccione otra.' 
                        }
                        
                        return JsonResponse(err,safe=False)
                hora_pm = datetime.strptime('1400',"%H%M")
                if(i['is_domingo']):
                    if hora<hora_pm:
                        err = {
                           'form_is_valid':False,
                           'error':'Día domingo, no puede seleccionar una hora menor a las 2:00 pm, por favor seleccione otra.' 
                        }
                        
                        return JsonResponse(err,safe=False)
                from datetime import datetime
                lider = get_object_or_404(Persona,pk=i['persona'])
                act = Actividades.objects.filter(fecha=fecha,persona=lider)
                if act.exists():
                    for i in act:
                        hora_a =str(i.hora).split(':')
                        hor = datetime.strptime(str(hora_a[0])+str(hora_a[1]),"%H%M")
                        if hora>=hor:
                            hora2 = str(i.hora).split(':')
                            time2 = datetime.strptime(str(hora2[0])+str(hora2[1]),"%H%M")
                            diff = hora-time2
                            horas = int(diff.total_seconds()/3600)   # seconds to hour 
                            if horas<=3:
                                err = {
                                'form_is_valid':False,
                                'error':'Ya este lider tiene asignada una actividad muy cercana a la hora seleccionada.' 
                                }
                        
                                return JsonResponse(err,safe=False)
            count = 0
            for i in data1:
                count +=1
                nombre = i['nombre']
                descripcion = i['descripcion']
                lugar = i['lugar']
                lider = get_object_or_404(Persona,pk=i['persona'])
                tipo = get_object_or_404(Tipo_actividad,pk=i['tipo'])
                hora = i['hora']
                fecha = i['fecha']

                act = Actividades(
                    nombre=nombre,
                    descripcion=descripcion,
                    lugar=lugar,
                    persona=lider,
                    tipo=tipo,
                    hora=hora,
                    fecha=fecha,
                    status=estatus_id,
                   )
                act.save()
                if i['entre']:
                    entrenamiento = get_object_or_404(Entrenamiento,pk=int(i['entre']))
                    Actividades.objects.filter(pk=act.pk).update(entrenamiento=entrenamiento)

                    if tipo.tipo == 'Entrenamiento':
                        link='/panel/actividades/detailentrenamiento/'+str(act.pk)
                        notificacions(
                            user=entrenamiento.iglesia.usuario,
                            tipo="organizacion",
                            contenido="Se ha planificado su entrenamiento solicitado dia "+str(count)+", fecha: "+str(fecha),
                            url=link
                        )
                val = {
                    'title':nombre,
                    'descripcion':descripcion,
                    'lugar':lugar,
                    'lider':lider.nombre,
                    'tipo':tipo.tipo,
                    'hora':hora,
                    'start':str(fecha)+"T"+str(hora),
                    'id':act.pk
                }
                data.append(val)
            datos = {
                'data' : data,
                'form_is_valid':True
            }

            return JsonResponse(datos,safe=False)
            
        else:
            form = ActividadesForm()

        context = {'form': form}
        data['html_form'] = render_to_string('actividades/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:home')

class ActividadesEditView1(TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        estatus_id = get_object_or_404(Status,status="Por Realizar")
        actividad = get_object_or_404(Actividades,pk=request.POST['ida'])

        data['form_is_valid'] = True
        data['lugar'] = request.POST['lugar']
        data['descripcion'] = request.POST['descripcion']
        data['tipo'] = request.POST['tipo']
        data['title'] = request.POST['nombre']
        data['color'] = "#00B0F0"
        data['hora'] = request.POST['hora']
        data['persona'] = request.POST['persona']
        data['start'] = str(actividad.fecha)+"T"+str(request.POST['hora'])

        #actividad = form.save()
        tipo = get_object_or_404(Tipo_actividad,pk=request.POST['tipo'])
        if tipo.tipo == 'Entrenamiento':
            link='/panel/actividades/detailentrenamiento/'+str(actividad.pk)
            notificacions(
                user=actividad.entrenamiento.iglesia.usuario,
                tipo="organizacion",
                contenido="Se ha modificado su entrenamiento solicitado, fecha: "+str(actividad.fecha),
                url=link
            )


        Actividades.objects.filter(pk=actividad.pk).update(
            nombre=data['title'],
            descripcion=data['descripcion'],
            hora=data['hora'],
            lugar=data['lugar'],
            persona=data['persona'],
            tipo=data['tipo'])

        data['id'] = actividad.pk

        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:home')


def Status_update(request, pk):
    data = dict()
    estatus = get_object_or_404(Actividades, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=estatus)
        formm = FechaForm(instance=estatus)
        
        fecha = ''
        for i in request.POST:
            print (request.POST)
            if i == 'fecha_submit':
                estatus_id = get_object_or_404(Status,status="Por Realizar")
                fecha = request.POST['fecha_submit']
                hora = request.POST['hora']
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
            data['estatuss'] = estatus.statuss
            data['tipo'] = estatus.tipo.tipo
            data['title'] = estatus.nombre
            data['color'] = "#00B0F0"
            data['start'] = str(fecha)+"T"+str(hora)
            data['estatus'] = estatus_id.status
            data['form_is_valid'] = True
            #notificacions(user=request.user,contenido="Actividad titulada: <strong>"+estatus.nombre+"</strong> actualizada a una nueva fecha: <p style='color:green;display: contents;'><strong>"+str(estatus.fecha)+"</strong></p>",url="")


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
                tipo = get_object_or_404(Tipo_actividad,pk=save.tipo.pk)
                if tipo.tipo == 'Entrenamiento':
                    
                    entr = Entrenamiento.objects.filter(pk=estatus.entrenamiento.pk)
                    if estatus.status.status == 'Realizada':
                        entr.update(estatus="aceptada")

                    if estatus.status.status == 'No Realizada':
                        act = Actividades.objects.filter(entrenamiento__pk=estatus.entrenamiento.pk).exclude(status__status="No Realizada")
                        if len(act) == 0:
                            entr.update(cancelado=True)
                    link='/panel/actividades/detailentrenamiento/'+str(save.pk)
                    notificacions(
                        user=estatus.entrenamiento.iglesia.usuario,
                        tipo="organizacion",
                        contenido="Se ha actualizado el estatus de su entrenamiento solicitado, fecha: "+str(save.fecha),
                        url=link
                    )
                #notificacions(user=request.user,contenido="Actividad titulada: <strong>"+estatus.nombre+"</strong> actualizada a: <p style='color:"+color+";display: contents;'><strong>"+estatus.status.status+"</strong></p>",url="")
                data['observacion'] = save.observacion
                data['tipo'] = save.tipo.tipo
                data['estatus'] = estatus.status.status
                data['estatuss'] = estatus.statuss
    else:
        form = StatusForm(instance=estatus)
        formm = FechaForm(instance=estatus)
    if estatus.tipo.tipo == 'Entrenamiento':
        tipo = Tipo_actividad.objects.filter(tipo="Entrenamiento")
    else:
        tipo = Tipo_actividad.objects.exclude(tipo="Entrenamiento")
    lider = Persona.objects.all().filter(roles="Lider")
    context = {'form': form,'actividad':estatus,'lider':lider,'tipo':tipo,'formm':formm}
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
    #Hace_tre = datetime.now().month-3
    #ano = datetime.now().year
    #dias = calendar.monthrange(ano,MesActual)
    #hace_tres_meses = str(ano)+"-"+str(Hace_tre)+"-01"
    #mes_actual = str(ano)+"-"+str(MesActual)+"-"+str(dias[1])

    activividades = Actividades.objects.filter(fecha__range=[hace_tres_meses,MesActual]).exclude(status__status="Por Realizar").count()
    suspendida = Actividades.objects.filter(status__status="Suspendida",fecha__range=[hace_tres_meses,MesActual]).count()
    realizada = Actividades.objects.filter(status__status="Realizada",fecha__range=[hace_tres_meses,MesActual]).count()
    no_realizada = Actividades.objects.filter(status__status="No Realizada",fecha__range=[hace_tres_meses,MesActual]).count()
    if suspendida:
        por_sus = (100*suspendida)/activividades
        data.append({"value": round(por_sus, 2),"label":"Suspendidas"})
    if realizada:
        por_rea = (100*realizada)/activividades
        data.append({"value": round(por_rea, 2),"label":"Realizadas"})
    if no_realizada:
        por_no_rea = (100*no_realizada)/activividades
        data.append({"value": round(por_no_rea, 2),"label":"No Realizadas"})
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

class IndexIglesiasView(LoginRequiredMixin,ProgramadorMixinRequired,TemplateView):
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

class SolicitarAlpha(TemplateView):
    def post(self,request):
        iglesia = Iglesia.objects.get(usuario=request.user)
        grupo = Grupo.objects.get(id=int(request.POST['id']))
        entrenamiento = Entrenamiento(iglesia=iglesia,grupo=grupo)
        entrenamiento.save()
        material = Material.objects.filter(grupo=grupo).first()
        asign = AsignarMaterial(entrenamiento=entrenamiento,material=material).save()
        link = "/panel/actividades?id="+str(entrenamiento.id)+"&titulo="+iglesia.nombre+"&entrenamiento="+str(entrenamiento.pk)
        notificacions(
            user=request.user,
            tipo="programador",
            contenido="Solicitud de Entrenamiento por la organización: "+iglesia.nombre+" Tipo: "+grupo.nombre,
            url=link)
        return JsonResponse([{"is_valid":True}],safe=False)

class IglesiaCreateView(TemplateView):
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

                    usu = user.save() #DO NOT FORGET THIS LINE
                    
                    iglesia = form.save()
                    Iglesia.objects.filter(pk=iglesia.pk).update(usuario=user)
                    grupo = Grupo.objects.get(id=int(request.POST['grupo']))
                    entrenamiento = Entrenamiento(iglesia=iglesia,grupo=grupo)
                    entrenamiento.save()
                    material = Material.objects.filter(grupo=grupo).first()
                    asign = AsignarMaterial(entrenamiento=entrenamiento,material=material).save()
                    data['form_is_valid'] = True
                    link = "/panel/actividades?id="+str(entrenamiento.id)+"&titulo="+request.POST['nombre']+"&entrenamiento="+str(entrenamiento.pk)
                    notificacions(
                        user=user,
                        tipo="programador",
                        contenido="Solicitud de Entrenamiento por la organización: "+request.POST['nombre']+" Tipo: "+grupo.nombre+"",
                        url=link)

                else:
                    data['form_is_valid'] = False
                    data['error'] = 'Ya existe un registro con este correo, por favor registre otro.'

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

class IndexEntrenamientoView(LoginRequiredMixin,ProgramadorMixinRequired,TemplateView):
    def get(self,request,**kwargs):
        actividades = Actividades.objects.filter(tipo=2)
        entrenamiento = Entrenamiento.objects.all()
        material = AsignarMaterial.objects.all()
        return render(request,'entrenamiento/listados.html',{"entrenamientos":material})

class DetailActividad(TemplateView):
    def get(self,request,pk,**kwargs):
        entrenamiento = Actividades.objects.get(pk=pk)
        return render(request,'entrenamiento/ver.html',{"entrenamiento":entrenamiento})

    def dispatch(self,request,pk,*args,**kwargs):
        if request.user.is_iglesia:
            actividad = Actividades.objects.get(pk=pk)
            if actividad.entrenamiento.iglesia.usuario.pk  != request.user.pk:
                return redirect(reverse_lazy('login'))
        return super(DetailActividad,self).dispatch(request,pk,*args,**kwargs)

class MaterialA(TemplateView):
    def post(self,request):
        pk = request.POST['id']
        activo = request.POST['activo']
        asign = AsignarMaterial.objects.filter(pk=pk)
        if activo == 'true':
            activo = True
            contenido = "Ya tienes acceso a un nuevo material."
        else:
            activo = False
            contenido = "Se te ha bloqueado el acceso a un material."

        asign.update(estatus=activo)
        link='/panel/actividades/material'
        notificacions(
            user=asign.first().entrenamiento.iglesia.usuario,
            tipo="organizacion",
            contenido=contenido,
            url=link
        )
        return JsonResponse([{"is_valid":True}],safe=False)

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


class GrupoCreateView(LoginRequiredMixin,ProgramadorMixinRequired,TemplateView):
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



class IndexMaterialView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'material/listado.html')

def MaterialJson(request):
    dicts = []
    iglesia = Iglesia.objects.get(usuario=request.user)
    entrenamiento = Entrenamiento.objects.filter(iglesia=iglesia)
    material = AsignarMaterial.objects.filter(entrenamiento__in=entrenamiento,estatus=True)
    for i in material:
        dicts.append({"model":"model.material","pk":i.pk,"fields":{"nombre":i.material.nombre,"url":i.material.url,'grupo':i.material.grupo.nombre}})
    return JsonResponse(dicts,safe=False)


class ProgressBarUploadView(TemplateView):
    def get(self, request):
        photos_list = Photo.objects.all().order_by('-id')[:6]
        json = serializers.serialize('json', photos_list)
        return HttpResponse(json, content_type='application/json')

    def post(self, request):
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
            photos.append({"id":i.id,"imagen":str(i.file)})
            #photos["actividad"] = i.actividad.nombre

        #json = serializers.serialize('json', album)
        return JsonResponse(photos,safe=False)

class Photo_del(TemplateView):
    def get(self,request):
        pk = request.GET['pk']
        photo = Photo.objects.get(id=pk)
        album = Photo.objects.filter(album=photo.album)
        print(album.count())
        if album.count() == 1:
            Album.objects.filter(id=photo.album.id).delete()
        photo.delete()
        return JsonResponse([{"is_valid":True}],safe=False)

class Photos_tem(TemplateView):
    def get(self,request,pk,**kwargs):
        album = Album.objects.get(id=pk)
        return render(request,'core/landing_page/photos.html',{'id':pk,'actividad':album.actividad.nombre})







#Estadisticas
class ActividadesEstadisticas(LoginRequiredMixin,ProgramadorMixinRequired,TemplateView):
    def get(self,request):
        persona = Persona.objects.filter(roles="Lider").exclude(nombre="Ofrenda")
        tipo = Tipo_actividad.objects.all()
        today=datetime.datetime.now()
        if len(str(today.month)) == 1:
            mes = '0'+str(today.month)
        else:
            mes = today.month

        inicio="%s-%s-01" % (today.year, mes)
        fin="%s-%s-%s" % (today.year, mes, calendar.monthrange(today.year-1, int(mes))[1])
        suspendida = Actividades.objects.filter(status__status="Suspendida",fecha__range=[inicio,fin]).count()
        realizada = Actividades.objects.filter(status__status="Realizada",fecha__range=[inicio,fin]).count()
        no_realizada = Actividades.objects.filter(status__status="No Realizada",fecha__range=[inicio,fin]).count()
        found = "True"
        
        result = ""
        if realizada >0:
            exitosa = Actividades.objects.filter(status__status="Realizada",statuss="Exitosa",fecha__range=[inicio,fin]).count()
            regular = Actividades.objects.filter(status__status="Realizada",statuss="Regular",fecha__range=[inicio,fin]).count()
            no_exitosa = Actividades.objects.filter(status__status="Realizada",statuss="No exitosa",fecha__range=[inicio,fin]).count()
            result = [{"nombre":"Act. exitosas","count":exitosa},{"nombre":"Act. regulares","count":regular},{"nombre":"Act. No Exitosas","count":no_exitosa}]

        if realizada == 0 and suspendida == 0 and no_realizada == 0:
            found = "False"
        tipo_ = []
        for i in tipo:
            cantidad = Actividades.objects.filter(tipo__tipo=i.tipo,fecha__range=[inicio,fin]).exclude(status__status="Por Realizar").count()
            if cantidad >0:
                tipo_.append({
                    "nombre":i.tipo,
                    "count":cantidad
                    })
        persona_ = []
        for a in persona:
            cantidad = Actividades.objects.filter(persona=a,fecha__range=[inicio,fin]).exclude(status__status="Por Realizar").count()
            if cantidad>0:
                persona_.append({
                    "nombre":a.nombre,
                    "count":cantidad
                    })
        total = suspendida+realizada+no_realizada
        arr = [{"nombre":"Realizadas","count":realizada},{"nombre":"Suspendidas","count":suspendida},{"nombre":"No Realizadas","count":no_realizada},{"found":found}]
        return render(request,'actividades/estadisticas2.html',{"total":total,"persona_":persona_,"tipo_":tipo_,"estadistica":arr,"result":result,"persona":persona,"tipo":tipo})
        
    def post(self,request):
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio","Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        data = request.POST
        json = []
        persona = ''
        tipo = ''
        today=datetime.datetime.now()
        if data['tipo']:
            tipo = "and a.tipo_id="+data['tipo']
        else:
            tipo = ''
        if data['lider']:
            persona = "and a.persona_id="+data['lider']
        else:
            persona = ''

        if data['trimestre']:
            count = 0
            for i in range(3):
                mes = int(data['trimestre'])+count
                if len(str(mes)) == 1:
                    mes = '0'+str(mes)
                    print(mes)
                inicio="%s-%s-01" % (today.year, mes)
                fin="%s-%s-%s" % (today.year, mes, calendar.monthrange(today.year-1, int(mes))[1])
                print(inicio,fin)
                realizada = 0
                suspendida = 0
                no_realizada = 0
                for a in Actividades.objects.raw("select a.id,s.status as estatua,count(a.status_id)as cantidada,t.tipo as tipos from actividades_actividades a inner join actividades_status s inner join actividades_tipo_actividad t where s.id=a.status_id and a.fecha>='"+inicio+"' and a.fecha<='"+fin+"'and t.id=a.tipo_id "+tipo+" "+persona+" and a.status_id!=1 group by a.status_id;"):
                    if a.estatua == 'Realizada':
                        realizada += a.cantidada
                    if a.estatua == 'No Realizada':
                        no_realizada += a.cantidada
                    if a.estatua == 'Suspendida':
                        suspendida += a.cantidada
                        
                found = "True"
                if realizada == 0 and suspendida == 0 and no_realizada == 0:
                    found = "False"
                total = realizada+suspendida+no_realizada
                datos = {
                "mes":str(meses[int(mes)-1])+" ("+str(total)+")",
                "realizadas":realizada,
                "suspendidas":suspendida,
                "no_realizadas":no_realizada,
                "found":found}
                json.append(datos)
                count +=1
        return JsonResponse(json,safe=False)

"""
 select a.*,s.status from actividades_actividades a inner join actividades_status s where a.status_id="4" and s.id=a.status_id and a.fecha>='2019-04-01' and a.fecha<='2019-04-30' and a.persona_id=5 and a.tipo_id=1;
"""