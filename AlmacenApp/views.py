from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Product,RegisteCash,Movement
from .forms import FormProduc,FormLot
from datetime import datetime ,timedelta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def RedirectHomeView(request):
    return redirect("home")

def BasePost(request):
    print(request.path_info)
    print(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        if "Inicar_Sesion" in request.POST:
            formlogin=AuthenticationForm(request,data=request.POST)
            if formlogin.is_valid():
                nombre=formlogin.cleaned_data.get("username")
                contra=formlogin.cleaned_data.get("password")
                usuario=authenticate(username=nombre,password=contra)
                if usuario is not None:
                    login(request,usuario)
                    messages.success(request ,"Se ha iniciado session en la cuenta '%s' correctamente"  %  nombre)    
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                messages.error(request,"No se pudo inicar session en la cuenta '%s'" % nombre)
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        elif "CerrarSesion" in request.POST:
            user=request.user.username
            logout(request)
            messages.success(request,"La cuenta %s se ha cerrado correctamente" % user)    
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request,"Home.html")

def HomeView(request):
    date=datetime.now()
    movEP=Movement.objects.select_related('product').filter(date__day=date.day,type="EP").values_list('product__id',flat=True)
    movVP=Movement.objects.select_related('product').filter(date__day=date.day,type="VP").values_list('product__id',flat=True)
    movM=Movement.objects.filter(date__day=date.day).order_by('-date')[:5]
    idsEP=[]
    idsVP=[]
    for id in movEP:
        idsEP.append(id)
    for id in movVP:
        idsVP.append(id)
    productsEP=Product.objects.filter(pk__in=idsEP).values('name','id').order_by('name')
    productsVP=Product.objects.filter(pk__in=idsVP).values('name','id').order_by('name')
    return render(request,"Home.html",{"productsEP":productsEP,"productsVP":productsVP,"movM":movM})
    
def CajaView(request):
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

def AlmacenView(request):
    products = Product.objects.exclude(removed=True).filter(stored__gt=0).order_by('name')
    registe_cash=RegisteCash.objects.all().first()
    return render(request,"Almacen.html",{'products':products})

def ProductosView(request):
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
                        messages.success(request,"Se ha creado  el objeto %s correctamente"%name)
                        return render(request,"Productos.html",{'products':products})
                except IntegrityError:
                    messages.error(request,"Nose ha podido  crear, ya existe un objeto de nombre %s"% name)
                    return render(request,"Productos.html",{'products':products,"Error":"IntegrityError"})
        messages.error(request,"Ha ocurrido un error  insesperado")
        return render(request,"Productos.html",{'products':products})
    return render(request,"Productos.html",{'products':products})

def ProductoView(request,productoID):
    product=Product.objects.get(id=productoID)
    if product:
        movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:50]
        if request.method == "POST":
            #Form Editar
            if "EditProduct" in request.POST:
                edit_product=FormProduc(request.POST, request.FILES)
                if edit_product.is_valid():
                    name=edit_product.cleaned_data.get("name")
                    price=edit_product.cleaned_data.get("precio")
                    description=edit_product.cleaned_data.get("descripcion")
                    image=edit_product.cleaned_data.get("imagen")
                    try:
                        if Movement.Edit(product,name,price,description,image):
                            messages.success(request,"Se ha editado el producto %s correctamente"%name)
                            return render(request,"Producto.html",{'product':product,"movements":movements})
                    except IntegrityError:
                        product=Product.objects.get(id=productoID)
                        messages.error(request,"No se ha podido editar, ya existe un objeto de nombre %s"% name)
                        return render(request,"Producto.html",{'product':product,"movements":movements})
                messages.error(request,"Ha ocurrido un errpr inescperado")
                return render(request,"Producto.html",{'product':product,"movements":movements})
            #Form Vender
            elif "SellProduct" in request.POST:
                sell_product=FormLot(request.POST)
                if sell_product.is_valid():
                    lot_sell=sell_product.cleaned_data.get("cantidad")
                    if Movement.Sell(product,lot_sell):
                        messages.success(request,"Se han vendido {} {} con un importe de {}$".format(lot_sell,product.name,product.price*lot_sell))
                        return render(request,"Producto.html",{'product':product,"movements":movements})
                    messages.error(request,"No se ha podido vender {}, solo quedan {} productos almacenados".format(lot_sell,product.stored))
                return render(request,"Producto.html",{'product':product, "movements":movements})
            #Form Eliminar
            elif "RemoveProduct" in request.POST:
                name=product.name
                if Movement.Remove(product):
                    messages.warning(request,"Se ha removido el producto %s"%name)
                    return redirect('productos')
                messages.error(request,"No se ha podido remover el producto %s"%name)
                return render(request,"Producto.html",{'product':product ,"movements":movements})
            #Form Agregar
            elif "AddProduct" in request.POST:
                add_product=FormLot(request.POST)
                if add_product.is_valid():
                    lot_add=add_product.cleaned_data.get("cantidad")
                    if lot_add>= 0:
                        if Movement.Add(product,lot=lot_add):
                            messages.success(request,"Se han agregado {} {} correctamente".format(lot_add,product.name))
                            return render(request,"Producto.html",{'product':product, "movements":movements})
                messages.error(request,"No se han podido insertar {} {}".format(lot_add,product.name))
                return render(request,"Producto.html",{'product':product ,"movements":movements})
            elif "SubProduct" in request.POST:
                sub_product=FormLot(request.POST)
                if sub_product.is_valid():
                    lot_sub=sub_product.cleaned_data.get("cantidad")
                    if lot_sub >= 0:
                        if Movement.Sub(product,lot=lot_sub):
                            messages.success(request,"Se han quitado {} {} correctamente".format(lot_sub,product.name))
                            return render(request,"Producto.html",{'product':product, "movements":movements})
                messages.error(request,"No se han podido quitar {} {}".format(lot_sub,product.name))
                return render(request,"Producto.html",{'product':product ,"movements":movements})
            elif "RefundProduct" in request.POST: 
                refund_product=FormLot(request.POST)
                if refund_product.is_valid():
                    lot_refund=refund_product.cleaned_data.get("cantidad")
                    if lot_refund > 0:
                        if Movement.Refund(product,lot=lot_refund):
                            messages.success(request,"Se han reembolsado {} {} con un importe de {}$".format(lot_refund,product.name,lot_refund*product.price))
                            return render(request,"Producto.html",{'product':product, "movements":movements})
                messages.error(request,"No se han podido reembolsar {} {}".format(lot_add,product.name))
                return render(request,"Producto.html",{'product':product ,"movements":movements})

        return render(request,"Producto.html",{'product':product ,"movements":movements})
    else:
        return redirect('productos')        

def TransaccionesView(request):
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
    return render(request,"Transacciones.html",{"date_end_filter":date_end_filter,"date_start_filter":date_start_filter,"date_day_filter":date_day_filter,"date_today":datetime.today().strftime("%Y-%m-%d"),"date_today_max":date_today_max.strftime("%Y-%m-%d"),"movements":movements,"product_filter":product_filter,"type_filter":type_filter,"date_filter":date_filter,"products":products})

