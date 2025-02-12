from django.db import models


# Create your models here.
class Vino(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Variables de puntuación
    cuerpo = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    aroma = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    sabor = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    taninos = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    acidez = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    dulzura = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100
    envejecimiento = models.IntegerField(
        default=50, choices=[(i, i) for i in range(1, 101)]
    )  # De 1 a 100

    # Maridaje
    maridaje = models.TextField(default="Pasta, Quesos, Carnes Rojas")  # Ejemplo

    def __str__(self):
        return self.nombre

    def puntuacion_total(self):
        # Método para calcular la puntuación total del vino
        return (
            self.cuerpo
            + self.aroma
            + self.sabor
            + self.taninos
            + self.acidez
            + self.dulzura
            + self.envejecimiento
        ) / 7
