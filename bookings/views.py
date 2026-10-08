from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from invoices.models import Invoice
from services.models import Service
from vehicles.models import Vehicle

from .models import Booking, BookingService


# ============================================================
# CREATE BOOKING
# ============================================================

@login_required
def create_booking(request):

    # Get customer's vehicles
    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    # Get all available services
    services = Service.objects.all().order_by("name")

    # ========================================================
    # GET REQUEST
    # ========================================================

    if request.method == "GET":

        return render(
            request,
            "bookings/create_booking.html",
            {
                "vehicles": vehicles,
                "services": services,
            }
        )

    # ========================================================
    # POST REQUEST
    # ========================================================

    if request.method == "POST":

        # ----------------------------------------------------
        # Get form data
        # ----------------------------------------------------

        vehicle_id = request.POST.get(
            "vehicle",
            ""
        ).strip()

        service_ids = request.POST.getlist(
            "services"
        )

        booking_date = request.POST.get(
            "booking_date",
            ""
        ).strip()

        booking_time = request.POST.get(
            "booking_time",
            ""
        ).strip()

        problem_description = request.POST.get(
            "problem_description",
            ""
        ).strip()

        # ----------------------------------------------------
        # Debug information
        # ----------------------------------------------------

        print("========== BOOKING POST ==========")
        print("Vehicle:", vehicle_id)
        print("Services:", service_ids)
        print("Date:", booking_date)
        print("Time:", booking_time)
        print("Problem:", problem_description)
        print("===================================")

        # ====================================================
        # VEHICLE VALIDATION
        # ====================================================

        if not vehicle_id:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Please select a vehicle.",
                }
            )

        vehicle = get_object_or_404(
            Vehicle,
            id=vehicle_id,
            owner=request.user
        )

        # ====================================================
        # SERVICE VALIDATION
        # ====================================================

        if not service_ids:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Please select at least one service.",
                }
            )

        selected_services = Service.objects.filter(
            id__in=service_ids
        )

        if not selected_services.exists():

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Selected service is not available.",
                }
            )

        # ====================================================
        # DATE VALIDATION
        # ====================================================

        if not booking_date:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Please select a service date.",
                }
            )

        # ====================================================
        # TIME VALIDATION
        # ====================================================

        if not booking_time:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Please select a service time.",
                }
            )

        # ====================================================
        # PROBLEM DESCRIPTION VALIDATION
        # ====================================================

        if not problem_description:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": "Please describe the vehicle problem.",
                }
            )

        # ====================================================
        # DUPLICATE BOOKING CHECK
        # ====================================================

        duplicate_booking = Booking.objects.filter(
            vehicle=vehicle,
            booking_date=booking_date,
            booking_time=booking_time
        ).exclude(
            status="Cancelled"
        ).exists()

        if duplicate_booking:

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": (
                        "This vehicle already has a booking "
                        "at this date and time."
                    ),
                }
            )

        # ====================================================
        # CREATE BOOKING
        # ====================================================

        try:

            with transaction.atomic():

                # ------------------------------------------------
                # Calculate total service cost
                # ------------------------------------------------

                total_cost = sum(
                    (
                        service.price
                        for service in selected_services
                    ),
                    Decimal("0.00")
                )

                # ------------------------------------------------
                # Create Booking
                # ------------------------------------------------

                booking = Booking.objects.create(
                    customer=request.user,
                    vehicle=vehicle,
                    booking_date=booking_date,
                    booking_time=booking_time,
                    problem_description=problem_description,
                    estimated_cost=total_cost,
                    status="Pending"
                )

                # ------------------------------------------------
                # Create BookingService records
                # ------------------------------------------------

                for service in selected_services:

                    BookingService.objects.create(
                        booking=booking,
                        service=service,
                        price=service.price
                    )

                # ------------------------------------------------
                # Create Invoice
                # ------------------------------------------------

                Invoice.objects.create(
                    booking=booking,
                    service_charge=total_cost,
                    parts_charge=Decimal("0.00"),
                    tax=Decimal("0.00"),
                    total_amount=total_cost,
                    payment_status="Pending"
                )

            # ----------------------------------------------------
            # Success message
            # ----------------------------------------------------

            messages.success(
                request,
                f"Booking #{booking.id} created successfully."
            )

            return redirect("my_bookings")

        # ========================================================
        # ERROR WHILE CREATING BOOKING
        # ========================================================

        except Exception as e:

            print("===================================")
            print("BOOKING ERROR:", e)
            print("===================================")

            return render(
                request,
                "bookings/create_booking.html",
                {
                    "vehicles": vehicles,
                    "services": services,
                    "error": (
                        "Unable to create the booking. "
                        "Please try again."
                    ),
                }
            )

    # ========================================================
    # SAFETY FALLBACK
    # ========================================================

    return render(
        request,
        "bookings/create_booking.html",
        {
            "vehicles": vehicles,
            "services": services,
        }
    )


# ============================================================
# MY BOOKINGS
# ============================================================

@login_required
def my_bookings(request):

    bookings = (
        Booking.objects
        .filter(
            customer=request.user
        )
        .select_related(
            "vehicle",
            "invoice"
        )
        .prefetch_related(
            "booking_services__service"
        )
        .order_by(
            "-created_at"
        )
    )

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings
        }
    )