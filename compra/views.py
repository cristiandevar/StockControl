from django import forms
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from compra.models import Proveedor, Producto
from compra.forms import ProveedorForm, ProductoForm


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')


def proveedores_view(request):
    try:
        proveedores = Proveedor.objects.all()
        for p in proveedores:
            p.cant_p = Producto.objects.filter(proveedor=p).count()
    except Exception:
        proveedores = None
    return render(request, 'proveedores.html', {
        'proveedores': proveedores
    })


def productos_view(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {
        'productos': productos
    })


def proveedor_create(request):
    form = ProveedorForm()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedores')

    return render(request, 'proveedor_create.html', {
        'form': form,
        'submit': 'Crear Proveedor',
        'direccion': 'proveedores'
    })


def producto_create(request):
    if Proveedor.objects.all().count() > 0:
        form = ProductoForm()
        if request.method == 'POST':
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('productos')
        return render(request, 'producto_create.html', {
                'form': form,
                'submit': 'Crear Producto',
                'direccion': 'productos'
            })
    else:
        return render(request, 'error_opcion_producto.html', {
            'mensaje': 'Error al Agregar: No existen proveedores registrados.',
            'direccion': 'inicio',
            'value_volver': 'Inicio',
            'value': 'Agregar Proveedor'
        })


def proveedor_update(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor_update.html', {
        'form': form,
        'submit': 'Modificar Proveedor',
        'direccion': 'proveedores'
    })


def producto_update(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_update.html', {
        'form': form,
        'submit': 'Modificar Producto',
        'direccion': 'productos'
    })


def proveedor_delete(request, proveedor_id):
    try:
        proveedor = Proveedor.objects.get(id=proveedor_id)
        proveedor.delete()
        return redirect('proveedores')
    except ProtectedError:
        proveedor = Proveedor.objects.get(id=proveedor_id)
        productos = Producto.objects.filter(proveedor=proveedor)
        return render(request, 'error_opcion_proveedor.html', {
            'mensaje': 'Error al borrar: Existen Productos relacionados.',
            'direccion': 'proveedores',
            'productos': productos,
            'proveedor': proveedor,
            'value': 'Ver Productos',
            'value_volver': 'Atras'
        })
    except Exception:
        return render(request, 'error.html', {
            'mensaje': 'Error al borrar: Proveedor no encontrado.',
            'direccion': 'productos-proveedor',
            'value_volver': 'Atras'
        })


def producto_delete(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('productos')


def productos_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.get(id=proveedor_id)
    productos = Producto.objects.filter(proveedor=proveedor)
    return render(request, 'productos_proveedor.html', {
        'productos': productos,
        'proveedor': proveedor,
    })


def producto_proveedor_delete(request, proveedor_id, producto_id):
    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    return redirect('productos-proveedor', proveedor_id=proveedor_id)


def producto_proveedor_create(request, proveedor_id):
    form = ProductoForm(initial={
        'proveedor': Proveedor.objects.get(id=proveedor_id)
    })
    form.fields['proveedor'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        form.fields['proveedor'].widget = forms.HiddenInput()
        if form.is_valid():
            producto = form.save(commit=False)
            proveedor = Proveedor.objects.get(id=proveedor_id)
            producto.proveedor = proveedor
            producto.save()
            return redirect('productos-proveedor', proveedor_id=proveedor_id)

    return render(request, 'producto_proveedor_create.html', {
        'form': form,
        'submit': 'Crear Producto',
        'direccion': 'productos-proveedor',
        'parametro': proveedor_id

    })
