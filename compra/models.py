from django.db import models

# Create your models here.


class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo()

    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'


class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()

    def __str__(self):
        return f'{self.nombre}'
