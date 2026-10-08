from django.contrib import admin

from .models import Service, ServicePricing


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "estimated_time",
        "created_at",
    )


@admin.register(ServicePricing)
class ServicePricingAdmin(admin.ModelAdmin):

    list_display = (
        "service",
        "vehicle_type",
        "problem_level",
        "price",
    )

    list_filter = (
        "service",
        "vehicle_type",
        "problem_level",
    )