from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Wine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="wines/", default="wines/img.jpg")
    body = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    aroma = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    taste = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    tannins = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    acidity = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    sweetness = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])
    aging = models.IntegerField(default=50, choices=[(i, i) for i in range(1, 101)])

    def __str__(self):
        return self.name

    def total_score(self):
        return round(
            (
                self.body
                + self.aroma
                + self.taste
                + self.tannins
                + self.acidity
                + self.sweetness
                + self.aging
            )
            / 7
        )
