from django.contrib import admin
from .models import *
# Register your models here.
class AdminAct(admin.ModelAdmin):
	list_display = [
		"id",
		"status",
		"persona",
		"fecha",
		"hora"
	]
admin.site.register(Actividades,AdminAct)
admin.site.register(Album)
admin.site.register(Photo)

admin.site.register(Status)
admin.site.register(Tipo_actividad)
admin.site.register(Iglesia)
admin.site.register(Grupo)
admin.site.register(Material)
admin.site.register(Entrenamiento)
admin.site.register(AsignarMaterial)








