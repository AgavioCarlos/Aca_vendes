from django.urls import path, re_path
from . import views
from miapp import templates
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('recordar/', views.recordarContrasenia, name='recordar'),
    path('formularioRegistro/', views.formularioRegistro, name='registro'),
    path('inicio/', views.Inicio, name='Inicio'),
    # ELIMINAR - path('cargarPublicacion/', views.cargarPublicacion, name='cargarPublicacion'),
    path('perfil/', views.perfil, name='perfil'),
    path('subirPublicacion/', views.subirPublicacion, name='publicacion'),
    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

