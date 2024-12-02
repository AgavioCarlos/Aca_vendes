from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Usuario, FotoPerfil, datos_personales, Categoria, FotoProducto, Publicaciones
from .models import Estado_Publicacion
from django.contrib.auth.hashers import make_password, check_password
from collections import defaultdict
from django.db import transaction
from django.http import JsonResponse
from django.core.files.storage import default_storage

def home(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['password']
        
        try: 
            # Busca al usuario por correo
            usuario = Usuario.objects.get(cusuario=username)
            # Verifica la contraseña
            if check_password(password, usuario.ccontrasena):
                # Credenciales válidas
                request.session['usuario_id'] = usuario.nid_usuario
                request.session['usuario_cuenta'] = usuario.cusuario
                # Cuando se usa una llave foránea, se debe guardar el campo que referencia la tabla, no el objeto completo.
                request.session['usuario_persona'] = usuario.nid_persona.nid_persona
                
                return redirect('Inicio')  
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
             messages.error(request, 'Usuario no encontrado.')
        request.session.flush() 
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
        perfil = request.FILES.get('perfil')   
        
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
            nueva_persona.save()
            
            nuevo_usuario = Usuario(
                cusuario = usuario,
                nid_persona = nueva_persona,
                ccontrasena = password_hash
            )
            nuevo_usuario.save()
            
            if perfil:
                foto_perfil = FotoPerfil(
                    nid_usuario=nuevo_usuario,  # Relación ya guardada
                    cubicacion_foto=perfil      # Archivo subido
                )
                foto_perfil.save()  # Guardar la foto
            else:
                messages.warning(request, 'No se ha cargado una foto de perfil.')
            
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('home')
    return render(request, 'miapp/Formulario-registro.html')

def Inicio(request):
    #Obtener sesion 
    usuario_cta = request.session.get('usuario_cuenta')  # Recuperar el ID del usuario
    if not usuario_cta:
        return redirect('home')  # Redirigir si no hay usuario en la sesión

    persona_id = request.session.get('usuario_persona') #Recupera el ID de la Persona (Llave foranea)
    # Obtén el registro de la tabla 'tbl_personas' usando el ID
    try:
        persona = datos_personales.objects.get(nid_persona=persona_id)
    except datos_personales.DoesNotExist:
        persona = None  # O maneja el caso en que no se encuentra la persona
    
        
    # Obtener la información del usuario desde la base de datos
    usuario = Usuario.objects.get(cusuario=usuario_cta)
    
    categorias = Categoria.objects.all()
    publicaciones = Publicaciones.objects.all()  # Obtiene todas las publicaciones
    fotos = FotoProducto.objects.select_related('nid_publicacion')


    
    context = {
        'persona' : persona,
        'categorias': categorias,
        'publicaciones': publicaciones,
        'fotos' : fotos,
        'usuario' : usuario,
    }
    return render(request, 'miapp/Inicio.html', context)

def Publicacion(request):
    fotos = Publicacion.objects.all()
    return render(request, 'Inicio.html', {'fotos': fotos})

def perfil(request):    
    #Obtener sesion 
    usuario_id = request.session.get('usuario_cuenta')  # Recuperar cuenta
    if not usuario_id:
        return redirect('home') 
    
    # Obtener la información del usuario desde la base de datos
    usuario = Usuario.objects.get(cusuario=usuario_id)
    
    usuario_id = request.session.get('usuario_id')  # Recuperar el ID del usuario
    # Obtén el registro de la tabla 'tbl_personas' usando el ID
    try:
        foto = FotoPerfil.objects.get(nid_usuario=usuario_id)
    except datos_personales.DoesNotExist:
        foto = None  # O maneja el caso en que no se encuentra la persona
    
    
    persona_id = request.session.get('usuario_persona') #Recupera el ID de la Persona (Llave foranea)
    # Obtén el registro de la tabla 'tbl_personas' usando el ID
    try:
        persona = datos_personales.objects.get(nid_persona=persona_id)
    except datos_personales.DoesNotExist:
        persona = None  # O maneja el caso en que no se encuentra la persona
    
    
    context = {
        'persona' : persona,
        'usuario' : usuario,
        'foto' : foto
    }
    return render(request, 'miapp/Perfil.html', context)

def subirPublicacion(request):
    

    id_usuario = request.session.get('usuario_id')  # Recuperar el ID del usuario
    
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombreProducto')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        estado_id = request.POST.get('estado')
        categoria_id = request.POST.get('categoria')
        unidades = request.POST.get('unidades')  
        imagenes = request.FILES.getlist('imagenes[]')          
        
        estado = get_object_or_404(Estado_Publicacion, nid_estado_publicacion=estado_id)
        categoria = get_object_or_404(Categoria, nid_categoria=categoria_id)
        usuario = get_object_or_404(Usuario, nid_usuario=id_usuario)
        
        #Crear la publicacion y la foto asociada en una transicción atomica 
        with transaction.atomic():
            publicaciones = Publicaciones.objects.create(
                cnombre_producto = nombre_producto,
                cdescripcion_producto = descripcion, 
                nprecio = precio,
                nid_estado_publicacion = estado, 
                nid_categoria = categoria,
                nid_usuario = usuario,
                nunidades = unidades 
            )
            for imagen in imagenes:
                #ruta = f"fotos/{imagen.name}"
                ruta = default_storage.save(f"fotos/{imagen.name}", imagen)
                #Crear la foto asociada
                FotoProducto.objects.create(
                    cubicacion_foto = ruta, 
                    nid_publicacion = publicaciones
                )
        return redirect('Inicio')
    
    categorias = Categoria.objects.all()
    estados = Estado_Publicacion.objects.all()
    context = {
        'categorias': categorias,
        'estados': estados,
    }
    return render(request, 'miapp/Formulario-publicaciones.html', context)


def cerrar_sesion(request):
    # Elimina todas las variables de sesión
    request.session.flush()
    # Redirige a la página de inicio
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['password']
        
        try: 
            # Busca al usuario por correo
            usuario = Usuario.objects.get(cusuario=username)
            # Verifica la contraseña
            if check_password(password, usuario.ccontrasena):
                # Credenciales válidas
                request.session['usuario_id'] = usuario.nid_usuario
                request.session['usuario_cuenta'] = usuario.cusuario
                # Cuando se usa una llave foránea, se debe guardar el campo que referencia la tabla, no el objeto completo.
                request.session['usuario_persona'] = usuario.nid_persona.nid_persona
                
                return redirect('Inicio')  
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
             messages.error(request, 'Usuario no encontrado.')
        request.session.flush() 
    return render(request, 'miapp/Index.html')

def historial(request):
        #Obtener sesion 
    usuario_id = request.session.get('usuario_cuenta')  # Recuperar cuenta
    if not usuario_id:
        return redirect('home') 
    
    # Obtener la información del usuario desde la base de datos
    usuario = Usuario.objects.get(cusuario=usuario_id)
    
    usuario_id = request.session.get('usuario_id')  # Recuperar el ID del usuario
    # Obtén el registro de la tabla 'tbl_personas' usando el ID
    try:
        foto = FotoPerfil.objects.get(nid_usuario=usuario_id)
    except datos_personales.DoesNotExist:
        foto = None  # O maneja el caso en que no se encuentra la persona
    
    
    persona_id = request.session.get('usuario_persona') #Recupera el ID de la Persona (Llave foranea)
    # Obtén el registro de la tabla 'tbl_personas' usando el ID
    try:
        persona = datos_personales.objects.get(nid_persona=persona_id)
    except datos_personales.DoesNotExist:
        persona = None  # O maneja el caso en que no se encuentra la persona
    
    
    context = {
        'persona' : persona,
        'usuario' : usuario,
        'foto' : foto
    }
    return render(request, 'miapp/Historial.html', context)