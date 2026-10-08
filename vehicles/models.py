from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):

    VEHICLE_TYPES = [
        ("Car", "Car"),
        ("Bike", "Bike"),
        ("SUV", "SUV"),
        ("Van", "Van"),
        ("Truck", "Truck"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )

    brand = models.CharField(max_length=50)

    model = models.CharField(max_length=50)

    year = models.PositiveIntegerField()

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} - {self.brand} {self.model}"
