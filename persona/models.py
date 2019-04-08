from django.db import models

# Create your models here.
class Persona(models.Model):
    cedula = models.CharField(verbose_name="Cedula",max_length=9,unique=True)
    nombre = models.CharField(verbose_name="Nombre",max_length=50)
    apellido = models.CharField(verbose_name="Apellido",max_length=200)
    telefono = models.CharField(verbose_name="Telefono",max_length=12)
    direccion = models.TextField()
    correo = models.EmailField()
    rol = (
        ("Miembro","Miembro"),
        ("Lider","Lider"),
        ("Asistente","Asistente"),
    )
    roles = models.CharField(max_length=50,choices=rol)

    def __str__(self):
        return '{},{}'.format(self.cedula,self.nombre)