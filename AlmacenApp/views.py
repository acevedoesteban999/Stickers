from django.shortcuts import render,redirect
from .models import Productos
# Create your views here.

def RedirectHomeView(request):
    return redirect("home")
def HomeView(request):
    return render(request,"Home.html")
def AlmacenView(request):
    TProductos = Productos.objects.all()
    return render(request,"Almacen.html",{'TProductos':TProductos})
def ProductosView(request):
    return render(request,"Productos.html")
def VentasView(request):
    return render(request,"Ventas.html")