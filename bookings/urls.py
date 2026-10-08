from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/",
        views.create_booking,
        name="create_booking",
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings",
    ),

]