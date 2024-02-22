from django.db import models
from django.contrib.auth.models import User

"""Aquí crearemos nuestras tablas que serán necesarias para ir organizando la información de las tareas que iran siendo
creadas, como por ejemplo quién la creó, la fecha, el tipo de tarea, para que fecha, etc."""


# Create your models here.
class Tarea(models.Model):
    """La persona que está creando esta tarea, será una relación de uno a varios, puesto que un solo usuario, puede
    crear muchas tareas"""
    """El argumento 'on_delete' es para aclarar que ocurrirá si el usuario es eliminado. En este caso si se elimina 
    todas sus tareas se borrarán en cascada"""
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    """El argumento max_length le aclara que solo podrá tener 200 carácteres como máximo el título"""
    titulo = models.CharField(max_length=200)
    """Los argumentos que le acabamos de pasar le indican que el espacio de descripción puede ser dejado en blanco"""
    descripcion = models.TextField(null=True,
                                   blank=True)
    """Las tareas al crearse en automático aparecen como False, es decir, no completadas, y más adelante podemos 
    modificar su valor a True o completadas"""
    completo = models.BooleanField(default=False)
    """Con este método en automático se le asignará la fecha que esté registrando la computadora y así no debemos 
    hacerlo nosotros manualmente"""
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['completo']


"""Al final de haber hecho esto es necesario ir a la terminal y ejecutar el comando 

'python manage.py makemigrations "nombre de la app" '

con lo cual actualizaremos la informacion de los modelos de la base de datos. Es un paso necesario e importante. Una 
vez que esto quedo hecho, debemos correr por último el comando 'python manage.py migrate' el cual migrará esta tabla 
a la base de datos. Este mismo comando lo corrimos al inicio de esta lección para migrar todas ls tablas que Django 
ya tiene por defecto"""