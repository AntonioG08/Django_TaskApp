from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea

"from django.http import HttpResponse"

"""Usuario: togor10
   Password: hola4050"""

"""Usuario: Pedro
   Password: hola3060"""

# Create your views here
"""def lista_pendientes(pedido):
    return HttpResponse('Lisa de mis pendientes')"""


# Esta clase es la que nos permite iniciar sesión
class Logueo(LoginView):
    template_name = 'Directorio/login.html'
    """Nos basamos en la vista 'LoginView' la cual tiene muchos campos, y en este caso le estamos aclarando que queremos
    trabajar con todas """
    field = '__all__'
    """Este parametro es para indicar si queremos redirigir al usuario que ha sido autenticado"""
    redirect_authenticated_user = True

    """Con esto le indicamos que una vez que el usuario se ha loggeado correctamente, sea dirigido al url de pendientes
    que es el url por default"""
    def get_success_url(self):
        return reverse_lazy('pendientes')


# Esta clase es la que nos permite registrar a usuarios nuevos
class PaginaRegistro(FormView):
    template_name = 'Directorio/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pendientes')

    # Con esta función hacemos que al hacer login, se entre al sitio con el usuario nuevo que acaba de ser creado
    def form_valid(self, form):
        """Aqui almacenamos las credenciales (usuario y contraseña) del nuevo usuario que hemos creado"""
        usuario = form.save()
        """Si si ha habido una creación de usuario, entonces ejecutamos el siguiente código"""
        if usuario is not None:
            """Aqui solicitamos el logueo de la persona con la información que acaba de llenar anteriormente"""
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    # Con esta función bloqueamos al usuario de acceder a la vista de 'registro' una vez que ya se registró
    """En teoría, con el atributo arriba de 'redirect_authenticated_user = True', no debería de pasar esto, pero como
    si ocurre, con esta función lo arreglamos manualmnente"""
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pendientes')
        return super(PaginaRegistro, self).get(*args, **kwargs)


# Esta clase nos permite ver una lista con todas las tareas que tenemos
class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    """Con esto nosotros cambiamos el nombre de nuestros 'objetos' a tareas. Login required lo usamos para garantizar
    que solo los usuarios autenticados puedan acceder"""
    context_object_name = 'tareas'

    """Kwargs es keyword arguments, es decir, argumentos que contengan palabras clave"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """Le pasamos este parametro para filtrar que solo nos muestre las tareas del usuario que está actualmente 
        logueado"""
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        """Le pasamos este parámetro para filtrar que solo muestre las tareas que no han sido completadas aun"""
        context['count'] = context['tareas'].filter(completo=False).count()

        nombre_buscado = self.request.GET.get('area-buscar') or ''
        if nombre_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=nombre_buscado)
        context['nombre_buscado'] = nombre_buscado
        return context


# Esta clase nos permite ver los detalles de una tarea en específico que elijamos
class DetalleTarea(LoginRequiredMixin, DetailView):
    """Por default el nombre debe llevar 'detail', ej. 'tarea_detail' el cual nosotros podemos cambiar después como
    en este caso usando a 'template_name'. Por ejemplo, en listas dejamos el nombre default de 'tarea_list' """
    model = Tarea
    context_object_name = 'tarea'
    """Dado que pusimos el nombre personalizado de 'tarea' a nuestro archivo HTML, debemos entonces especificar el 
    template name para que pueda ser encontrado"""
    template_name = 'Directorio/tarea.html'


# Esta clase nos permite crear nuevas tareas que el usuario necesite
class CrearTarea(LoginRequiredMixin, CreateView):
    """Por defecto debemos nombrar al documento html usando 'form' como 'tarea_form', ya después podemos cambiar
    su nombre como hemos explicado anteriormente """
    model = Tarea

    # CreateView nos permite hacer en automático formularios, solo debemos aclarar que elementos queremos del modelo
    "fields = ['titulo', 'descripcion', 'etc']"
    """El método de arriba de una manera de hacerlo, pero como en este caso queremos un formulario con todos los 
    elementos que hemos especificado en nuestro modelo, podemos usar lo siguiente
    fields = '__all__' """

    """El método ha cambiado y ahora no queremos que se vean todos los campos, pues el programa en automático asigna 
    el autor a la persona que está logueada, por ende ahora solo queremos ver ciertos campos"""
    fields = ['titulo', 'descripcion', 'completo']

    """En el documento urls, al sitio por defecto que está en blanco '' lo hemos llamado pendientes, y aqui estamos 
    solicitando que cuando la tarea ha sido enviada, nos devuelva al sitio por defecto"""
    success_url = reverse_lazy('pendientes')

    """Con esta función hacemos que la tarea sea asignada en automático a la persona que esta logueada actualmente"""
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)


# Esta clase nos permite editar las tareas que ya han sido creadas
class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    """fields = '__all__' """
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('pendientes')


# Esta clase nos permite eliminar tareas que tengamos ya creadas
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('pendientes')
