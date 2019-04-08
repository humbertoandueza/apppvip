from django.urls import path
from .views import *

personas_urlpatterns = ([
    path('', PersonasView.as_view(), name="personas"),
    path('personasJson', PersonasJson, name="personasJson"),
    path('crear',PersonaCreate.as_view(),name="crear"),
    path('crear_persona',PersonasCreateView.as_view(),name="crear_persona"),
    path('actualizar/<int:pk>/', persona_update,name="actualizar_persona"),
    path('ver_persona/<int:pk>/', ver_persona,name="ver_persona"),

    path('borrar/<int:pk>/', persona_delete,name="borrar_persona"),


],"persona")

