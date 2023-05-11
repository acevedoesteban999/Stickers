from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RedirectHomeView),
    path('Home/', views.HomeView,name='home'),
    path('Tienda/', views.TiendaView,name='tienda'),
    path('Administracion/', views.AdminView,name='administracion'),
    path('Producto/<int:productoID>/', views.ProductoView,name='producto'),
    path('Administracion/Categoria/<int:categoryID>/', views.CategoriaView,name='categoria'),
    path('Administracion/Categoria/<int:categoryID>/SubCategoria/<int:subcategoryID>', views.SubCategoriaView,name='subcategoria'),
    path('Operaciones/', views.OperacionesView,name='operaciones'),
    path('Caja/', views.CajaView,name='caja'),
    path('Usuario/<int:usuarioID>', views.UserView,name='usuario'),
    path('Usuarios/', views.UsersView,name='usuarios'),
    path('BasePost',views.BasePost,name='base_post'),
    path('Resumen/',views.ResumeView,name='resumen'), 
    path('QR/',views.QR,name='qr'), 
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
