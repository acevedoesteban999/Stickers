from django import forms

class FormEditar(forms.Form):
    name=forms.CharField( max_length=20, required=True)
    precio=forms.IntegerField(required=True)
    descripcion=forms.CharField( max_length=100, required=False,widget=forms.Textarea)
    imagen=forms.ImageField(required=False)

class FormVender(forms.Form):
    cantidad=forms.IntegerField(required=True)


    
