from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
import requests
from invoices.models import Invoice
from .models import EmailOTP


def send_otp_email(email, username, otp):
    """
    Send OTP using Brevo API.
    """

    api_key = settings.BREVO_API_KEY

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    data = {
        "sender": {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        },


        "to": [
            {
                "email": email,
                "name": username
            }
        ],
        "subject": "AutoCare Email Verification OTP",
        "htmlContent": f"""
        <html>
            <body>
                <h2>Welcome to AutoCare</h2>

                <p>Hello {username},</p>

                <p>Your email verification OTP is:</p>

                <h1>{otp}</h1>

                <p>This OTP is valid for 5 minutes.</p>

                <p>Please do not share this OTP with anyone.</p>

                <p>Regards,<br>
                AutoCare Team</p>
            </body>
        </html>
        """
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    return response.status_code in [200, 201]


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check passwords
        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email already exists."
            )
            return redirect("register")

        # Create inactive user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP
        EmailOTP.objects.create(
            user=user,
            otp=otp
        )

        # Send OTP
        email_sent = send_otp_email(
            email,
            username,
            otp
        )

        if email_sent:

            request.session["otp_user_id"] = user.id

            messages.success(
                request,
                "Registration successful! OTP has been sent to your email."
            )

            return redirect("verify_otp")

        else:

            user.delete()

            messages.error(
                request,
                "Unable to send OTP. Please try again."
            )

            return redirect("register")

    return render(
        request,
        "accounts/register.html"
    )


def verify_otp(request):

    user_id = request.session.get("otp_user_id")

    if not user_id:
        messages.error(
            request,
            "OTP session expired. Please register again."
        )
        return redirect("register")

    try:
        user = User.objects.get(id=user_id)
        otp_record = EmailOTP.objects.get(user=user)

    except (
        User.DoesNotExist,
        EmailOTP.DoesNotExist
    ):
        messages.error(
            request,
            "Invalid OTP session."
        )
        return redirect("register")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        if entered_otp == otp_record.otp:

            user.is_active = True
            user.save()

            otp_record.delete()

            request.session.pop("otp_user_id", None)

            messages.success(
                request,
                "Email verified successfully. You can now login."
            )

            return redirect("login")

        else:

            messages.error(
                request,
                "Invalid OTP. Please try again."
            )

    return render(
        request,
        "accounts/verify_otp.html",
        {
            "email": user.email
        }
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Admin / Staff user
            if user.is_staff:
                return redirect("admin_dashboard")

            # Normal customer
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username, password, or email not verified."
        )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")

@login_required
def dashboard_view(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    from services.models import Service

    total_vehicles = request.user.vehicles.count()

    services = Service.objects.all().order_by("name")

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_vehicles": total_vehicles,
            "services": services,
        }
    )


@login_required
def profile_view(request):

    return render(
        request,
        "accounts/profile.html"
    )

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