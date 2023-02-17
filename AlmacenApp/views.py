from django.shortcuts import render,redirect
from .models import Product,RegisteCash,Movement
from .forms import FormEditar,FormVender
from datetime import datetime 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
  
# Create your views here.

def RedirectHomeView(request):
    return redirect("home")

def HomeView(request):
    if request.method == "POST":
        if "Iniicar_Sesion" in request.POST:
            formlogin=AuthenticationForm(request,data=request.POST)
            if formlogin.is_valid():
                nombre=formlogin.cleaned_data.get("username")
                contra=formlogin.cleaned_data.get("password")
                usuario=authenticate(username=nombre,password=contra)
                if usuario is not None:
                    login(request,usuario)
                    return render(request,"Home.html",{'log_in':True})
            return render(request,"Home.html",{'log_in':False})
        elif "CerrarSesion" in request.POST:
            logout(request)
            return render(request,"Home.html",{'log_out':True})
            
    return render(request,"Home.html",)

def AlmacenView(request):
    products = Product.objects.filter(removed=False).order_by('name')
    registe_cash=RegisteCash.objects.all().first()
    # if request.method == "POST":    
    #     if "ReiniciarRegisteCashDinero" in request.POST:
    #        t_RegisteCash.dinero=0
    #        t_RegisteCash.save()
    return render(request,"Almacen.html",{'products':products,'registe_cash':registe_cash})

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
                        return render(request,"Productos.html",{'products':products,"ProductName":name})
                except IntegrityError:
                    return render(request,"Productos.html",{'products':products,"Error":"IntegrityError","ErrorName":_name})
        return render(request,"Productos.html",{'products':products,"Error":True})
    return render(request,"Productos.html",{'products':products})

def ProductoView(request,productoID):
    product=Product.objects.get(id=productoID)
    if product:
        #editar_form=FormEditar(data={'name': product.name, 'precio': product.price, 'descripcion': product.description, 'imagen': product.image},auto_id=False)
        movements=Movement.objects.filter(product_id=product.id).order_by('-date')
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
                            return render(request,"Producto.html",{'product':product,"movements":movements, "lot_edit":True})
                    except IntegrityError:
                        product=Product.objects.get(id=productoID)
                        return render(request,"Producto.html",{'product':product,"movements":movements, "Error":"IntegrityError","ErrorName":name})
                        
                return render(request,"Producto.html",{'product':product,"movements":movements, "Error":True})
            #Form Vender
            elif "SellProduct" in request.POST:
                sell_product=FormVender(request.POST)
                if sell_product.is_valid():
                    lot_sell=sell_product.cleaned_data.get("cantidad")
                    if Movement.Sell(product,lot_sell):
                        return render(request,"Producto.html",{'product':product,"movements":movements, "lot_sell":lot_sell})
                return render(request,"Producto.html",{'product':product, "movements":movements,"Error":True})
            #Form Eliminar
            elif "RemoveProduct" in request.POST:
                if Movement.Remove(product):
                    return redirect('productos')
                return render(request,"Producto.html",{'product':product ,"movements":movements,"Error":True})
            #Form Agregar
            elif "AddProduct" in request.POST:
                add_product=FormVender(request.POST)
                if add_product.is_valid():
                    lot_add=add_product.cleaned_data.get("cantidad")
                    if lot_add>= 0:
                        if Movement.Add(product,lot=lot_add):
                            return render(request,"Producto.html",{'product':product, "movements":movements,"lot_add":lot_add})
                return render(request,"Producto.html",{'product':product ,"movements":movements,"Error":True})
        return render(request,"Producto.html",{'product':product ,"movements":movements})
    else:
        return redirect('productos')        
def VentasView(request):
    t_Movement=Movement.objects.all()
    return render(request,"Ventas.html",{"t_Movement":t_Movement})

