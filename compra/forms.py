from django import forms
from django.forms import ModelForm
from compra.models import Proveedor, Producto


class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'apellido', 'dni']
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'dni': 'DNI',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),

        }

    def clean(self):
        max_dni = 99999999
        min_dni = 1
        cleaned_data = super().clean()
        dni = cleaned_data.get('dni')
        if dni < min_dni or dni > max_dni:
            raise forms.ValidationError("DNI debe estar entre (1 : 99999999")


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['proveedor', 'nombre', 'precio', 'stock_actual']
        labels = {
            'proveedor': 'Proveedor',
            'nombre': 'Nombre',
            'precio': 'Precio',
            'stock_actual': 'Stock'
        }
        widgets = {
            'proveedor': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 50%;'
            }),

        }

    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get('precio')
        stock = cleaned_data.get('stock_actual')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser un numero positivo y menor a 1 millon")
        elif stock <= 0:
            raise forms.ValidationError("El stock debe ser un numero natural mayor a cero")

