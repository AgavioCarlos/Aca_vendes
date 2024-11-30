from django.db import models
# Create your models here.
class datos_personales(models.Model):
    nid_persona = models.AutoField(primary_key=True)
    cnombre = models.CharField(max_length=50)
    capellido_paterno = models.CharField(max_length=50)
    capellido_materno = models.CharField(max_length=50)
    ccorreo = models.CharField(max_length=50)
    cnumero_celular = models.CharField(max_length=50)
    cubicacion_foto = models.CharField(max_length=200, default='Desconocida')
    bhabilitado = models.BooleanField(default=True)
    dfecha_alta = models.DateTimeField(auto_now= True)
    # username = models.CharField(max_length=50, unique=True)  # Nombre de usuario único
    # password_hash = models.CharField(max_length=250)  # Almacenar la contraseña (deberías usar hashing)
    class Meta:
        db_table = 'tbl_personas'  # Nombre de la tabla existente
        managed = False 
    def __str__(self):
        return self.CCORREO
        
class Usuario(models.Model):
    nid_usuario = models.AutoField(primary_key=True)  # Autoincremental
    nid_persona = models.CharField(max_length=50, default=1)  # Nombre de usuario único
    cusuario = models.CharField(max_length=200) 
    ccontrasena = models.CharField(max_length=250)
    bhabilitado = models.BooleanField(default= True)
    dfecha_alta = models.DateField(auto_now= True)
    class Meta:
        db_table = 'tbl_usuario'  # Nombre de la tabla existente
        managed = False 
    def __str__(self):
        return self.username

class Categoria(models.Model):
    nid_categoria = models.AutoField(primary_key= True)
    ccategoria = models.CharField(max_length=50)
    bhabilitado = models.BooleanField(default=True)
    dfecha_alta = models.DateField(auto_now= True)
    dfecha_baja = models.DateField(null=True)
    class Meta:
         db_table = 'cat_categorias' 
         managed = False
         
    def _str_(self):
        return self.ccategoria

class Estado_Publicacion(models.Model):
    nid_estado_publicacion = models.AutoField(primary_key=True)
    cestado_publicacion = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'cat_estados_publicacion'
        managed = False
    def __str__(self):
        return self.cestado_publicacion
    
class Publicaciones(models.Model):
    nid_publicacion = models.AutoField(primary_key= True)
    nid_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='nid_categoria') 
    cnombre_producto = models.CharField(max_length=50)
    cdescripcion_producto = models.CharField(max_length=200)
    nprecio = models.DecimalField(max_digits=10, decimal_places=2)
    nid_estado_publicacion = models.ForeignKey(Estado_Publicacion, on_delete=models.CASCADE, db_column='nid_estado_publicacion')
    nunidades = models.IntegerField()
    nunidades_vendidas = models.IntegerField(default=0)
    bhabilitado = models.BooleanField(default=True)
    dfecha_alta = models.DateField(auto_now= True)
    
    class Meta:
        db_table = 'tbl_publicaciones'
        managed = False
        
    def _str_(self):
        return self.cnombre_producto
    
class FotoProducto(models.Model):
    nid_foto_publicacion = models.AutoField(primary_key= True)
    nid_publicacion = models.ForeignKey(Publicaciones,on_delete=models.CASCADE, db_column='nid_publicacion')
    cubicacion_foto = models.ImageField(upload_to='fotos/')
    bhabilitado = models.BooleanField(default=True)
    dfecha_alta = models.DateField(auto_now= True)
    
    class Meta:
        db_table = 'tbl_foto_publicaciones'
        managed = False
        
    def _str_(self):
        return self.nid_foto_publicacion
        
    
    
    
    
    
    
    