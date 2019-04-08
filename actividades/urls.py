from django.urls import path
from .views import *

actividades_urlpatterns = ([
    path('', ActividadesView.as_view(), name="home"),
    path('actividades', ActividadesJson, name="actividades_json"),
    path('iglesias', IglesiasJson, name="iglesias_json"),
    path('grupos', GrupoJson, name="grupos_json"),
    path('materiales', MaterialJson, name="material_json"),


    path('entrenamientos', EntrenamientoJson, name="entrenamiento_json"),

    path('iglesia',IndexIglesiasView.as_view(),name="index_iglesia"),
    path('material',IndexMaterialView.as_view(),name="index_material"),

    path('grupo',IndexGrupoView.as_view(),name="index_grupo"),

    path('entrenamiento',IndexEntrenamientoView.as_view(),name="index_entrenamiento"),

    path('post_iglesia',IglesiaCreateView.as_view(),name="post_iglesia"),
    path('post_grupo',GrupoCreateView.as_view(),name="post_grupo"),

    path('post_entrenamiento',EntrenamientoCreateView.as_view(),name="post_entrenamiento"),


    path('crear',ActividadCreate.as_view(),name="crear_actividad"),
    path('crear_iglesia',IglesiaCreate.as_view(),name="crear_iglesia"),
    path('crear_entrenamiento',EntrenamientoCreate.as_view(),name="crear_entrenamiento"),
    path('crear_grupo',GrupoCreate.as_view(),name="crear_grupo"),

    #Galerria
    path('progress-bar-upload/',ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    path('album/',Album_get.as_view(),name="album"),
    path('albumes/',Album_tem.as_view(),name="albumes"),
    path('photo/<int:pk>/',Photo_get.as_view(),name="photo"),
    path('photos/<int:pk>/',Photos_tem.as_view(),name="photos"),




    path('post',ActividadesCreateView1.as_view(),name="post_actividad"),
    path('actualizar/<int:pk>/', Status_update,name="actualizar_status"),
    path('chart',chart,name="chart"),
    path('estadisticas',EstadisticasView.as_view(),name="estadisticas")


],"actividades")

