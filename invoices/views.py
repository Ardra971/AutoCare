from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Invoice


@login_required
def my_invoices(request):

    invoices = (
        Invoice.objects
        .filter(
            booking__customer=request.user
        )
        .select_related(
            "booking",
            "booking__vehicle"
        )
        .prefetch_related(
            "booking__booking_services__service"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "invoices/my_invoices.html",
        {
            "invoices": invoices
        }
    )


@login_required
def invoice_detail(request, invoice_id):

    invoice = get_object_or_404(
        Invoice.objects
        .select_related(
            "booking",
            "booking__customer",
            "booking__vehicle"
        )
        .prefetch_related(
            "booking__booking_services__service"
        ),
        id=invoice_id,
        booking__customer=request.user
    )

    return render(
        request,
        "invoices/invoice_detail.html",
        {
            "invoice": invoice
        }
    )