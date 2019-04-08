from django.contrib import admin
from .models import TipoDePago,Ingreso,Concepto,Egreso
# Register your models here.
admin.site.register(TipoDePago)
admin.site.register(Ingreso)
admin.site.register(Concepto)
admin.site.register(Egreso)


