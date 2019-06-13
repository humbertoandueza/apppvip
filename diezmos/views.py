from django.shortcuts import render, get_object_or_404,redirect
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired,AdministradorMixinRequired
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum
from datetime import datetime
import  json
from django.views.generic.base import TemplateView

#Importo El model
from .models import Ingreso,Egreso,Concepto
#Importo Modelo notificacion
from core.views import notificacions
#Importo Form
from .forms import IngresoForm,EgresoForm,ConceptoForm
from django.template.loader import render_to_string
# Create your views here.

class IndexPageView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'diezmos/ingreso/listado.html')


def Transacciones(request):
    if "year" in request.GET and "mes" in request.GET :
        mes = request.GET['mes']
        year = request.GET['year']
    else:
        mes = datetime.now().month
        year = datetime.now().year
    ingreso = Ingreso.objects.filter(fecha__month=mes,fecha__year=year).values_list("fecha_t","monto","disponible","tipo","id")
    ingreso1 = Ingreso.objects.filter(fecha__month=mes,fecha__year=year).aggregate(Sum('monto'))
    print(ingreso1)
    egreso = Egreso.objects.filter(fecha__month=mes,fecha__year=year).values_list("fecha_t","monto","disponible","tipo","id")
    total = ingreso1['monto__sum']
    print(total)
    transaccion = ingreso.union(egreso).order_by('-fecha_t','-id')
    tran = []
    count = 0
    for i in transaccion:
        count += 1
        tran.append({
            "count":count,
            "fecha":i[0],
            "monto":"{:,}".format(int(i[1])).replace(',','.'),
            "tipo":i[3]})
    return render(request,'diezmos/ingreso/transacciones.html',{"transacciones":tran,"total":total})

