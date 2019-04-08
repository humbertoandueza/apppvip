from django.db import models
from persona.models import Persona
from django.db.models.signals import post_delete
from django.dispatch import receiver
# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length=200)
    
    def __str__(self):
        return self.status

class Tipo_actividad(models.Model):
    tipo = models.CharField(max_length=200)

    def __str__(self):
        return self.tipo

class Iglesia(models.Model):
    nombre = models.CharField(verbose_name="Nombre",max_length=200)
    pastor = models.CharField(verbose_name="Pastor",max_length=200)
    email = models.EmailField(verbose_name="Correo")
    direccion = models.TextField(verbose_name="Direccion")
    telefono = models.CharField(verbose_name="Telefono",max_length=11)

    def __str__(self):
        return '{},{}'.format(self.nombre,self.pastor)

class Grupo(models.Model):
    nombre = models.CharField(verbose_name="Nombre",max_length=200)
    descripcion = models.TextField(verbose_name="Descripcion")

    def __str__(self):
        return '{},{}'.format(self.nombre,self.descripcion)

class Material(models.Model):
    nombre = models.CharField(verbose_name="Nombre",max_length=200)
    url = models.URLField(verbose_name="Link del Material")
    grupo = models.ForeignKey(Grupo,verbose_name="Grupo Alpha",on_delete=models.CASCADE)
    
    def __str__(self):
        return '{},{}'.format(self.nombre,self.grupo.nombre)

class Entrenamiento(models.Model):
    iglesia = models.ForeignKey(Iglesia,on_delete=models.CASCADE)
    material = models.ManyToManyField(Material)

    def __str__(self):
        return self.iglesia.nombre

class Actividades(models.Model):
    nombre = models.CharField(verbose_name="Nombre de la Actividad",max_length=200)
    descripcion = models.TextField(verbose_name="Descripcion")
    fecha = models.DateField(verbose_name="Fecha")
    hora = models.TimeField(verbose_name="Hora")
    lugar = models.TextField(verbose_name="Lugar")
    suspended = models.BooleanField(default=False)
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True)
    tipo = models.ForeignKey(Tipo_actividad,on_delete=models.CASCADE)
    entrenamiento = models.ForeignKey(Entrenamiento,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return '{},{},{}'.format(self.nombre,self.fecha,self.persona.nombre)

class Album(models.Model):
    actividad = models.ForeignKey(Actividades,on_delete=models.CASCADE)

    def __str__(self):
        return self.actividad.nombre

class Photo(models.Model):
    file = models.FileField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file)


@receiver(post_delete, sender=Photo)
def photo_post_delete_handler(sender, **kwargs):
    listingImage = kwargs['instance']
    storage, path = listingImage.file.storage, listingImage.file.path
    storage.delete(path)