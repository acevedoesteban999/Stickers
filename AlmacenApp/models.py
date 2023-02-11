from django.db import models

# Create your models here.
class Productos(models.Model):
    name=models.CharField(max_length=20)
    precio=models.IntegerField()
    imagen=models.ImageField(blank=True,null=True,upload_to='AlmacenApp/Media', height_field=None, width_field=None, max_length=None)
    En_Almacen=models.IntegerField(blank=True,default=0)
    Vendidos=models.IntegerField(blank=True,default=0)
    descripcion=models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name
    @classmethod
    def _PrecioStr(self):
        return self.precio.__str__()+' $'
    
class Caja(models.Model):
    dinero=models.IntegerField(default=0)
    def __str__(self):
        return self.dinero.__str__()+' $'
    

class Movimientos(models.Model):
    TipoChoise = [('EP','Entrada_Productos'),('SP','Salida_Productos'),('SD','Salida_Dinero')]
    tipo=models.CharField(max_length=2,choices=TipoChoise)
    fecha=models.DateTimeField(auto_now_add=True)
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=0)
    importe=models.IntegerField(default=0)
    def __str__(self):
        return self.fecha.date().__str__()
    @classmethod
    def _ImporteStr(self):
        return self.importe.__str__()+' $'





