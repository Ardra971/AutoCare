from django.urls import path
from . import views


urlpatterns = [

    path(
        "my-invoices/",
        views.my_invoices,
        name="my_invoices"
    ),

    path(
        "<int:invoice_id>/",
        views.invoice_detail,
        name="invoice_detail"
    ),

]