from django.shortcuts import render,redirect
from .models import Productos,Caja,Movimientos
from .forms import FormEditar,FormVender
from datetime import datetime 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
# Create your views here.

def RedirectHomeView(request):
    return redirect("home")

def HomeView(request):
    print("cc")
    if request.method == "POST":
        print("dd")
        if "Iniicar_Sesion" in request.POST:
            formlogin=AuthenticationForm(request,data=request.POST)
            print("AA")
            if formlogin.is_valid():
                print("bb")
                nombre=formlogin.cleaned_data.get("username")
                contra=formlogin.cleaned_data.get("password")
                usuario=authenticate(username=nombre,password=contra)
                if usuario is not None:
                    print("ee")
                    login(request,usuario)
                    return redirect("home")
    auth_form=AuthenticationForm()
    return render(request,"Home.html",{"auth_form":auth_form})

def AlmacenView(request):
    t_productos = Productos.objects.all()
    t_caja=Caja.objects.all().first()
    if request.method == "POST":    
        if "ReiniciarCajaDinero" in request.POST:
           t_caja.dinero=0
           t_caja.save()
    return render(request,"Almacen.html",{'t_productos':t_productos,'t_caja':t_caja})

def ProductosView(request):
    productos = Productos.objects.all()
    if request.method == "POST":
        crear_form=FormEditar(request.POST,request.FILES)
        if crear_form.is_valid():
            producto=Productos(
                name=crear_form.cleaned_data.get("name"),
                precio=crear_form.cleaned_data.get("precio"),
                descripcion=crear_form.cleaned_data.get("descripcion"))  
            pos_img=crear_form.cleaned_data.get("imagen")
            if pos_img:
                producto.imagen=pos_img
            producto.save()
            crear_form=FormEditar()
            return render(request,"Productos.html",{'productos':productos,"crear_form":crear_form,"producto_creado":True})
    crear_form=FormEditar()
    return render(request,"Productos.html",{'productos':productos,"crear_form":crear_form})

def ProductoView(request,productoID):
    producto=Productos.objects.get(id=productoID)
    #Renderizado Habitual de la pagina
    editar_form=FormEditar(data={'name': producto.name, 'precio': producto.precio, 'descripcion': producto.descripcion, 'imagen': producto.imagen},auto_id=False)
    t_movimientos=Movimientos.objects.filter(producto_id=producto.id)

    if request.method == "POST":
        #Form Editar
        if "EditarForm" in request.POST:
            editar_form=FormEditar(request.POST, request.FILES)
            if  editar_form.is_valid():
                producto.name=editar_form.cleaned_data.get("name")
                producto.precio=editar_form.cleaned_data.get("precio")
                producto.descripcion=editar_form.cleaned_data.get("descripcion")
                pos_img=editar_form.cleaned_data.get("imagen")
                if pos_img:
                    producto.imagen=pos_img
                producto.save()
                return render(request,"Producto.html",{'producto':producto,"editar_form":editar_form,"t_movimientos":t_movimientos, "producto_editado":True})
         #Form Vender
        elif "VenderForm" in request.POST:
            vender_form=FormVender(request.POST)
            if  vender_form.is_valid():
                    venta=Movimientos.crear_venta(producto,vender_form.cleaned_data.get("cantidad"))
                    if venta:
                        return render(request,"Producto.html",{'producto':producto,"editar_form":editar_form,"t_movimientos":t_movimientos, "producto_vendido":True})
                    return render(request,"Producto.html",{'producto':producto, "editar_form":editar_form,"t_movimientos":t_movimientos,"producto_vendido":False})
        elif "EliminarForm" in request.POST:
            producto.name+="_"+ datetime.now().__str__()
            producto.eliminado=True
            producto.save()
            return redirect("productos")
        elif "AgregarForm" in request.POST:
            agregar_form=FormVender(request.POST)
            if agregar_form.is_valid():
                agregar=Movimientos.crear_agregar(producto,agregar_form.cleaned_data.get("cantidad"))
                if agregar:
                    return render(request,"Producto.html",{'producto':producto, "editar_form":editar_form,"t_movimientos":t_movimientos,"producto_agregado":True})
 
    return render(request,"Producto.html",{'producto':producto ,"editar_form":editar_form,"t_movimientos":t_movimientos})
    

def VentasView(request):
    t_movimientos=Movimientos.objects.all()
    return render(request,"Ventas.html",{"t_movimientos":t_movimientos})

