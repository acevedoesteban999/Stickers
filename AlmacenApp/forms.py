from django import forms
class FormProduc(forms.Form):
    name=forms.CharField( max_length=20, required=True)
    precio=forms.IntegerField(required=True)
    descripcion=forms.CharField( max_length=100, required=False,widget=forms.Textarea)
    imagen=forms.ImageField(required=False)

class FormLot(forms.Form):
    cantidad=forms.IntegerField(required=True)


# FormChoise = [
        
#         ('NF','Sin Filtro'),
#         ('EP','Entrada de Productos'),
#         ('CP','Creado Producto'),
#         ('SP','Salida de Productos'),
#         ('RD','Retirada de Dinero'),
#         ("eP","Editado de Producto"),
#         ("VP","Venta de Productos"),
#         ("rP","Reembolso de Productos"),
#         ("RP","Remover Producto")]
        
# class FormFilter(forms.Form):  
#     TypeFilter=forms.ChoiceField(choices=FormChoise)


    
