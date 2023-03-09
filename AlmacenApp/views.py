from django.shortcuts import render,redirect,HttpResponse
from .models import Product,RegisteCash,Movement,Category,MChoise
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormProduc,FormLot,FormImg
from datetime import datetime ,timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q

def RedirectHomeView(request):
    return redirect("home")

def BasePost(request):
    try:
        if request.method == "POST":
            if "Inicar_Sesion" in request.POST:
                formlogin=AuthenticationForm(request,data=request.POST)
                if formlogin.is_valid():
                    nombre=formlogin.cleaned_data.get("username")
                    contra=formlogin.cleaned_data.get("password")
                    usuario=authenticate(username=nombre,password=contra)
                    if usuario is not None:
                        login(request,usuario)
                        messages.success(request ,"Se ha iniciado en la cuenta '%s' correctamente"  %  nombre)    
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                    messages.error(request,"No se pudo inicar en la cuenta '%s'" % nombre)
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            elif "CerrarSesion" in request.POST:
                user=request.user.username
                logout(request)
                messages.success(request,"La cuenta %s se ha cerrado correctamente" % user)    
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        return render(request,"Home.html")
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('productos')

def HomeView(request):
    try:
        date=datetime.now() 
        movEP=Movement.objects.select_related('product').filter(date__day=date.day,type="EP").values_list('product__id',flat=True)
        movVP=Movement.objects.select_related('product').filter(date__day=date.day,type="VP").values_list('product__id',flat=True)
        movM=Movement.objects.filter(date__day=date.day).order_by('-date')[:5]
        idsEP=[]
        idsVP=[]
        if movEP:
            for id in movEP:
                idsEP.append(id)
        if movVP:
            for id in movVP:
                idsVP.append(id)
        productsEP=Product.objects.filter(pk__in=idsEP).values('name','id').order_by('name')
        productsVP=Product.objects.filter(pk__in=idsVP).values('name','id').order_by('name')
        return render(request,"Home.html",{"productsEP":productsEP,"productsVP":productsVP,"movM":movM})
    except :
        pass
    return HttpResponse("Ha ocurrido un error insesperado , contacte con los administradores")

def CajaView(request):
    try:
        movements=Movement.objects.filter(Q(type="VP") | Q(type="RD") | Q(type="rP")).order_by('-date')[:50]
        if "RetireProduct" in request.POST:
            retire_product=FormLot(request.POST)
            if retire_product.is_valid():
                lot_retire=retire_product.cleaned_data.get("cantidad")
                if lot_retire >= 0:
                    if Movement.Retire(lot=lot_retire):
                        messages.success(request,"Se ha retirado {}$ correctamente".format(lot_retire))
                        return render(request,"Caja.html",{"movements":movements})
            messages.error(request,"No se han podido retirar {}$".format(lot_retire))
            return render(request,"Caja.html",{"movements":movements})
        return render(request,"Caja.html",{"movements":movements})
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def AlmacenView(request):
    try:
        products = Product.objects.exclude(removed=True).filter(stored__gt=0).order_by('name')
        return render(request,"Almacen.html",{'products':products})
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def ProductosView(request):
    try:
        products = Product.objects.exclude(removed=True).order_by('name')   
        if request.method == "POST":
            if "CrearProducto" in request.POST:
                crear_form=FormProduc(request.POST,request.FILES)
                if crear_form.is_valid():
                    name=crear_form.cleaned_data.get("name").__str__().capitalize()
                    price=crear_form.cleaned_data.get("precio") 
                    image=crear_form.cleaned_data.get("imagen")
                    description=crear_form.cleaned_data.get("descripcion")
                    try:
                        if Movement.Create(name,price,description,image):
                            crear_form=FormProduc()
                            product=Product.objects.exclude(removed=True).get(name=name)
                            categorys=Category.objects.filter(product__id=product.id).order_by("name")
                            movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:50]
                            messages.success(request,"Se ha creado  el objeto %s correctamente"%name)
                            return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys}) 
                    except IntegrityError:
                        messages.error(request,"Nose ha podido  crear, ya existe un objeto de nombre %s"% name)
                        return render(request,"Productos.html",{'products':products})
            messages.error(request,"Ha ocurrido un error  insesperado")
            return render(request,"Productos.html",{'products':products})
        return render(request,"Productos.html",{'products':products})
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')

