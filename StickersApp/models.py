from django.db import models
from datetime  import datetime
from django.contrib.auth.models import User
# Create your models here.

class Visits(models.Model):
    # today_date=models.DateField( auto_now=False, auto_now_add=False)
    # todat_visits=models.IntegerField(default=0)
    # week_date=models.DateField( auto_now=False, auto_now_add=False)
    # week_visits=models.IntegerField(default=0)
    # month_date=models.DateField( auto_now=False, auto_now_add=False)
    # month_visits=models.IntegerField(default=0)
    total_visits=models.IntegerField(default=0)

class RegisteCash(models.Model):
    money=models.IntegerField(default=0)
    def __str__(self):
        return self.money.__str__()+' $'
    
class Product(models.Model):
    name=models.CharField(max_length=30, unique=True)
    pair=models.BooleanField(default=False)
    unit_price=models.IntegerField(default=0)
    unit_profit_worker=models.IntegerField(default=0)
    pair_price=models.IntegerField(default=0,blank=True,null=True)
    pair_profit_worker=models.IntegerField(default=0,blank=True,null=True)
    image=models.ImageField(blank=True,null=True,upload_to='productos',default="no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    unit_stored=models.IntegerField(blank=True,default=0)
    pair_stored=models.IntegerField(blank=True,default=0)
    unit_sold=models.IntegerField(blank=True,default=0)
    pair_sold=models.IntegerField(blank=True,default=0)
    description=models.CharField(max_length=100,blank=True)
    removed=models.BooleanField(default=False)
    confirm=models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=20) 
    unit_stored=models.IntegerField(default=0)
    pair_stored=models.IntegerField(default=0)
    unit_sold=models.IntegerField(default=0)
    pair_sold=models.IntegerField(default=0)
    image=models.ImageField(blank=True,null=True,upload_to='categorias', height_field=None, width_field=None, max_length=None)
    product=models.ForeignKey(Product, on_delete=models.CASCADE) 
    @classmethod
    def create(cls,product,name,unit_stored=0,pair_stored=0,unit_sold=0,pair_sold=0):
        return cls(product=product,name=name,unit_stored=unit_stored,pair_stored=pair_stored,pair_sold=pair_sold,unit_sold=unit_sold)
    def __str__(self):
        return self.name
    
MChoise = [
    ('CP','Creado de Producto'),
    ("eP","Editado de Producto"),
    ("RP","Removido de Producto"),
    ('EP','Agregado de Productos'),
    ("cP","Confirmado de Producto"),
    ("VP","Venta de Productos"),
    ("rP","Reembolso de Productos"),
    ('SP','Quitado de Productos'),
    ("AC","Agregado de Categoría"),
    ("RC","Removido de Categoría"),
    ('AD','Agregado de Dinero'),
    ('RD','Retiro de Dinero'),
    ]

