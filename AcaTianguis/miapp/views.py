from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario, datos_personales, Categoria, FotoProducto, Publicaciones
from .models import Estado_Publicacion
from django import forms
from .forms import RegistroPersonaForm
from .forms import RegistroUsuarioForm
from .forms import GuardarFotoPublicacionForm
from .forms import GuardarPublicacionForm
from django.contrib.auth.hashers import make_password, check_password
from collections import defaultdict
from django.db import transaction 

def home(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        try:
            usuario = Usuario.objects.get(cusuario=usuario)
            if check_password(password, usuario.ccontrasena):  # Compara contraseñas (deberías usar hashing en producción)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('Inicio')  # Redirigir a la vista de inicio
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario perdido.')
        
    return render(request, 'miapp/Index.html')

def recordarContrasenia(request):
    return render(request, 'miapp/Formulario-olvido-contraseña.html')

def formularioRegistro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        correo_electronico = request.POST.get('correo_electronico')
        usuario = request.POST.get('usuario')
        numero_telefonico = request.POST.get('numero_telefonico')
        password = request.POST.get('password')
        
        #Validacion básica
        if datos_personales.objects.filter(ccorreo=correo_electronico).exists():
            messages.error(request, 'El numero de cuenta ya existe.')
        else: 
            #Crear un nuevo usuario
            password_hash = make_password(password)
            
            nueva_persona = datos_personales(
                cnombre = nombre, 
                capellido_paterno = apellido_paterno, 
                capellido_materno = apellido_materno,   
                ccorreo = correo_electronico, 
                cnumero_celular = numero_telefonico,       
            )
            nuevo_usuario = Usuario(
                cusuario = usuario,
                ccontrasena = password_hash,
            )
            nueva_persona.save()
            nuevo_usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('home')
    return render(request, 'miapp/Formulario-registro.html')


def Inicio(request):
    categorias = Categoria.objects.all()
    publicaciones = Publicaciones.objects.all()  # Obtiene todas las publicaciones
    fotos = FotoProducto.objects.select_related('nid_publicacion')
    
    # publicaciones = Publicacion.objects.all()
    # fotos = FotoProducto.objects.all()
    
    # Obtenemos todas las fotos y las ordenamos por `nid_fotos`
    # fotos = FotoProducto.objects.all().order_by('nid_publicacion')

    # # Creamos un diccionario donde cada clave es `nid_foto_publicacion` y su valor es una lista de fotos
    # grouped_fotos = {}
    # for foto in fotos:
    #     if foto.nid_publicacion not in grouped_fotos:
    #         grouped_fotos[foto.nid_publicacion] = []
    #     grouped_fotos[foto.nid_publicacion].append(foto)
    # Agrupar productos por id_imagen
    # productos_agrupados = defaultdict(list)
    # for fotoProducto in fotosProducto:
    #     productos_agrupados[fotoProducto.nid_publicacion].append(fotoProducto)
        
    context = {
        'categorias': categorias,
        'publicaciones': publicaciones,
        'fotos' : fotos,
    }
    return render(request, 'miapp/Inicio.html', context)

#SOLO SON PRUEBAS
def Index(request):
    return render(request, 'miapp/Index.html')

def subirFoto(request):
    if request.method == 'POST':
        form = GuardarFotoPublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'miapp/CargarPublicacion.html')
    else:
        form = GuardarFotoPublicacionForm()
    return render(request, 'miapp/CargarPublicacion.html', {'form': form})

def Publicacion(request):
    fotos = Publicacion.objects.all()
    return render(request, 'Inicio.html', {'fotos': fotos})

def cargarPublicacion(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        nombre_producto = request.POST.get('nombreProducto')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        unidades = request.POST.get('unidades')    
        #Agregar la llave primaria de nid_foto_publicacion 
        publicacion=Publicacion(
            nid_categoria = categoria,
            cnombre_producto = nombre_producto, 
            cdescripcion_producto = descripcion, 
            nprecio = precio,   
            nunidades = unidades,     
            )
        form = GuardarFotoPublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        publicacion.save()
        return redirect('home')  
    else: 
        form = GuardarFotoPublicacionForm()
    context = {
        'categorias': categorias,
        'form': form,
    }
    return render(request, 'miapp/CargarPublicacion.html', context)


def perfil(request):
    return render(request, 'miapp/Perfil.html')

def subirPublicacion(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombreProducto')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        estado_id = request.POST.get('estado')
        categoria_id = request.POST.get('categoria')
        unidades = request.POST.get('unidades')  
        imagen = request.FILES.get('imagen')          #FotoPublicacion 
        
        estado = get_object_or_404(Estado_Publicacion, nid_estado_publicacion=estado_id)
        categoria = get_object_or_404(Categoria, nid_categoria=categoria_id)
        #Crear la publicacion y la foto asociada en una transicción atomica 
        
        with transaction.atomic():
            publicaciones = Publicaciones.objects.create(
                cnombre_producto = nombre_producto,
                cdescripcion_producto = descripcion, 
                nprecio = precio,
                nid_estado_publicacion = estado, 
                nid_categoria = categoria,
                nunidades = unidades 
            )
            #Crear la foto asociada
            FotoProducto.objects.create(
                cubicacion_foto = imagen, 
                nid_publicacion = publicaciones
            )
        return redirect('Inicio')
            
        # # Verifica que el id de la categoría sea válido y obtenlo
        # try:
        #     categoria = Categoria.objects.get(nid_categoria=categoria_id)
        # except Categoria.DoesNotExist:
        #     messages.error(request, 'Categoría no válida')
        #     return render(request, 'miapp/Formulario-publicaciones.html', {'categorias': categorias})
        
        #  # Verifica la categoría antes de crear la publicación
        # if not categoria:
        #     messages.error(request, 'Error: Categoría no encontrada')
        #     return render(request, 'miapp/Formulario-publicaciones.html', {'categorias': categorias})
        
        # # Confirma que 'categoria' es válida y crea la publicación
        # publicacion=Publicacion(
        #     nid_categoria = categoria,
        #     cnombre_producto = nombre_producto, 
        #     cdescripcion_producto = descripcion, 
        #     nprecio = precio,   
        #     nunidades = unidades  
        #     )
        # publicacion.save()
        # if imagen:
        #     # Guarda el archivo en la base de datos
        #     fotos = FotoProducto(nid_publicacion = publicacion, cubicacion_foto = imagen)
        #     fotos.save()
        # messages.success(request, 'Publicacion exitosa.')
    categorias = Categoria.objects.all()
    estados = Estado_Publicacion.objects.all()
    context = {
        'categorias': categorias,
        'estados': estados,
    }
    return render(request, 'miapp/Formulario-publicaciones.html', context)