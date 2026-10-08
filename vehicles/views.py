from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Vehicle


@login_required
def vehicle_list(request):

    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "vehicles/vehicle_list.html",
        {
            "vehicles": vehicles
        }
    )


@login_required
def add_vehicle(request):

    if request.method == "POST":

        registration_number = request.POST.get(
            "registration_number",
            ""
        ).strip().upper()

        brand = request.POST.get("brand", "").strip()
        model = request.POST.get("model", "").strip()
        year = request.POST.get("year")
        vehicle_type = request.POST.get("vehicle_type")

        # Check duplicate registration number
        if Vehicle.objects.filter(
            registration_number=registration_number
        ).exists():

            return render(
                request,
                "vehicles/add_vehicle.html",
                {
                    "error": (
                        "A vehicle with this registration "
                        "number already exists."
                    )
                }
            )

        # Create vehicle
        Vehicle.objects.create(
            owner=request.user,
            registration_number=registration_number,
            brand=brand,
            model=model,
            year=year,
            vehicle_type=vehicle_type
        )

        return redirect("vehicle_list")

    return render(
        request,
        "vehicles/add_vehicle.html"
    )


@login_required
def delete_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        owner=request.user
    )

    if request.method == "POST":
        vehicle.delete()

    return redirect("vehicle_list")