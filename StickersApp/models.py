from django.db import models
from datetime  import datetime
# Create your models here.

class RegisteCash(models.Model):
    money=models.IntegerField(default=0)
    def __str__(self):
        return self.money.__str__()+' $'
    
class Product(models.Model):
    name=models.CharField(max_length=30, unique=True)
    price=models.IntegerField()
    image=models.ImageField(blank=True,null=True,upload_to='productos',default="no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    stored=models.IntegerField(blank=True,default=0)
    sold=models.IntegerField(blank=True,default=0)
    description=models.CharField(max_length=100,blank=True)
    removed=models.BooleanField(default=False)
    confirm=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=10) 
    stored=models.IntegerField(default=0)
    sold=models.IntegerField(default=0)
    image=models.ImageField(blank=True,null=True,upload_to='categorias', height_field=None, width_field=None, max_length=None)
    product=models.ForeignKey(Product, on_delete=models.CASCADE) 
    @classmethod
    def create(cls,product,name,stored=0,sold=0):
        return cls(product=product,name=name,stored=stored,sold=sold)
    def __str__(self):
        return self.name
    
MChoise = [
    ('EP','Agregado de Productos'),
    ('CP','Creado de Producto'),
    ('SP','Quitado de Productos'),
    ('RD','Retiro de Dinero'),
    ("eP","Editado de Producto"),
    ("VP","Venta de Productos"),
    ("rP","Reembolso de Productos"),
    ("RP","Removido de Producto"),
    ("AC","Agregado de Categoría"),
    ("RC","Removido de Categoría"),
    ("cP","Confirmado de Producto"),
    ]

class Movement(models.Model):
    type=models.CharField(max_length=2,choices=MChoise)
    date=models.DateTimeField(default=datetime.now,blank=True)
    lot=models.IntegerField(default=0)
    extra_info_str=models.CharField(max_length=25,null=True,blank=True)
    extra_info_int=models.IntegerField(default=0)
    extra_info_bool=models.BooleanField(default=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True,related_name="RN_product")
    category=models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return "M"+self.id.__str__()+"-"+self.date.date().__str__()

    @classmethod
    def Create(cls,name,price,description,image):
        if price  > 0:
            product=Product(name=name,price=price,description=description)
            if product:
                if image:
                    product.image=image
                product.save()
                movement=cls(type="CP",product=product,lot=price)
                if movement:
                    movement.save()
                return True
        return False
    @classmethod
    def Remove(cls,product):
        product.removed = True
        product.description=product.name
        product.name+="[_X_]"
        movement=cls(type="RP",product=product)
        if movement:
            movement.save()
            product.save()
            return True
        return False
    @classmethod
    def Sell(cls,product,lot,category_id):
        if product and lot > 0:
            diff = product.stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.stored = diff
                    product.sold += lot
                    amount=lot * product.price
                    r_box.money += amount
                    movement=cls(type="VP",product=product,lot=lot,extra_info_int=product.price)
                    if movement:
                        if category_id:
                            category=Category.objects.get(id=category_id)
                            diff = category.stored - lot
                            print(diff)
                            if diff >= 0:
                                category.stored = diff
                                category.sold += lot
                                category.save()
                                movement.category=category
                            else:
                                return None
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
            movement=cls(type="eP",product=product,extra_info_int=price)
            
            if movement:
                movement.save()
                product.save()
                return True
        return False 
    @classmethod
    def Add(cls,product,lot,category):
        if product and lot > 0:
            movement=cls(type="EP",product=product,lot=lot)
            if movement:
                if category:
                    movement.category=category
                movement.extra_info_bool=False
                movement.save()
                product.confirm=False
                product.save()
                return True
        return False
    @classmethod
    def ConfirmAdd(cls,movement,lot):
        if movement.product.confirm == False and movement:
            if movement.product and movement.lot >= lot:
                movement_confirm=cls(type="cP",product=movement.product,lot=lot,category=movement.category)
                if movement_confirm:
                    movement_confirm.product.stored += lot
                    if movement.category:
                        movement_confirm.category.stored += lot
                        movement_confirm.category.save()
                    movement_confirm.product.confirm=True
                    movement.extra_info_bool=True
                    movement.save()
                    movement_confirm.save()
                    movement_confirm.product.save()
                    return True
        return False
    @classmethod
    def Sub(cls,product,lot,category_id):
        if product and lot > 0:
            diff= product.stored - lot
            if diff >= 0:
                product.stored = diff
                movement=cls(type="SP",product=product,lot=lot)
                if movement:
                    if category_id:
                        category=Category.objects.get(id=category_id)
                        diff = category.stored - lot
                        if diff >= 0:
                            category.stored = diff
                            category.save()
                            movement.extra_info=category.name
                        else:
                            return None
                    movement.save()
                    product.save()
                    return True
        return False
    @classmethod
    def Refund(cls,product,lot,category_id):
        if product and lot > 0:
                diff = product.sold - lot 
                if diff >= 0:
                    r_box=RegisteCash.objects.all().first()
                    if r_box:
                        amount=lot * product.price
                        r_box.money -= amount
                        if r_box.money >= 0:
                            product.sold = diff
                            product.stored += lot
                            movement=cls(type="rP",product=product,lot=lot,extra_info_int=product.price)
                            if movement:
                                if category_id:
                                    category=Category.objects.get(id=category_id)
                                    diff = category.sold - lot 
                                    if diff >= 0:
                                        category.sold = diff
                                        category.stored += lot
                                        category.save()
                                        movement.extra_info=category.name
                                    else:
                                        return {"None":True}
                                movement.save()
                                product.save()
                                r_box.save()
                                return True
                        return None
        return False
    @classmethod
    def Retire(cls,lot):
        if lot > 0:
            r_box=RegisteCash.objects.all().first()
            if r_box:
                dif= r_box.money - lot
                if dif >= 0:
                    r_box.money = dif
                    movement=cls(type="RD",lot=lot)
                    if movement:
                        movement.save()
                        r_box.save()
                        return True
        return False
    @classmethod
    def AddCategory(cls,product,category_name,image):
        categorys=Category.objects.filter(product__id=product.id)
        category_nc=None
        if categorys:
            for cat_name in categorys:
                if cat_name.__str__() == category_name.__str__():
                    return None
        else:
            category_nc=Category.create(product=product,name="Sin Categoría",stored=product.stored,sold=product.sold)
            
        category=Category.create(product=product,name=category_name)
        if category:
            if image:
                category.image=image
            movement=cls(type="AC",product=product,category=category)
            category.save()
            if category_nc:
                category_nc.save()  
            movement.save()
            return True
        return False
    @classmethod
    def RemoveCategory(cls,id,p_id):
        category=Category.objects.get(id=id)
        if category:
            categorys=Category.objects.filter(product__id=p_id)
            if categorys.count() == 2:
                for category_d in categorys:
                    category_d.delete()
            movement=cls(type="RC",product=category.product,extra_info_str=category.name)
            category.delete()
            movement.save()
            
            return True
        return False    



