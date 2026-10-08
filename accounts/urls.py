from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

    path("profile/", views.profile_view, name="profile"),
    path("invoices/", views.my_invoices, name="my_invoices"),
]