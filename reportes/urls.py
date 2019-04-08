from django.urls import path
from .views import *

reportes_urlpatterns = ([
    path('', Persona_general.as_view(),name="personas_general"),
    path('<int:id>', Persona_detalle.as_view(),name="persona_detalle")

],"reportes")