class Movement(models.Model):
    type=models.CharField(max_length=2,choices=MChoise)
    date=models.DateTimeField(default=datetime.now,blank=True)
    lot=models.IntegerField(default=0)
    extra_info_str=models.CharField(max_length=100,null=True,blank=True)
    extra_info_int=models.IntegerField(default=0)
    extra_info_int_1=models.IntegerField(default=0)
    extra_info_bool=models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True,related_name="product")
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return "M"+self.id.__str__()+"-"+self.date.date().__str__()

    @classmethod
    def Create(cls,user,name,pair,unit_price,unit_profit_worker,pair_price,pair_profit_worker,description,image):
        if unit_price  > 0 and unit_profit_worker > 0 and unit_price >= unit_profit_worker:
            if pair == True :
                if pair_price <= 0 or pair_profit_worker <= 0 or pair_price < pair_profit_worker:
                    return False
            product=Product(
                name=name,
                pair=pair,
                unit_price=unit_price,
                unit_profit_worker=unit_profit_worker,
                pair_price=pair_price,
                pair_profit_worker=pair_profit_worker,
                description=description
                )
            str_info="Nombre:{}<br>Por Pares:{}<br>{}{}<br>Descripcion:{}<br>Imagen:{}<br>".format(
                name,
                "Si" if pair else "No",
                "Precio por Par:{}<br>Ganancia por Par:{}<br>".format(pair_price,pair_profit_worker) if pair else "",
                "Precio por Unidad:{}<br>Ganancia por Unidad:{}".format(unit_price,unit_profit_worker),
                "{}".format("Si" if len(description.__str__()) > 0 else "No"),
                "{}".format("Si" if image else "No")
                )
            if product:
                if image:
                    product.image=image
                movement=cls(type="CP",product=product,extra_info_str=str_info,user=user)
                if movement:
                    try:
                        product.save()
                        movement.save()
                        return True
                    except:
                        return "E0"
        return False
    @classmethod
    def Remove(cls,user,product):
        product.removed = True
        product.description=product.name
        product.name+="[_X_]"
        movement=cls(type="RP",product=product,user=user)
        if movement:
            movement.save()
            product.save()
            return True
        return False
    @classmethod
    def Unit_Sell(cls,user,product,lot,category,note,bool_no_category=False):
        if product and lot > 0:
            if category and bool_no_category == False:
                diff = category.unit_stored - lot
                if diff >= 0:
                    category.unit_stored = diff
                    category.unit_sold += lot
                else:
                    if lot==1 and category.pair_stored > 0 :
                        category.unit_stored+=1
                        category.pair_stored-=1
                    else:
                        return "E2"
                    #return "E0"    
            diff = product.unit_stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.unit_stored = diff
                    product.unit_sold += lot
                    amount=lot * product.unit_price
                    r_box.money += amount
                    
                    movement=cls(type="VP",user=user,extra_info_str=note,extra_info_bool=False,extra_info_int=product.unit_price,extra_info_int_1=product.unit_profit_worker,product=product,lot=lot,category=category)
                    if movement:
                        product.save()
                        movement.save()
                        if category:
                            category.save()
                        r_box.save()
                        if bool_no_category == True:
                            return "OK0"    
                        return True
                return False
            if lot==1 and product.pair_stored > 0 :
                product.unit_stored+=2
                product.pair_stored-=1
                return Movement.Unit_Sell(product,1,category,note,True)
            return "E2"                    
        return False
    @classmethod
    def Pair_Sell(cls,user,product,lot,category,note):
        if product and lot > 0:
            diff = product.pair_stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.pair_stored = diff
                    product.pair_sold += lot
                    amount=lot * product.unit_price
                    r_box.money += amount
                    if category:
                        diff = category.pair_stored - lot
                        if diff >= 0:
                            category.pair_stored = diff
                            category.pair_sold += lot
                        else:
                            return "E1"
                    movement=cls(type="VP",extra_info_int_1=product.pair_profit_worker,user=user,extra_info_str=note,extra_info_bool=True,extra_info_int=product.pair_price,product=product,lot=lot,category=category)
                    if movement:
                        product.save()
                        movement.save()
                        if category:
                            category.save()
                        r_box.save()
                        return True
                return False
            return "E0"
        return False
    @classmethod
    def Edit(cls,user,product,name,pair_stored,pair_sold,pair_price,pair_profit_worker,unit_stored,unit_sold,unit_price,unit_profit_worker,description,image):  
        str_info=""
        if product.name!=name:
            str_info+="Nombre: {} editado a {}<br>".format(product.name,name)
            product.name=name
        if product.pair:
            if pair_stored>=0 and pair_sold>=0  and pair_price>0  and pair_profit_worker>0:
                
                if product.pair_stored != pair_stored:
                    str_info+="Almacenados por Par: {} editado a {}<br>".format(product.pair_stored,pair_stored)
                    product.pair_stored=pair_stored
                if product.pair_sold != pair_sold:
                    str_info+="Vendidos por Par: {} editado a {}<br>".format(product.pair_sold,pair_sold)
                    product.pair_sold=pair_sold
                if product.pair_price != pair_price:
                    str_info+="Precio por Par: {} editado a {}<br>".format(product.pair_price,pair_price)
                    product.pair_price=pair_price
                if product.pair_profit_worker != pair_profit_worker:
                    str_info+="Ganancia por Par: {} editado a {}<br>".format(product.pair_profit_worker,pair_profit_worker)
                    product.pair_profit_worker=pair_profit_worker
            else:
                return  False    
        if unit_stored>=0 and unit_sold>=0  and unit_price>0  and unit_profit_worker>0:
            if product.unit_stored != unit_stored:
                str_info+="Almacenados por Unidad: {} editado a {}<br>".format(product.unit_stored,unit_stored)
                product.unit_stored=unit_stored
            if product.unit_sold != unit_sold:
                str_info+="Vendidos por Unidad: {} editado a {}<br>".format(product.unit_sold,unit_sold)
                product.unit_sold=unit_sold
            if product.unit_price != unit_price:
                str_info+="Precio por Unidad:{} editado a {}<br>".format(product.unit_price,unit_price)
                product.unit_price=unit_price
            if product.unit_profit_worker != unit_profit_worker:
                str_info+="Ganancia por Unidad: {} editado a {}<br>".format(product.unit_profit_worker,unit_profit_worker)
                product.unit_profit_worker=unit_profit_worker
            
            if image:
                str_info+="Imagen Editada<br>"
                product.image=image 
            if product.description!= description:
                str_info+="Descripcion Editada<br>"
                product.description=description
            movement=cls(type="eP",user=user,product=product,extra_info_str=str_info)
            if movement:
                try:
                    product.save()
                    movement.save()                   
                    return True
                except:
                    return "E0"
        return False
    @classmethod
    def Add(cls,user,product,lot,category,pair_action,note):
        if product and lot > 0:
            movement=cls(type="EP",user=user,product=product,lot=lot)
            if movement:
                if category:
                    movement.category=category
                movement.extra_info_bool=False
                movement.extra_info_int= (1 if pair_action else 0)
                movement.extra_info_str=note
                movement.save()
                product.confirm=False
                product.save()
                return True
        return False
    @classmethod
    def ConfirmAdd(cls,user,movement,lot,note):
        if movement and movement.product.confirm == False:
            if movement.product and movement.lot >= lot:
                movement_confirm=cls(type="cP",user=user,extra_info_str=note,product=movement.product,extra_info_int=movement.lot,lot=lot,category=movement.category)
                if movement_confirm:
                    if movement_confirm.product.pair and movement.extra_info_int==1:
                        movement_confirm.product.pair_stored += lot
                    else:
                        movement_confirm.product.unit_stored += lot
                    if movement.category:
                        if movement_confirm.product.pair and movement.extra_info_int==1:
                            movement_confirm.category.pair_stored += lot
                        else:
                            movement_confirm.category.unit_stored += lot
                        movement_confirm.category.save()
                    movement_confirm.product.confirm=True
                    movement.extra_info_bool=True
                    movement_confirm.product.save()
                    movement_confirm.save()
                    movement.save()
                    return True
        return False
    @classmethod
    def Unit_Sub(cls,user,product,lot,category,note):
        if product and lot > 0:
            diff= product.unit_stored - lot
            if diff >= 0:
                product.unit_stored = diff
                movement=cls(type="SP",user=user,extra_info_str=note,extra_info_bool=False,product=product,lot=lot,category=category)
                if movement:
                    if category:
                        #category=Category.objects.get(id=category_id)
                        diff = category.unit_stored - lot
                        if diff >= 0:
                            category.unit_stored = diff
                        else:
                            return "E1"
                    movement.save()
                    product.save()
                    if category:
                        category.save()
                    return True
                return False
            return "E0"
        return False
    @classmethod
    def Pair_Sub(cls,user,product,lot,category,note):
        if product and lot > 0:
            diff= product.pair_stored - lot
            if diff >= 0:
                product.pair_stored = diff
                movement=cls(type="SP",user=user,extra_info_str=note,extra_info_bool=True,product=product,lot=lot,category=category)
                if movement:
                    if category:
                        #category=Category.objects.get(id=category_id)
                        diff = category.pair_stored - lot
                        if diff >= 0:
                            category.pair_stored = diff
                        else:
                            return "E1"
                    movement.save()
                    product.save()
                    if category:
                        category.save()
                    return True
                return False
            return "E0"
        return False
    @classmethod
    def Unit_Refund(cls,user,product,lot,category,note):
        if product and lot > 0:
            diff = product.unit_sold - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    amount=lot * product.unit_price
                    r_box.money -= amount
                    if r_box.money >= 0:
                        product.unit_sold = diff
                        product.unit_stored += lot
                        movement=cls(type="rP",extra_info_int_1=product.unit_profit_worker,user=user,extra_info_str=note,extra_info_bool=False,extra_info_int=product.unit_price,product=product,lot=lot,category=category)
                        if movement:
                            if category:
                                #category=Category.objects.get(id=category_id)
                                diff = category.unit_sold - lot 
                                if diff >= 0:
                                    category.unit_sold = diff
                                    category.unit_stored += lot
                                    
                                else:
                                    return "E2"
                            if category:
                                category.save()
                            movement.save()
                            product.save()
                            r_box.save()
                            return True
                        return False
                    return "E1"
                return False
            return "E0"
        return False
    @classmethod
    def Pair_Refund(cls,user,product,lot,category,note):
        if product and lot > 0:
            diff = product.pair_sold - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    amount=lot * product.pair_price
                    r_box.money -= amount
                    if r_box.money >= 0:
                        product.pair_sold = diff
                        product.pair_stored += lot
                        movement=cls(type="rP",extra_info_int_1=product.pair_profit_worker,user=user,extra_info_str=note,extra_info_bool=True,extra_info_int=product.pair_price,product=product,lot=lot,category=category)
                        if movement:
                            if category:
                                #category=Category.objects.get(id=category_id)
                                diff = category.pair_sold - lot 
                                if diff >= 0:
                                    category.pair_sold = diff
                                    category.pair_stored += lot
                                else:
                                    return "E2"
                            if category:
                                category.save()
                            movement.save()
                            product.save()
                            r_box.save()
                            return True
                        return False
                    return "E1"
                return False
            return "E0"
        return False
    @classmethod
    def RetireMoney(cls,user,lot,note):
        if lot > 0:
            r_box=RegisteCash.objects.all().first()
            if r_box:
                dif= r_box.money - lot
                if dif >= 0:
                    r_box.money = dif
                    movement=cls(type="RD",user=user,extra_info_str=note,lot=lot)
                    if movement:
                        movement.save()
                        r_box.save()
                        return True
        return False
    @classmethod
    def AgregateMoney(cls,user,lot,note):
        if lot > 0:
            r_box=RegisteCash.objects.all().first()
            if r_box:
                r_box.money += lot
                movement=cls(type="AD",user=user,extra_info_str=note,lot=lot)
                if movement:
                    movement.save()
                    r_box.save()
                    return True
        return False
    @classmethod
    def AddCategory(cls,user,product,category_name,image):
        categorys=Category.objects.filter(product__id=product.id)
        category_nc=None
        if categorys:
            for cat_name in categorys:
                if cat_name.__str__() == category_name.__str__():
                    return "E0"
        else:
            if product.pair:
                category_nc=Category.create(product=product,name="Sin Categoría",pair_stored=product.pair_stored ,pair_sold=product.pair_sold )
            else:
                category_nc=Category.create(product=product,name="Sin Categoría",unit_stored=product.unit_stored ,unit_sold=product.unit_sold )
            
        category=Category.create(product=product,name=category_name)
        if category:
            if image:
                category.image=image
            movement=cls(type="AC",user=user,product=product,category=category)
            try:
                print("A")
                category.save()
                print("A")
                if category_nc:
                    category_nc.save()  
                movement.save()
                return True
            except:
                return "E0"
        return False
    @classmethod
    def RemoveCategory(cls,user,id,p_id):
        category=Category.objects.get(id=id)
        if category:
            categorys=Category.objects.filter(product__id=p_id)
            if categorys.count() == 2:
                for category_d in categorys:
                    category_d.delete()
            movement=cls(type="RC",user=user,product=category.product,extra_info_str=category.name)
            category.delete()
            movement.save()
            return True
        return False    



