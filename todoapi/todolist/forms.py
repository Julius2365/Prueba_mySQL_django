from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor']  # Lista de campos del modelo que quieres incluir en el formulario
