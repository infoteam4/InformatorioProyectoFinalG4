from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE) #cargados los ej. quitar el null = True
    dni = models.PositiveIntegerField(unique = True , null = False )
    nombre = models.CharField(max_length=25, verbose_name="Nombre")
    apellido = models.CharField(max_length=25, verbose_name="Apellido")
    email = models.EmailField(blank=True, null = False, verbose_name="Correo")
    tel = models.PositiveIntegerField(verbose_name="Telefono", null = True )
    fecha = models.DateField(null = False)
    os = models.CharField(max_length=55, verbose_name="Obra Social")

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length = 100, null = False, unique = True)
    def __str__(self):
        return self.nombre


class Practica(models.Model):
    nombre = models.CharField(max_length = 100, null = False, unique = True)
    descripcion = models.CharField(max_length = 200, null = True)
    servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE) #BUSCAR q setee el name de la tabla foranea

    def __str__(self):
        return self.nombre


class Turno(models.Model):
    id = models.AutoField(primary_key = True)
    ESTADOS = (
        ('Libre', 'Libre'),
        ('Reservado', 'Reservado')
    )
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE, null = True)
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE, null = True)
    
    estado = models.CharField(choices = ESTADOS, max_length=50, default = 'Libre')

    fecha = models.DateField( null = True)
    hora = models.TimeField( null = True)
    servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE,null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['servicio', 'fecha', 'hora'], name='clavediahoraservicio')
        ]

    def __str__(self):
        return str(self.fecha)+' '+str(self.hora)


class Novedad(models.Model):
    descripcion = models.CharField(null = True, max_length = 1000)
    