def ProductoView(request,productoID):
    try:
        product=Product.objects.exclude(removed=True).get(id=productoID)
        if product:
            categorys=Category.objects.filter(product__id=product.id).order_by("name")
            i=0
            for categ in categorys:
                if(categ.image):
                    i+=1

            movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:50]
            def NormalPageProduct():
                return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)}) 
            def ErrorProduct(text):
                messages.error(request,text)
                return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)}) 
            def SuccessProduct(text):
                messages.success(request,text)
                return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys,"categorysImgI":range(i)})
            def WarningProduct(text):
                messages.warning(request,text)
                # return render(request,"Producto.html",{'product':product,"movements":movements,"categorys":categorys})
                return redirect('home') 
            if request.method == "POST":
                #Form Editar
                if "EditProduct" in request.POST:
                    edit_product=FormProduc(request.POST, request.FILES)
                    if edit_product.is_valid():
                        name=edit_product.cleaned_data.get("name")
                        price=edit_product.cleaned_data.get("precio")
                        description=edit_product.cleaned_data.get("descripcion")
                        image=edit_product.cleaned_data.get("imagen")
                        print(image)
                        try:
                            if Movement.Edit(product,name,price,description,image):
                                return SuccessProduct("Se ha editado el producto %s correctamente" %name)
                        except IntegrityError:
                            product=Product.objects.exclude(removed=True).get(id=productoID)
                            return ErrorProduct("No se ha podido editar, ya existe un objeto de nombre %s" %name)
                    return ErrorProduct("Ha ocurrido un errpr inescperado")    
                #Form Vender
                elif "SellProduct" in request.POST:
                    sell_product=request.POST.dict()
                    lot_sell=int(sell_product.get("cantidad"))
                    category_id=sell_product.get("CategorySelect")
                    ms=Movement.Sell(product,lot_sell,category_id)
                    if ms==True:
                        return SuccessProduct("Se han vendido {} {} con un importe de {}$".format(lot_sell,product.name,product.price*lot_sell))
                    elif ms==None:
                        category=Category.objects.get(id=category_id) 
                        return ErrorProduct("No se ha podido vender, en la categoría {} solo quedan {} productos almacenados".format(category.name,category.stored))
                    return ErrorProduct("No se ha podido vender {}, solo quedan {} productos almacenados".format(lot_sell,product.stored))  
                    #return ErrorProduct("Ha ocurrido un errpr inescperado")   
                #Form Eliminar
                elif "RemoveProduct" in request.POST:
                    name=product.name
                    if Movement.Remove(product):
                        return WarningProduct("Se ha removido el producto {}, contacte con el administrador del proyecto para usar nuevamante este producto".format(name))
                    return ErrorProduct("No se ha podido remover el producto %s"%name)
                #Form Agregar
                elif "AddProduct" in request.POST:
                    add_product=request.POST.dict()
                    lot_add=int(add_product.get("cantidad"))
                    category_id=add_product.get("CategorySelect")
                    if lot_add >= 0:
                        if Movement.Add(product,lot=lot_add,category_id=category_id):
                            return SuccessProduct("Se han agregado {} {} correctamente".format(lot_add,product.name))
                    return ErrorProduct("No se han podido insertar {} {}".format(lot_add,product.name))
                #Form Quitar
                elif "SubProduct" in request.POST:
                    sub_product=request.POST.dict()
                    lot_sub=int(sub_product.get("cantidad"))
                    category_id=sub_product.get("CategorySelect")
                    if lot_sub >= 0:
                        ms=Movement.Sub(product,lot=lot_sub,category_id=category_id)
                        if ms == True:
                            return SuccessProduct("Se han quitado {} {} correctamente".format(lot_sub,product.name))
                        elif ms==None:
                            category=Category.objects.get(id=category_id) 
                            return ErrorProduct("No se han podido quitar, la categoría {} solo tiene {} productos almcenados".format(category.name,category.stored))
                    return ErrorProduct("No se han podido quitar {} {}".format(lot_sub,product.name))
                #Form Reembolsar
                elif "RefundProduct" in request.POST: 
                    refund_product=request.POST.dict()
                    lot_refund=int(refund_product.get("cantidad"))
                    category_id=refund_product.get("CategorySelect")
                    if lot_refund > 0:
                        rf=Movement.Refund(product,lot=lot_refund,category_id=category_id)
                        if rf == True:
                            return SuccessProduct("Se han reembolsado {} {} con un importe de {}$".format(lot_refund,product.name,lot_refund*product.price))
                        elif rf == None:
                            return ErrorProduct("No hay suficiente dinero en caja para reembolsar {} {}".format(lot_refund,product.name))
                        elif "None" in rf:
                            category=Category.objects.get(id=category_id) 
                            return ErrorProduct("No se ha podido  reembolsar, la categoría {} solo tiene {} productos vendidos".format(category.name,category.sold))
                    return ErrorProduct("No se han podido reembolsar {} {}".format(lot_refund,product.name))
                #Form Agregar Categoría
                elif "AddCategory" in request.POST: 
                    add_category=FormImg(request.POST,request.FILES)
                    if add_category.is_valid():
                        name=add_category.cleaned_data.get("name")         
                        image=add_category.cleaned_data.get("imagen")
                        rf=Movement.AddCategory(product,name,image)
                        if rf == True:
                            categorys=Category.objects.filter(product__id=product.id).order_by("name")
                            i=0
                            for categ in categorys:
                                if(categ.image):
                                    i+=1
                            return SuccessProduct("Se ha creado la categoría {} correctamente".format(name))
                        elif rf == None:
                            return ErrorProduct("Ya existe la categoría {}".format(name))
                    return ErrorProduct("No se ha podido  crear la categoría {}".format(name))     
                #Form Eliminar Categoría
                elif "RemoveCategory" in request.POST: 
                    remove_category=request.POST.dict()
                    id=remove_category.get("RemoveCategorySelect")
                    category=Category.objects.get(id=id)
                    rf=Movement.RemoveCategory(id=id,p_id=product.id)
                    if rf == True:
                        categorys=Category.objects.filter(product__id=product.id).order_by("name")
                        i=0
                        for categ in categorys:
                            if(categ.image):
                                i+=1
                        return SuccessProduct("Se ha eliminado la categoría {} correctamente".format(category.name))
                    return ErrorProduct("No se ha podido eliminar la categoría {}".format(category.name))
            return NormalPageProduct()
    except ObjectDoesNotExist:
        messages.error(request,"Error, producto inexistente")
    
    return redirect('productos')        

