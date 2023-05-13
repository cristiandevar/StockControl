from django.urls import path
from compra import views


urlpatterns = [
    path('proveedor/all', views.proveedores_view, name="proveedores"),
    path('producto/all', views.productos_view, name="productos"),
    path('productos-proveedor/<int:proveedor_id>', views.productos_proveedor, name="productos-proveedor"),
    path('proveedor/create', views.proveedor_create, name="proveedor-create"),
    path('proveedor/update/<int:proveedor_id>', views.proveedor_update, name="proveedor-update"),
    path('proveedor/delete/<int:proveedor_id>', views.proveedor_delete, name="proveedor-delete"),
    path('producto/create', views.producto_create, name="producto-create"),
    path('producto/update/<int:producto_id>', views.producto_update, name="producto-update"),
    path('producto/delete/<int:producto_id>', views.producto_delete, name="producto-delete"),
    path('proveedor/<int:proveedor_id>/producto/<int:producto_id>/delete', views.producto_proveedor_delete, name="producto-proveedor-delete"),
    path('', views.index, name="index"),

]