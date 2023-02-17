from django.shortcuts import render,redirect
from .models import Product,RegisteCash,Movement
from .forms import FormEditar,FormVender
from datetime import datetime 
from django.contrib.auth.forms import AuthenticationForm
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
                    return redirect("home")
    auth_form=AuthenticationForm()
    return render(request,"Home.html",{"auth_form":auth_form})

def AlmacenView(request):
    t_Product = Product.objects.all().exclude(removed=True)
    t_RegisteCash=RegisteCash.objects.all().first()
    if request.method == "POST":    
        if "ReiniciarRegisteCashDinero" in request.POST:
           t_RegisteCash.dinero=0
           t_RegisteCash.save()
    return render(request,"Almacen.html",{'t_Product':t_Product,'t_RegisteCash':t_RegisteCash})

def ProductosView(request):
    products = Product.objects.filter(removed=False)
    if request.method == "POST":
        if "CrearProducto" in request.POST:
            crear_form=FormEditar(request.POST,request.FILES)
            if crear_form.is_valid():
                _price=crear_form.cleaned_data.get("precio")
                if _price > 0:
                    _name=crear_form.cleaned_data.get("name").__str__().capitalize() 
                    try:   
                        product=Product(name=_name,price=_price,description=crear_form.cleaned_data.get("descripcion"))  
                        pos_img=crear_form.cleaned_data.get("imagen")
                        if pos_img:
                            product.image=pos_img
                        product.save()
                        crear_form=FormEditar()
                        return render(request,"Productos.html",{'products':products,"ProductName":_name})
                    except IntegrityError:
                        return render(request,"Productos.html",{'products':products,"Error":"IntegrityError","ErrorName":_name})
        return render(request,"Productos.html",{'products':products,"Error":True})
    return render(request,"Productos.html",{'products':products})

def ProductoView(request,productoID):
    product=Product.objects.get(id=productoID)
    if product:
        #editar_form=FormEditar(data={'name': product.name, 'precio': product.price, 'descripcion': product.description, 'imagen': product.image},auto_id=False)
        movement=Movement.objects.filter(product_id=product.id)
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
                        edit=Movement.Edit(product,name,price,description,image)
                        if edit:
                            return render(request,"Producto.html",{'product':product,"movement":movement, "lot_edit":True})
                    except IntegrityError:
                        product=Product.objects.get(id=productoID)
                        return render(request,"Producto.html",{'product':product,"movement":movement, "Error":"IntegrityError","ErrorName":name})
                        
                return render(request,"Producto.html",{'product':product,"movement":movement, "Error":True})
            #Form Vender
            elif "SellProduct" in request.POST:
                sell_product=FormVender(request.POST)
                if sell_product.is_valid():
                    lot_sell=sell_product.cleaned_data.get("cantidad")
                    sell=Movement.Sell(product,lot_sell)
                    if sell:
                        return render(request,"Producto.html",{'product':product,"movement":movement, "lot_sell":lot_sell})
                return render(request,"Producto.html",{'product':product, "movement":movement,"Error":True})
            elif "RemoveProduct" in request.POST:
                rem=Movement.Remove(product)
                if rem:
                    return redirect('productos')
                return render(request,"Producto.html",{'product':product ,"movement":movement,"Error":True})
            elif "AddProduct" in request.POST:
                add_product=FormVender(request.POST)
                if add_product.is_valid():
                    lot_add=add_product.cleaned_data.get("cantidad")
                    if lot_add>= 0:
                        add=Movement.Add(product,lot=lot_add)
                        if add:
                            return render(request,"Producto.html",{'product':product, "movement":movement,"lot_add":lot_add})
                return render(request,"Producto.html",{'product':product ,"movement":movement,"Error":True})
        return render(request,"Producto.html",{'product':product ,"movement":movement})
    else:
        return redirect('productos')        
def VentasView(request):
    t_Movement=Movement.objects.all()
    return render(request,"Ventas.html",{"t_Movement":t_Movement})