def TransaccionesView(request):
    try:
        type_filter="NF"
        product_filter="NF"
        date_filter="NF"
        date_day_filter=datetime.today().strftime("%Y-%m-%d")
        date_start_filter=date_day_filter
        date_end_filter=date_day_filter
        q=Q()
        if request.method  == "POST":
            if "FilterMovement" in request.POST:
                filter_movement=request.POST.dict()
                type_filter=filter_movement.get("TypeFilter")
                product_filter=filter_movement.get("ProductFilter")
                date_filter=filter_movement.get("FilterDate")
                if date_filter ==  "DD":
                    date_day_filter=filter_movement.get("FilterDateDay")
                    print(date_day_filter)
                    q = q & Q(date__date=date_day_filter)
                elif date_filter ==  "RD":
                    date_start_filter=filter_movement.get("FilterDateStart")
                    start_date=date_start_filter
                    date_end_filter=filter_movement.get("FilterDateEnd")
                    end_date=date_end_filter
                    q = q & Q(date__range=(start_date,end_date))
                if product_filter != "NF":
                    q = q & Q(product__id=product_filter)
                    product_filter=int(product_filter)
                if type_filter != "NF":
                    q = q & Q(type=type_filter)
        movements=Movement.objects.filter(q).order_by('-date')[:50] 
        products=Product.objects.all().exclude(removed=True).values("id","name")
        date_today_max =datetime.today() + timedelta(days=1)
        return render(request,"Transacciones.html",{"MChoise":MChoise,"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"date_filter":date_filter,"products":products})
    except:
        messages.error(request,"Algo ha salido mal")    
    return redirect('home')
