from django.urls import path
from .views import *

diezmo_urlpatterns = ([
    #Url para ingresos
    path('ingresos', IndexPageView.as_view(), name="ingresos"),
    path('transaccciones', Transacciones, name="transacciones"),
    path('ingresojson',IngresoJson,name="IngresosJson"),
    path('crear_ingreso',IngresoCreate.as_view(),name="crear_ingreso"),
    path('post_ingreso',IngresoCreateView.as_view(),name="post_ingreso"),
    path('ingresos/actualizar/<int:pk>/', ingreso_update,name="put_ingreso"),

    #Url para Egresos
    path('egresos', IndexEgresoPageView.as_view(), name="egresos"),
    path('egresojson',EgresoJson,name="EgresosJson"),
    path('crear_egreso',EgresoCreate.as_view(),name="crear_egreso"),
    path('post_egreso',EgresoCreateView.as_view(),name="post_egreso"),
    path('capital',Capital,name="capital"),
    #concepto
    path('concepto/', ConceptoPageView.as_view(), name="concepto"),
    path('conceptojson',ConceptoJson,name="ConceptoJson"),
    path('crear_concepto',ConceptoCreate.as_view(),name="crear_concepto"),
    path('post_concepto',ConceptoCreateView.as_view(),name="post_concepto"),
    path('concepto/ver_concepto/<int:pk>/', Concepto_detail.as_view(),name="concepto_detail"),
    path('concepto/actualizar/<int:pk>/', concepto_update,name="concepto_actualizar"),
    path('concepto/delete/', concepto_delete,name="concepto_delete"),






],"diezmo")

