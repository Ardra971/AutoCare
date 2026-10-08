from django.db import models
from django.contrib.auth.models import User

from vehicles.models import Vehicle
from services.models import Service


class Booking(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Vehicle Received", "Vehicle Received"),
        ("Under Service", "Under Service"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    problem_description = models.TextField()

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.vehicle.registration_number} - Booking #{self.id}"


class BookingService(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booking_services"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="booking_services"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.booking} - {self.service.name}"