#Retorno Json para Imprimir con DataTables
def IngresoJson(request):
    dicts = []
    monto = Ingreso.objects.aggregate(Sum('monto'))
    ingresos = Ingreso.objects.all().order_by('-fecha','-id')
    for i in ingresos:
        dicts.append({"model":"model.ingreso","pk":i.pk,"fields":{"fecha":i.fecha,"monto":str(i.monto)+" bs.","numero_trans":i.numero_trans,"cedula":i.persona.cedula,"persona":i.persona.nombre,"tipo_de_pago":i.tipo_de_pago.tipopago}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)
def consulta(request):
    query = Ingreso.objects.aggregate(Sum('monto'))
    return render(request,plantillaHtml,{'context':query})
#Formulario del modelo Ingresos

class IngresoCreate(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    model = Ingreso
    template_name = 'diezmos/ingreso/create.html'
    def get(self,request,*args,**kwargs):
        form = IngresoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

#Class Post Ingresos
class IngresoCreateView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        import datetime
        data = dict()

        if request.method == 'POST':
            form = IngresoForm(request.POST)
            if form.is_valid():
                ingreso = form.save()
                hora = datetime.datetime.now().time()
                fec = request.POST['fecha']+' '+str(hora)
                Ingreso.objects.filter(pk=ingreso.pk).update(disponible=capital_obtener(),fecha_t=fec)
                #notificacions(user=request.user,contenido=request.user.first_name+" registro un ingreso de: <strong>"+str(request.POST['monto'])+" Bs.</strong>",url=ingreso.pk)
                
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            form = IngresoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/ingreso/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('diezmo:home')
#Funcion para Actualizar
def ofrenda():
    MesActual = datetime.now().month
    montoofrenda = Ingreso.objects.filter(persona__nombre='Ofrenda',fecha__month=MesActual).aggregate(Sum('monto'))
    if montoofrenda['monto__sum'] == None:
        montoofrenda = 0
    else:
        montoofrenda = montoofrenda['monto__sum']
    return (montoofrenda)
#Retorno Json Capital Disponible
def Capital(request):
    MesActual = datetime.now().month

    montoingreso = Ingreso.objects.aggregate(Sum('monto'))
    montoingreso_mes = Ingreso.objects.filter(fecha__month=MesActual).aggregate(Sum('monto'))

    montoegreso = Egreso.objects.aggregate(Sum('monto'))

    #obtener valores de ofrenda
    if montoingreso['monto__sum'] == None or montoegreso['monto__sum'] == None:
        capital = {"total":0,"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":0}

        if montoingreso['monto__sum'] != None:
            capital = {"total":montoingreso['monto__sum'],"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":montoingreso_mes['monto__sum']-ofrenda()}
        elif montoegreso['monto__sum'] != None:
            capital = {"total":-total['monto__sum'],"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":montoingreso_mes['monto__sum']-ofrenda()}
    else:
        resta = int(montoingreso['monto__sum'] - montoegreso['monto__sum'])
        if montoingreso_mes['monto__sum'] == None:
            montoingreso_mes = 0
        else:
            montoingreso_mes = montoingreso_mes['monto__sum']
        print (montoingreso_mes)
        resta_mes = int(montoingreso_mes-ofrenda())
        capital = {"total":resta,"ofrenda":ofrenda(),"diezmo":resta_mes}
    return JsonResponse(capital)


#Funcion para obtener el capital
def capital_obtener():
    montoingreso = Ingreso.objects.aggregate(Sum('monto'))
    montoegreso = Egreso.objects.aggregate(Sum('monto'))
    if montoingreso['monto__sum'] == None or montoegreso['monto__sum'] == None:
        capital = 0
        if montoingreso['monto__sum'] != None:
            capital = montoingreso['monto__sum']
        elif montoegreso['monto__sum'] != None:
            capital = montoegreso['monto__sum']
    else:
        capital = (montoingreso['monto__sum'] - montoegreso['monto__sum'])
    return capital

#Funcion para actualizar
def ingreso_update(request, pk):
    data = dict()
    ingreso = get_object_or_404(Ingreso, pk=pk)
    if request.method == 'POST':
        montoegreso = int(capital_obtener())
        monto_actualizar = int(request.POST['monto'])
        resta = (int(ingreso.monto)-montoegreso)
        resta2 = monto_actualizar-resta
        print ("\n \n \n \n resta",resta2)
        form = IngresoForm(request.POST, instance=ingreso)

        if resta2 < 0:
            data['error'] = "El monto que intenta actualizar no coincide con el dinero disponible"
            print (data['error'])
            data['form_is_valid'] = False
        else:
            if form.is_valid():
                ingreso = form.save()
                #Ingreso.objects.filter(pk=ingreso.pk).update(disponible=capital_obtener())
                data['form_is_valid'] = True


            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/ingreso/update.html',
            context,
            request=request
        )
        return JsonResponse(data)
    else:
        form = IngresoForm(instance=ingreso)
    context = {'form': form}
    data['html_form'] = render_to_string('diezmos/ingreso/update.html',
        context,
        request=request
    )
    return JsonResponse(data)



# Index del Egreso
class IndexEgresoPageView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def get(self,request,**kwargs):
        concepto = Concepto.objects.all()
        return render(request,'diezmos/egreso/listado.html',{'concepto':concepto})

#Retorno Json para Imprimir con DataTables
def EgresoJson(request):
    dicts = []
    monto = Egreso.objects.aggregate(Sum('monto'))
    egresos = Egreso.objects.all().order_by('-fecha','-id')
    for i in egresos:
        dicts.append({"model":"model.egreso","pk":i.pk,"fields":{"fecha":i.fecha,"monto":str(i.monto)+" bs.","descripcion":i.descripcion,"concepto":i.concepto.concepto}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)


#Class Formulario Egreso
class EgresoCreate(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    model = Egreso
    template_name = 'diezmos/egreso/create.html'
    def get(self,request,*args,**kwargs):
        form = EgresoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class EgresoCreateView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        import datetime

        if request.method == 'POST':
            form = EgresoForm(request.POST)
            capital = int(capital_obtener())
            print('recibo',request.POST['monto'])
            print('recibo c',Capital(request))

            monto_egreso = int(request.POST['monto'])
            resta = (capital-monto_egreso)
            print ("\n \n \n \n resta",resta)

            if resta < 0:
                data['error'] = "El monto que intenta retirar es no coincide con el dinero disponible"
                print (data['error'])
                data['form_is_valid'] = False
            else:
                if form.is_valid():
                    usuario = form.save(commit=False)
                    usuario.usuario = request.user
                    egreso = form.save()
                    hora = datetime.datetime.now().time()
                    fec = request.POST['fecha']+' '+str(hora)
                    Egreso.objects.filter(pk=egreso.pk).update(disponible=capital_obtener(),fecha_t=fec)
                    #notificacions(user=request.user,contenido=request.user.first_name+" realizó un retiro de: <strong>"+str(request.POST['monto'])+" Bs.</strong>",url=egreso.pk)

                    data['form_is_valid'] = True

                else:
                    data['form_is_valid'] = False
            context = {'form': form}
            data['html_form'] = render_to_string('diezmos/egreso/create.html',
                context,
                request=request
            )
            return JsonResponse(data)
        else:
            form = EgresoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/egreso/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('diezmo:home')


class ConceptoPageView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'diezmos/concepto/listado.html')

def ConceptoJson(request):
    dicts = []
    conceptos = Concepto.objects.all()
    for i in conceptos:
        dicts.append({"model":"model.concepto","pk":i.pk,"fields":{"concepto":i.concepto}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)


class ConceptoCreate(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    model = Concepto
    template_name = 'diezmos/concepto/create.html'
    def get(self,request,*args,**kwargs):
        form = ConceptoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class ConceptoCreateView(LoginRequiredMixin,AdministradorMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        if request.method == 'POST':
            form = ConceptoForm(request.POST)
            if form.is_valid():
                form.save()
                #notificacions(user=request.user,contenido="se ha registrado un nuevo concepto: <strong>"+str(request.POST['concepto'])+"</strong>",url="")

                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            form = ConceptoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/concepto/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('diezmo:home')

class Concepto_detail(LoginRequiredMixin,TemplateView):
    def get(self,request,pk):
        concepto = get_object_or_404(Concepto,pk=pk)
        data= dict()
        data['concepto']= concepto.concepto
        return JsonResponse(data)

def concepto_update(request, pk):
    data = dict()
    concepto = get_object_or_404(Concepto, pk=pk)
    if request.method == 'POST':
        form = ConceptoForm(request.POST, instance=concepto)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
    else:
        form = ConceptoForm(instance=concepto)
    context = {'form': form}
    data['html_form'] = render_to_string('diezmos/concepto/update.html',
        context,
        request=request
    )
    return JsonResponse(data)

def concepto_delete(request):
    data = dict()
    if request.method == 'POST':
        pk = request.POST['id']
        concepto = get_object_or_404(Concepto, pk=pk)
        egreso = Egreso.objects.filter(concepto=concepto)
        if egreso:
            data['form_is_valid'] = False
        else:
            concepto.delete()
            data['form_is_valid'] = True

    else:
        data['form_is_valid'] = False    
    return JsonResponse(data)