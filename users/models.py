from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=50)
    victories = models.IntegerField(default=0)
    wines = models.ManyToManyField("wines.Wine", blank=True) # Relación muchos a muchos

    def __str__(self):
        return f"Profile of {self.user.username}"

    def add_coins(self, amount):
        self.coins += amount
        self.save()

    def subtract_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            self.save()

    def add_victory(self):
        self.victories += 1
        self.save()

    def add_points(self, amount):
        self.points += amount
        self.save()
