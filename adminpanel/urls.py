from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "customers/",
        views.customers_view,
        name="admin_customers"
    ),

    path(
        "vehicles/",
        views.vehicles_view,
        name="admin_vehicles"
    ),

    path(
        "services/",
        views.services_view,
        name="admin_services"
    ),

    path(
        "services/add/",
        views.add_service,
        name="admin_service_add"
    ),

    path(
        "bookings/",
        views.bookings_view,
        name="admin_bookings"
    ),

    path(
        "invoices/",
        views.invoices_view,
        name="admin_invoices"
    ),

    path(
    "invoices/<int:invoice_id>/update-payment/",
    views.update_invoice_payment,
    name="update_invoice_payment"
),


path(
    "bookings/<int:booking_id>/status/",
    views.update_booking_status,
    name="update_booking_status"
),
]