from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RedirectHomeView),
    path('Home/', views.HomeView,name='home'),
    path('Almacen/', views.AlmacenView,name='almacen'),
    path('Productos/', views.ProductosView,name='productos'),
    path('Producto/<int:productoID>/', views.ProductoView,name='producto'),
    path('Transacciones/', views.TransaccionesView,name='transacciones'),
    path('Caja/', views.CajaView,name='caja'),
    path('BasePost',views.BasePost,name='base_post'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)