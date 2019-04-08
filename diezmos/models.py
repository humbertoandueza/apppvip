from django.db import models
from persona.models import  Persona
from core.models import User
# Create your models here.


#Modulo de Ingreso
class TipoDePago(models.Model):
    tipopago = models.CharField(verbose_name="Tipo de Pago",max_length=60)

    def __str__(self):
        return self.tipopago

class Ingreso(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.IntegerField(verbose_name="Monto")
    numero_trans = models.IntegerField(verbose_name="Numero de Transferencia",null=True,blank=True)
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    tipo_de_pago = models.ForeignKey(TipoDePago,on_delete=models.CASCADE)

    def __str__(self):
        return '{},{},{}'.format(self.persona.nombre,self.fecha,self.monto)

#Modulo de Egreso
class Concepto(models.Model):
    concepto = models.CharField(verbose_name="Concepto", max_length=60)
    
    def __str__(self):
        return self.concepto

class Egreso(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.IntegerField(verbose_name="Monto")
    descripcion = models.TextField(verbose_name="Descripcion")
    concepto = models.ForeignKey(Concepto,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return '{},{},{}'.format(self.usuario.first_name,self.fecha,self.monto)
    




