from django.urls import path
from .views import *

reportes_urlpatterns = ([
    path('personas', PersonaPDF,name="personas"),
    path('ingresos', IngresoPDF,name="ingresos"),
    path('egresos', EgresoPDF,name="egresos"),
    path('transacciones', TranPDF,name="transacciones"),



],"reportes")

