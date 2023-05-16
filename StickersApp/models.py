from django.db import models
from datetime  import datetime
#from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser


class UsEr(AbstractUser):
    is_worker=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    image=models.ImageField(blank=True,null=True,upload_to='usuarios',default="no_user_imagen.jpg", height_field=None, width_field=None, max_length=None)
     
class Visits(models.Model):
    total_visits=models.IntegerField(default=0)
    def __str__(self):
        return self.total_visits.__str__()

class RegisteCash(models.Model):
    money=models.IntegerField(default=0)
    def __str__(self):
        return self.money.__str__()

class SummaryDate(models.Model):
    start_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    active=models.BooleanField(default=False)
    def __str__(self):
        return "Active-"+self.start_date.strftime("%d-%m-%y %H:%M")+" ~ "+self.end_date.strftime("%d-%m-%y %H:%M") if self.active else "Desactive"


class Category(models.Model):
    name=models.CharField(max_length=30,unique=True)
    #image=models.ImageField(blank=True,null=True,upload_to='categorias',default="no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    def __str__(self) -> str:
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=30,unique=True)
    category=models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.name

class SubCategoryColor(models.Model):
    name=models.CharField(max_length=30,unique=True)
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    #i_d=models.CharField(max_length=4)
    name=models.CharField(max_length=40, unique=True)
    pair=models.BooleanField(default=False)
    purchase_price=models.IntegerField(default=0)
    unit_price=models.IntegerField(default=0)
    unit_profit=models.IntegerField(default=0)
    unit_profit_worker=models.IntegerField(default=0)
    pair_price=models.IntegerField(default=0,blank=True,null=True)
    pair_profit=models.IntegerField(default=0,blank=True,null=True)
    pair_profit_worker=models.IntegerField(default=0)
    image=models.ImageField(blank=True,null=True,upload_to='productos',default="no_imagen.jpg", height_field=None, width_field=None, max_length=None)
    unit_stored=models.IntegerField(blank=True,default=0)
    pair_stored=models.IntegerField(blank=True,default=0)
    unit_sold=models.IntegerField(blank=True,default=0)
    pair_sold=models.IntegerField(blank=True,default=0)
    description=models.CharField(max_length=100,blank=True)
    removed=models.BooleanField(default=False)
    confirm=models.BooleanField(default=True)
    
    #category=models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    sub_category=models.ForeignKey(SubCategory,null=True,blank=True,on_delete=models.DO_NOTHING)
    color=models.ForeignKey(SubCategoryColor,null=True,blank=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
    
    
MChoise = [
    
    ('AD','Agregado de Dinero'),
    ('EP','Agregado de Productos'),
    ("CC","Creado de Categoría"),
    ("Cc","Creado de Color"),
    ("CS","Creado de SubCategoría"),
    ("CM","Cierre de Mes"),
    ("cP","Confirmado de Producto"),
    ('CP','Creado de Producto'),
    ("eC","Editado de Categoría"),
    ("eP","Editado de Producto"),
    ("eS","Editado de SubCategoría"),
    ("eT","Editado toda SubCategoría"),
    ('eU','Editado de Usuario'),
    ('SP','Quitado de Productos'),
    ("rP","Reembolso de Productos"),
    ("RP","Removido de Producto"),
    ('RD','Retiro de Dinero'),
    ("VP","Venta de Productos"),
    
    ]



class Movement(models.Model):
    type=models.CharField(max_length=2,choices=MChoise)
    date=models.DateTimeField(default=datetime.now,blank=True)
    lot=models.IntegerField(default=0)
    extra_info_str=models.CharField(max_length=100,null=True,blank=True)
    extra_info_int=models.IntegerField(default=0)
    extra_info_int_1=models.IntegerField(default=0)
    extra_info_int_2=models.IntegerField(default=0)
    extra_info_bool=models.BooleanField(default=False)
    user = models.ForeignKey(UsEr,on_delete=models.SET_NULL,null=True,blank=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True,related_name="product")
    def __str__(self):
        return "M"+self.id.__str__()+"-"+self.type+"-"+self.date.date().__str__()

    @classmethod
    def Create_Product(cls,user,name,pair,unit_price,unit_profit,unit_profit_worker,pair_price,pair_profit,pair_profit_worker,description,image,subcategory,color,purchase_price):
        if unit_price > 0  and unit_profit_worker >= 0  and unit_profit >= 0 :
            if pair == True :
                if pair_price > 0 and pair_profit >= 0 and pair_profit_worker >= 0 :
                    pass
                else:
                    return False
            product=Product(
                name=name,
                pair=pair,
                unit_price=unit_price,
                unit_profit=unit_profit,
                unit_profit_worker=unit_profit_worker,
                pair_price=pair_price,
                pair_profit=pair_profit,
                pair_profit_worker=pair_profit_worker,
                description=description,
                sub_category=subcategory,
                purchase_price=purchase_price,
                )
            if color:
                product.color=color
            str_info="Nombre:{}<br>Por Pares:{}<br>{}{}<br>Category:{}<br>SubCategory:{}{}<br>Descripción:{}<br>Imagen:{}<br>".format(
                name,
                "Si" if pair else "No",
                "Precio por Par:{}<br>Gannacia por Par:{}<br>Pago a Trabajador por Par:{}<br>".format(pair_price,pair_profit,pair_profit_worker) if pair else "",
                "Precio por Unidad:{}<br>Ganancia por Unidad:{}<br>Pago a Trabajador por Unidad:{}".format(unit_price,unit_profit,unit_profit_worker),
                subcategory.category.name,
                subcategory.name,
                "<br>Color:{}".format(color.name) if color else "",
                "Si" if len(description.__str__()) > 0 else "No",
                "Si" if image else "No",
                
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
                    except Exception as e:
                        return "E0"
        return False
    @classmethod
    def create_category(cls,name,user):
        try:
            category=Category(name=name)
            #if image:
            #    category.image=image
            movement=cls(type="CC",extra_info_str=name,user=user)
            category.save()
            movement.save()
            return True
        except Exception as e:
            pass                
        return False
    @classmethod 
    def edit_category(cls,name,category,user):
        str_info=""
        if category.name!=name:
            str_info+="Nombre: {} editado a {}<br>".format(category.name,name)
            category.name=name
        #if image:
        #    str_info+="Imagen Editada<br>"
        #    category.image=image 
        movement=cls(type="eC",user=user,extra_info_str=str_info)
        if movement:
            try:
                category.save()
                movement.save()                   
                return True
            except:
                return False
    @classmethod 
    def edit_sub_category(cls,name,subcategory,user):
        str_info=""
        if subcategory.name!=name:
            str_info+="Nombre: {} editado a {}<br>".format(subcategory.name,name)
            subcategory.name=name
        movement=cls(type="eS",user=user,extra_info_str=str_info)
        if movement:
            try:
                subcategory.save()
                movement.save()                   
                return True
            except:
                return False
    @classmethod
    def create_sub_category(cls,name,category,user):
        try:
            subcategory=SubCategory(name=name,category=category)
            movement=cls(type="CS",extra_info_str=name,user=user)
            subcategory.save()
            movement.save()
            return True
        except Exception as e:
            pass    
        return False
    @classmethod
    def create_color(cls,name,user):
        try:
            color=SubCategoryColor(name=name)
            movement=cls(type="Cc",extra_info_str=name,user=user)
            color.save()
            movement.save()
            return True
        except Exception as e:
            pass    
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
    def Unit_Sell(cls,user,product,lot,note,bool_div_par=False):
        if product and lot > 0:
            diff = product.unit_stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.unit_stored = diff
                    product.unit_sold += lot
                    amount=lot * product.unit_price
                    r_box.money += amount
                    movement=cls(type="VP",user=user,extra_info_str=note,extra_info_bool=False,extra_info_int=product.unit_price,extra_info_int_1=product.unit_profit,extra_info_int_2=product.unit_profit_worker,product=product,lot=lot)
                    if movement:
                        product.save()
                        movement.save()
                        
                        r_box.save()
                        user.save()
                        if bool_div_par == True:
                            return "OK0"
                        return True
                return False
            if product.pair and lot==1 and product.pair_stored > 0 :
                product.unit_stored+=2
                product.pair_stored-=1
                return Movement.Unit_Sell(user=user,product=product,lot=1,note=note,bool_div_par=True)
            return "E2"                    
        return False
    @classmethod
    def Pair_Sell(cls,user,product,lot,note):
        if product and lot > 0:
            diff = product.pair_stored - lot 
            if diff >= 0:
                r_box=RegisteCash.objects.all().first()
                if r_box:
                    product.pair_stored = diff
                    product.pair_sold += lot
                    amount=lot * product.pair_price
                    r_box.money += amount
                    movement=cls(type="VP",user=user,extra_info_str=note,extra_info_bool=True,extra_info_int=product.pair_price,extra_info_int_1=product.pair_profit,extra_info_int_2=product.pair_profit_worker,product=product,lot=lot)
                    if movement:
                        product.save()
                        movement.save()
                        r_box.save()
                        user.save()
                        return True
                return False
            return "E0"
        return False
    @classmethod
    def Edit(cls,user,product,name,purchase_price,pair_price,pair_profit,pair_profit_worker,unit_price,unit_profit,unit_profit_worker,description,image,color):  
        str_info=""
        if product.name!=name:
            str_info+="Nombre: {} editado a {}<br>".format(product.name,name)
            product.name=name
        if product.purchase_price!=purchase_price:
            str_info+="Precio de Compra: {} editado a {}<br>".format(product.purchase_price,purchase_price)
            product.purchase_price=purchase_price
        
        if product.pair:
            if pair_price>0  and pair_profit_worker>0 and pair_profit>0:
                if product.pair_price != pair_price:
                    str_info+="Precio por Par: {} editado a {}<br>".format(product.pair_price,pair_price)
                    product.pair_price=pair_price
                if product.pair_profit != pair_profit:
                    str_info+="Ganancia por Par: {} editado a {}<br>".format(product.pair_profit,pair_profit)
                    product.pair_profit=pair_profit
                if product.pair_profit_worker != pair_profit_worker:
                    str_info+="Pago a Trabajdor por Par: {} editado a {}<br>".format(product.pair_profit_worker,pair_profit_worker)
                    product.pair_profit_worker=pair_profit_worker
                
                
            else:
                return  False    
        if unit_price>0  and unit_profit_worker>0:
            if product.unit_price != unit_price:
                str_info+="Precio por Unidad:{} editado a {}<br>".format(product.unit_price,unit_price)
                product.unit_price=unit_price
            if product.unit_profit != unit_profit:
                str_info+="Ganancia por Unidad: {} editado a {}<br>".format(product.unit_profit,unit_profit)
                product.unit_profit=unit_profit
            if product.unit_profit_worker != unit_profit_worker:
                str_info+="Pago a Trabajador por Unidad: {} editado a {}<br>".format(product.unit_profit_worker,unit_profit_worker)
                product.unit_profit_worker=unit_profit_worker
           
           
            if image:
                str_info+="Imagen Editada<br>"
                product.image=image 
            
            
            if product.color:
                if color:
                    if product.color != color:
                        product.name=product.name.replace(product.color.name.lower(),color.name.lower())    
                        str_info+="Color: {} editado a {}<br>".format(product.color.name,color.name)
                        product.color=color
                else:
                    product.name=product.name.replace(product.color.name.lower(),"")[:-1]   
                    str_info+="Color eliminado<br>"
                    product.color=None
            else:
                if color:
                    product.name+=" {}".format(color.name.lower()) 
                    str_info+="Color: editado a {}<br>".format(color.name)
                    product.color=color
            
            if product.description!= description:
                str_info+="Descripción Editada<br>"
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
    def EditUser(cls,user,username=None,password=None,image=None,user_activ_desact=None):
        str_info=""
        if user_activ_desact:
            user_activ_desact.is_active=not user_activ_desact.is_active
            str_info="{} de Usuario".format("Activado" if user_activ_desact.is_active==True else "Desactivado")
            
        else:
            if user.username!=username:
                str_info+="Nombre: {} editado a {}<br>".format(user.username,username)
                user.username=username
            if password:
                user.set_password(password)
                str_info+="Contraseña: editada <br>"
            if image:
                str_info+="Imagen Editada<br>"
                user.image=image
        movement=cls(type="eU",user=user,extra_info_str=str_info)
        if movement:
            try:
                if user_activ_desact:
                    user_activ_desact.save()
                else:
                    user.save()
                movement.save()                   
                return True
            except:
                return "E0"
    @classmethod
    def edit_price_products(cls,products,purchase_price,user,unit_price,pair_profit,unit_profit,unit_profit_worker,pair_price,pair_profit_worker):
        str_info=""
        if purchase_price:
            str_info+="Precio de Compra editado a {}<br>".format(purchase_price)
        if unit_price:
            str_info+="Precio por Unidad a {}<br>".format(unit_price)
        if unit_profit:
            str_info+="Ganancia por Unidad editado a {}<br>".format(unit_profit)
        if unit_profit_worker:
            str_info+="Pago al Trabajador por Unidad editado a {}<br>".format(unit_profit_worker)
        if pair_price:
            str_info+="Precio por Par editado a {}<br>".format(pair_price)
        if pair_profit:
            str_info+="Ganancia por Par editado a {}<br>".format(pair_profit)
        if pair_profit_worker:
            str_info+="Pago al Trabajador por Par editado a {}<br>".format(pair_profit_worker)
        movement=cls(type="eT",user=user,extra_info_str=str_info)
        try:
            for product in products:
                if purchase_price:
                    product.purchase_price=purchase_price
                if unit_price:
                    product.unit_price=unit_price
                if unit_profit:
                    product.unit_profit=unit_profit
                if unit_profit_worker:
                    product.unit_profit_worker=unit_profit_worker
                if product.pair:
                    if pair_price:
                        product.pair_price=pair_price
                    if pair_profit:
                        product.pair_profit=pair_profit
                    if pair_profit_worker:
                        product.pair_profit_worker=pair_profit_worker
                product.save()
            movement.save()
            return True
        except Exception as e:
            print(e)
            return "E0"
    @classmethod
    def Add(cls,user,product,lot,lot_1,pair_action,note):
        if product and lot>0  :
            extra_info_int=None
            if pair_action:
                extra_info_int=1
                movement=cls(type="EP",user=user,product=product,lot=lot)
                if lot_1!=None and lot_1 > 0:
                    extra_info_int=2
                    movement.extra_info_int_1=lot_1
                
            else:  
                extra_info_int=0
                movement=cls(type="EP",user=user,product=product,lot=lot)
            if movement:
                movement.extra_info_bool=False
                movement.extra_info_int= extra_info_int
                movement.extra_info_str=note
                movement.save()
                product.confirm=False
                product.save()
                return True
        return False
    @classmethod
    def ConfirmAdd(cls,user,movement,note):
        if movement and movement.product:
            if movement.product.confirm == False and movement.type=="EP" and movement.extra_info_bool==False:
                
                movement_confirm=None
                if (movement.extra_info_int==1 or movement.extra_info_int==0 ) and movement.lot>0 :
                    movement_confirm=cls(type="cP",user=user,extra_info_str=note,product=movement.product,lot=movement.lot,extra_info_int=movement.extra_info_int)
                elif movement.extra_info_int==2 and movement.lot>0 and  movement.extra_info_int_1 > 0 :
                    movement_confirm=cls(type="cP",user=user,extra_info_str=note,product=movement.product,lot=movement.lot,extra_info_int=movement.extra_info_int,extra_info_int_1=movement.extra_info_int_1)
                
                if movement_confirm:
                    
                    if  movement.extra_info_int==1:
                        movement_confirm.product.pair_stored += movement.lot
                    elif  movement.extra_info_int==2:
                        movement_confirm.product.pair_stored += movement.lot
                        movement_confirm.product.unit_stored += movement.extra_info_int_1
                    elif movement.extra_info_int==0:
                        movement_confirm.product.unit_stored += movement.lot
                    else:
                        return False
                    #movement_confirm.product.confirm=True
                    movement.extra_info_bool=True
                    movement_confirm.product.save()
                    movement_confirm.save()
                    movement.save()
                    return True
        return False
    @classmethod
    def Sub(cls,user,product,lot,note,pair):
        if product and lot > 0:
            diff= product.pair_stored - lot
            if diff >= 0:
                product.pair_stored = diff
                movement=cls(type="SP",user=user,extra_info_str=note,extra_info_bool=pair,product=product,lot=lot)
                
                if movement:
                
                    movement.save()
                    product.save()
                    
                    return True
                return False
            return "E0"
        return False
    @classmethod
    def Refund(cls,user,product,movement,note):
        if product and product.id == movement.product.id and movement.type=="VP":
            if movement.extra_info_bool:
                diff = product.pair_sold - movement.lot 
                if diff >= 0:
                    r_box=RegisteCash.objects.all().first()
                    if r_box:
                        amount=movement.lot * product.pair_price
                        r_box.money -= amount
                        if r_box.money >= 0:
                            product.pair_sold = diff
                            product.pair_stored += movement.lot
                            movement_refund=cls(type="rP",extra_info_int_1=product.pair_profit,extra_info_int_2=product.pair_profit_worker,user=user,extra_info_str=note,extra_info_bool=True,extra_info_int=product.pair_price,product=product,lot=movement.lot)
                            if movement_refund:
                                movement_refund.extra_info_str+="<br><div class='text-success'>Id de Operación Reembolsada: {}</div>".format(movement.id)
                                movement_refund.save()
                                movement.extra_info_str+="<br><div class='text-danger'>Reembolsado</div>"
                                movement.save()
                                product.save()
                                r_box.save()
                                user.save()
                                return True
                            return False
                        return "E1"
                    return False
                return "E0"
            else:
                diff = product.unit_sold - movement.lot 
                if diff >= 0:
                    r_box=RegisteCash.objects.all().first()
                    if r_box:
                        amount=movement.lot * product.unit_price
                        r_box.money -= amount
                        if r_box.money >= 0:
                            product.unit_sold = diff
                            product.unit_stored += movement.lot
                            movement_refund=cls(type="rP",extra_info_int_2=product.unit_profit_worker,extra_info_int_1=product.unit_profit,user=user,extra_info_str=note,extra_info_bool=False,extra_info_int=product.unit_price,product=product,lot=movement.lot)
                            if movement_refund:
                                movement_refund.extra_info_str+="<br><div class='text-success'>Id de Operación Reembolsada: {}</div>".format(movement.id)
                                movement_refund.save()
                                movement.extra_info_str+="<br><div class='text-danger'>Reembolsado</div>"
                                movement.save()
                                product.save()
                                r_box.save()
                                user.save()
                                return True
                            return False
                        return "E1"
                    return False
                return "E0"
        return False
    @classmethod
    def CloseMonth(cls,user,note,date_start,date_end,next_date_end,total_money,total_profit,total_profit_worker):
        if user.is_admin:
            r_box=RegisteCash.objects.all().first()
            if r_box:
                movement=cls(
                            type="CM",
                            user=user,
                            lot=r_box.money,
                            extra_info_int=total_money,
                            extra_info_int_1=total_profit,
                            extra_info_int_2=total_profit_worker,
                            extra_info_str="Mes:{}~{} {} {}".format(
                                date_start.strftime("%d-%m-%y"),
                                date_end.strftime("%d-%m-%y"),
                                "<br>Fecha De Cierre:"+datetime.today().strftime("%d-%m-%y"),
                                ("<br>Nota:"+note.__str__()) if note else "",
                                )
                            )
                if movement:
                    summary_date=SummaryDate.objects.first()
                    if summary_date:
                        movement.save()
                        summary_date.start_date=datetime.now()
                        summary_date.end_date=next_date_end
                        summary_date.save()
                        
                        r_box.money = 0
                        r_box.save()
                        return True
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