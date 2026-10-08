from django.db import models


class Service(models.Model):

    name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estimated_time = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class ServicePricing(models.Model):

    VEHICLE_TYPES = [
        ("Car", "Car"),
        ("Bike", "Bike"),
        ("SUV", "SUV"),
        ("Van", "Van"),
        ("Truck", "Truck"),
    ]

    PROBLEM_LEVELS = [
        ("Minor", "Minor"),
        ("Moderate", "Moderate"),
        ("Major", "Major"),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="pricing"
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES
    )

    problem_level = models.CharField(
        max_length=20,
        choices=PROBLEM_LEVELS
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return (
            f"{self.service.name} - "
            f"{self.vehicle_type} - "
            f"{self.problem_level}"
        )
