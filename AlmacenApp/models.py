from django.db import models

# Create your models here.
class Productos(models.Model):
    name=models.CharField(max_length=30, unique=True)
    precio=models.IntegerField()
    imagen=models.ImageField(blank=True,null=True,upload_to='productos',default="productos/no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    En_Almacen=models.IntegerField(blank=True,default=0)
    Vendidos=models.IntegerField(blank=True,default=0)
    descripcion=models.CharField(max_length=100,blank=True)
    eliminado=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Caja(models.Model):
    dinero=models.IntegerField(default=0)
    def __str__(self):
        return self.dinero.__str__()+' $'
    

class Movimientos(models.Model):
    TipoChoise = [('EP','Entrada Productos'),('SP','Salida Productos'),('SD','Salida Dinero'),("VP","Venta Productos")]
    tipo=models.CharField(max_length=2,choices=TipoChoise)
    fecha=models.DateTimeField(primary_key=True,auto_now_add=True)
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad=models.IntegerField(default=0)
    importe=models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return self.fecha.date().__str__()
    
    @classmethod
    def crear_venta(cls,producto,cantidad):
        if producto and cantidad > 0:
            cant = producto.En_Almacen - cantidad 
            if cant >= 0:
                producto.En_Almacen=cant
                producto.Vendidos+=cantidad
                caja=Caja.objects.all().first()
                importe=cantidad*producto.precio
                caja.dinero+=importe
                movimiento=cls(tipo="VP",producto=producto,cantidad=cantidad,importe=importe)
                movimiento.save()
                producto.save()
                caja.save()
                return True
        return False
    @classmethod
    def crear_agregar(cls,producto,cantidad):
        if producto and cantidad > 0:
            producto.En_Almacen += cantidad 
            movimiento=cls(tipo="EP",producto=producto,cantidad=cantidad)
            movimiento.save()
            producto.save()
            return True
        return False
        
    






