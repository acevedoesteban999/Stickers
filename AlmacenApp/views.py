from django.shortcuts import render,redirect
from .models import Productos,Caja
# Create your views here.

def RedirectHomeView(request):
    return redirect("home")

def HomeView(request):
    return render(request,"Home.html")

def AlmacenView(request):
    TProductos = Productos.objects.all()
    TCaja=Caja.objects.all().first()
    return render(request,"Almacen.html",{'TProductos':TProductos,'TCaja':TCaja})

def ProductosView(request):
    TProductos = Productos.objects.all()
    return render(request,"Productos.html",{'TProductos':TProductos})

def ProductoIdView(request,productID):
    Product=Productos.objects.get(id=productID)
    return render(request,"Productos.html",{'Product':Product})

def VentasView(request):
    return render(request,"Ventas.html")