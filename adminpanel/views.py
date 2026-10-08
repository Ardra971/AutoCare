from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from services.models import Service
from bookings.models import Booking
from invoices.models import Invoice
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
@staff_member_required
def admin_dashboard(request):

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    total_vehicles = Vehicle.objects.count()

    total_services = Service.objects.count()

    total_bookings = Booking.objects.count()

    total_invoices = Invoice.objects.count()

    recent_bookings = (
        Booking.objects
        .select_related(
            "customer",
            "vehicle"
        )
        .prefetch_related(
            "booking_services__service"
        )
        .order_by("-created_at")[:8]
    )

    context = {
        "total_customers": total_customers,
        "total_vehicles": total_vehicles,
        "total_services": total_services,
        "total_bookings": total_bookings,
        "total_invoices": total_invoices,
        "recent_bookings": recent_bookings,
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context
    )

@staff_member_required
def customers_view(request):

    customers = User.objects.filter(
        is_staff=False
    ).order_by("-date_joined")

    return render(
        request,
        "adminpanel/customers.html",
        {
            "customers": customers
        }
    )

@staff_member_required
def vehicles_view(request):

    vehicles = Vehicle.objects.select_related(
        "owner"
    ).order_by("-created_at")

    return render(
        request,
        "adminpanel/vehicles.html",
        {
            "vehicles": vehicles
        }
    )

@staff_member_required
def services_view(request):

    services = Service.objects.all().order_by("name")

    return render(
        request,
        "adminpanel/services.html",
        {
            "services": services
        }
    )

@staff_member_required
def bookings_view(request):

    bookings = (
        Booking.objects
        .select_related(
            "customer",
            "vehicle",
            "invoice"
        )
        .prefetch_related(
            "booking_services__service"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "adminpanel/bookings.html",
        {
            "bookings": bookings
        }
    )


@staff_member_required
def invoices_view(request):

    invoices = (
        Invoice.objects
        .select_related(
            "booking",
            "booking__customer",
            "booking__vehicle"
        )
        .prefetch_related(
            "booking__booking_services__service"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "adminpanel/invoices.html",
        {
            "invoices": invoices
        }
    )

@staff_member_required
def add_service(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        description = request.POST.get(
            "description",
            ""
        ).strip()
        price = request.POST.get("price")
        estimated_time = request.POST.get(
            "estimated_time",
            ""
        ).strip()

        Service.objects.create(
            name=name,
            description=description,
            price=price,
            estimated_time=estimated_time
        )

        return redirect("admin_services")


    return render(
        request,
        "adminpanel/add_service.html"
    )

@staff_member_required
def update_invoice_payment(request, invoice_id):

    invoice = get_object_or_404(
        Invoice,
        id=invoice_id
    )

    if request.method == "POST":

        payment_status = request.POST.get(
            "payment_status"
        )

        if payment_status in ["Pending", "Paid"]:

            invoice.payment_status = payment_status
            invoice.save()

        return redirect("admin_invoices")

    return redirect("admin_invoices")

@staff_member_required
def bookings_view(request):

    bookings = (
        Booking.objects
        .select_related(
            "customer",
            "vehicle",
            "invoice"
        )
        .prefetch_related(
            "booking_services__service"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "adminpanel/bookings.html",
        {
            "bookings": bookings
        }
    )


@staff_member_required
def update_booking_status(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    if request.method == "POST":

        new_status = request.POST.get("status")

        valid_statuses = [
            "Pending",
            "Confirmed",
            "Vehicle Received",
            "Under Service",
            "Completed",
            "Cancelled",
        ]

        if new_status in valid_statuses:

            booking.status = new_status
            booking.save(update_fields=["status"])

            messages.success(
                request,
                f"Booking #{booking.id} status updated to {new_status}."
            )

    return redirect("admin_bookings")