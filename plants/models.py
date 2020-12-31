from django.db import models
from accounts.models import (User, Nursery)


class Plant(models.Model):
    nursery = models.ForeignKey(
        Nursery, related_name='Plants', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plants/')
    name = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Order')
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name='Order')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.name} ordered {self.quantity} of {self.plant.name}"
