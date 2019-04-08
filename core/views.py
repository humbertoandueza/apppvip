from django.shortcuts import render
from django.views.generic.base import TemplateView
#Importo Mixins Login
from .mixins import LoginRequiredMixin,SuperUserMixinRequired
from django.http import JsonResponse
from django.core import serializers

from .models import Notificacion
class IndexPageView(TemplateView):
	template_name = 'core/landing_page/index.html'

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,{'titulo':'APPVIP'})

class IndexPagePanelView(LoginRequiredMixin,TemplateView):
	template_name = 'panel_admin/index.html'

class ProhibidoView(TemplateView):
	template_name = 'registration/prohibido.html'

class Notification(LoginRequiredMixin,TemplateView):
	def get(self,request):
		noti = Notificacion.objects.filter(estatus='No leida').order_by('-id')[:5]
		noti1 = Notificacion.objects.filter(estatus='No leida')

		notifications = []
		notifications.append({'cantidad':noti1.count()})
		if(noti):
			for i in noti:
				notifications.append({'notificacion':{'id':i.id,'contenido':i.contenido,'estatus':i.estatus,'fecha':i.date}})
			print('Hay notis pendientes:',noti.count())
		else:
			print('No tienes noti')
		#json = serializers.serialize('json', notifications)
		return JsonResponse(notifications,safe=False)

	def post(self,request):
		noti = Notificacion.objects.filter(id=request.POST['id'])
		noti.update(estatus="Leida")

		return JsonResponse({"success":"Notificación actualizada"})


def notificacions(user,contenido,url):
	noti = Notificacion(user=user,contenido=contenido,url=url)
	noti.save()
	return True