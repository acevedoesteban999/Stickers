from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Product,RegisteCash,Movement
from .forms import FormEditar,FormVender
from datetime import datetime 
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
    
    #mov=Movement.objects.filter(date__year=, date__month=today.month, date__day=today.day)

    
    #products0=Product.objects.all()
    #start_date = datetime.date(2005, 1, 1)
    #end_date = datetime.date(2024, 3, 31)
    #mo=Movement.objects.filter(date__range=(start_date, end_date),type="AP")
    #mov=Movement.objects.filter(date__date__gt=datetime.date(2023,2,15),type="AP")
    #print(mov)
    return render(request,"Home.html",)

def CajaView(request):
    movements=Movement.objects.filter(Q(type="VP") | Q(type="RD") | Q(type="rP")).order_by('-date')[:25]
    if "RetireProduct" in request.POST:
        retire_product=FormVender(request.POST)
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
    products = Product.objects.filter(removed=False).order_by('name')
    registe_cash=RegisteCash.objects.all().first()
    return render(request,"Almacen.html",{'products':products})

def ProductosView(request):
    products = Product.objects.filter(removed=False).order_by('name')   
    if request.method == "POST":
        if "CrearProducto" in request.POST:
            crear_form=FormEditar(request.POST,request.FILES)
            if crear_form.is_valid():
                name=crear_form.cleaned_data.get("name").__str__().capitalize()
                price=crear_form.cleaned_data.get("precio") 
                image=crear_form.cleaned_data.get("imagen")
                description=crear_form.cleaned_data.get("descripcion")
                try:
                    if Movement.Create(name,price,description,image):
                        crear_form=FormEditar()
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
        movements=Movement.objects.filter(product_id=product.id).order_by('-date')[:20]
        if request.method == "POST":
            #Form Editar
            if "EditProduct" in request.POST:
                edit_product=FormEditar(request.POST, request.FILES)
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
                sell_product=FormVender(request.POST)
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
                add_product=FormVender(request.POST)
                if add_product.is_valid():
                    lot_add=add_product.cleaned_data.get("cantidad")
                    if lot_add>= 0:
                        if Movement.Add(product,lot=lot_add):
                            messages.success(request,"Se han agregado {} {} correctamente".format(lot_add,product.name))
                            return render(request,"Producto.html",{'product':product, "movements":movements})
                messages.error(request,"No se han podido insertar {} {}".format(lot_add,product.name))
                return render(request,"Producto.html",{'product':product ,"movements":movements})
            elif "SubProduct" in request.POST:
                sub_product=FormVender(request.POST)
                if sub_product.is_valid():
                    lot_sub=sub_product.cleaned_data.get("cantidad")
                    if lot_sub >= 0:
                        if Movement.Sub(product,lot=lot_sub):
                            messages.success(request,"Se han quitado {} {} correctamente".format(lot_sub,product.name))
                            return render(request,"Producto.html",{'product':product, "movements":movements})
                messages.error(request,"No se han podido quitar {} {}".format(lot_sub,product.name))
                return render(request,"Producto.html",{'product':product ,"movements":movements})
            elif "RefundProduct" in request.POST: 
                refund_product=FormVender(request.POST)
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

def VentasView(request):
    t_Movement=Movement.objects.all()
    return render(request,"Ventas.html",{"t_Movement":t_Movement})

