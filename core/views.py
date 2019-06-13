from django.shortcuts import render
from django.views.generic.base import TemplateView
#Importo Mixins Login
from .mixins import LoginRequiredMixin,SuperUserMixinRequired
from django.http import JsonResponse
from django.core import serializers
from actividades.models import Entrenamiento,Iglesia
from .models import Notificacion
class IndexPageView(TemplateView):
	template_name = 'core/landing_page/index.html'

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,{'titulo':'APPVIP'})

class NotificacionesView(TemplateView):
	template_name = 'core/notificaciones.html'
	def get(self,request):
		if request.user.is_programador:
			noti = Notificacion.objects.filter(tipo="programador").order_by('-id')
		elif request.user.is_iglesia:
			noti = Notificacion.objects.filter(tipo="organizacion",user=request.user).order_by('-id')

		notifications = []
		#notifications.append({'cantidad':noti1.count()})
		if(noti):
			count= 0
			for i in noti:
				count +=1
				notifications.append({"count":count,'id':i.id,'contenido':i.contenido,'estatus':i.estatus,'fecha':i.date,"url":i.url})
		return render(request,self.template_name,{"notificaciones":notifications})


class IndexPagePanelView(LoginRequiredMixin,TemplateView):
	template_name = 'panel_admin/index.html'
	def get(self,request,*args,**kwargs):
		serie = False
		nino = False
		joven = False
		matri = False
		if request.user.is_iglesia:
			iglesia = Iglesia.objects.get(usuario=request.user)
			entrenamiento = Entrenamiento.objects.filter(iglesia=iglesia)
			for i in entrenamiento:
				if i.grupo.nombre == 'ALPHA SERIES':
					serie = True
				if i.grupo.nombre == 'ALPHA NIÑOS':
					nino = True
				if i.grupo.nombre == 'ALPHA JOVEN':
					joven = True
				if i.grupo.nombre == 'ALPHA MATRIMONIO':
					matri = True
		else:
			entrenamiento = ''
		return render(request,self.template_name,{"serie":serie,"nino":nino,"joven":joven,"matri":matri})

class ProhibidoView(TemplateView):
	template_name = 'registration/prohibido.html'

class Notification(LoginRequiredMixin,TemplateView):
	def get(self,request):
		if request.user.is_programador:
			noti = Notificacion.objects.filter(tipo="programador",estatus='No leida').order_by('-id')[:4]
			noti1 = Notificacion.objects.filter(tipo="programador",estatus='No leida')
		elif request.user.is_iglesia:
			noti = Notificacion.objects.filter(tipo="organizacion",user=request.user,estatus='No leida').order_by('-id')[:4]
			noti1 = Notificacion.objects.filter(tipo="organizacion",user=request.user,estatus='No leida')

		notifications = []
		notifications.append({'cantidad':noti1.count()})
		if(noti):
			for i in noti:
				notifications.append({'notificacion':{'id':i.id,'contenido':i.contenido,'estatus':i.estatus,'fecha':i.date,"url":i.url}})
		return JsonResponse(notifications,safe=False)

	def post(self,request):
		noti = Notificacion.objects.filter(id=request.POST['id'])
		noti.update(estatus="Leida")

		return JsonResponse({"success":"Notificación actualizada"})


def notificacions(user,contenido,url,tipo):
	noti = Notificacion(user=user,contenido=contenido,url=url,tipo=tipo)
	noti.save()
	return True