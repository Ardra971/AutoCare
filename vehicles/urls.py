from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.vehicle_list,
        name="vehicle_list"
    ),

    path(
        "add/",
        views.add_vehicle,
        name="add_vehicle"
    ),

    path(
        "delete/<int:vehicle_id>/",
        views.delete_vehicle,
        name="delete_vehicle"
    ),

]