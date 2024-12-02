from django.urls import path
from . import views
from miapp import templates
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('inicio/', views.Inicio, name='Inicio'),
    path('recordar/', views.recordarContrasenia, name='recordar'),
    path('formularioRegistro/', views.formularioRegistro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('subirPublicacion/', views.subirPublicacion, name='publicacion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('historial/', views.historial, name='historial'),
    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

