from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RedirectHomeView),
    path('Home/', views.HomeView,name='home'),
    path('Tienda/', views.TiendaView,name='tienda'),
    path('Productos/', views.ProductosView,name='productos'),
    path('Producto/<int:productoID>/', views.ProductoView,name='producto'),
    path('Operaciones/', views.OperacionesView,name='Operaciones'),
    path('Caja/', views.CajaView,name='caja'),
    path('BasePost',views.BasePost,name='base_post'),
    path('Resumen/',views.ResumeView,name='resumen'), 
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
