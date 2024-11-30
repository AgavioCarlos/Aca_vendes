from django import forms
from .models import datos_personales
from django.contrib.auth.hashers import make_password
from .models import Usuario
from .models import Categoria
from .models import FotoProducto;
from .models import Publicaciones;
from .models import FotoPerfil;

class RegistroPersonaForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = datos_personales
        fields = ['cnombre', 'capellido_paterno', 'capellido_materno', 'ccorreo', 'cnumero_celular']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Almacenar la contraseña como un hash
        # user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class RegistroUsuarioForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['cusuario', 'ccontrasena']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Almacenar la contraseña como un hash
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class GuardarFotoPerfil(forms.ModelForm):
    class Meta:
        model = FotoPerfil
        fields =['cubicacion_foto']

class GuardarFotoPublicacionForm(forms.ModelForm):
    class Meta:
        model = FotoProducto
        fields = ['cubicacion_foto']

class GuardarPublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['nid_categoria', 'cnombre_producto', 'cdescripcion_producto', 'nprecio','nid_estado_publicacion', 'nunidades']