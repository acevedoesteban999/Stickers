from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=30, unique=True)
    price=models.IntegerField()
    image=models.ImageField(blank=True,null=True,upload_to='productos',default="productos/no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    stored=models.IntegerField(blank=True,default=0)
    sold=models.IntegerField(blank=True,default=0)
    description=models.CharField(max_length=100,blank=True)
    removed=models.BooleanField(default=False)
    def __str__(self):
        return self.name


class RegisteCash(models.Model):
    money=models.IntegerField(default=0)
    def __str__(self):
        return self.money.__str__()+' $'
    

class Movement(models.Model):
    MChoise = [('EP','Entrada de Productos'),('SP','Salida de Productos'),('SD','Salida de Dinero'),("DP","Editado de Producto"),("VP","Venta de Productos"),("RD","Reembolso de Productos"),("RP","Remover Producto")]
    type=models.CharField(max_length=2,choices=MChoise)
    date=models.DateTimeField(auto_now_add=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    lot=models.IntegerField(default=0)
    amount=models.IntegerField(default=0,blank=True,null=True)
    refund_id=models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return self.date.date().__str__()

    @classmethod
    def Remove(cls,product):
        import datetime
        product.removed = True
        product.name+="_"+ datetime.datetime.now().__str__()
        movement=cls(type="RP",product=product)
        if movement:
            movement.save()
            product.save()
            return True
        return False
    @classmethod
    def Sell(cls,product,lot):
        if product and lot > 0:
            diff = product.stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.stored = diff
                    product.sold += lot
                    amount=lot * product.price
                    r_box.money += amount
                    movement=cls(type="VP",product=product,lot=lot,amount=amount)
                    if movement:
                        movement.save()
                        product.save()
                        r_box.save()
                        return True
        return False
    @classmethod
    def Edit(cls,product,name,price,description,image):
        if price > 0:
            product.name=name
            product.price=price
            product.description=description
            if image:
                product.image=image
            movement=cls(type="DP",product=product,lot=price)
            if movement:
                movement.save()
                product.save()
                return True
        return False 
    @classmethod
    def Add(cls,product,lot):
        if product and lot > 0:
            product.stored += lot 
            movement=cls(type="EP",product=product,lot=lot)
            if movement:
                movement.save()
                product.save()
                return True
        return False
        
    






