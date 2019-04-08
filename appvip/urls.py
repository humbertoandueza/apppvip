from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import login
from core.urls import core_urlpatterns
from persona.urls import  personas_urlpatterns
from diezmos.urls import diezmo_urlpatterns
from actividades.urls import actividades_urlpatterns
from reportes.urls import reportes_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    #App Core Url
	path('',include(core_urlpatterns)),
    #App Diezmos Url
	path('panel/diezmos/',include(diezmo_urlpatterns)),
    #App Persona
	path('panel/persona/',include(personas_urlpatterns)),
    #App Actividades
    #App Reportes
    path('panel/reportes/',include(reportes_urlpatterns)),

    path('panel/actividades/',include(actividades_urlpatterns)),
    #Urls Login
    path('accounts/login/',login ,{'redirect_authenticated_user': True}, name='login'),
    path('accounts/',include('django.contrib.auth.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
