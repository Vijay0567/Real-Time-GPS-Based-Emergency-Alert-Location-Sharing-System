# -----------------------------
# CORE IMPORTS
# -----------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import AccidentReport, EmergencyContact, Profile
import json

# -----------------------------
# USER REGISTRATION
# -----------------------------

def register(request):

    # show form when page opens
    if request.method == "GET":
        return render(request, "register.html")

    # create account when form submitted
    if request.method == "POST":

        name = request.POST.get("name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        blood = request.POST.get("blood")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            name=name,
            age=age,
            sex=sex,
            phone_number=phone,
            email=email,
            blood_group=blood
        )
        return render(request, "register_success.html")
    return render(request,"register.html")
# -----------------------------
# USER LOGIN
# -----------------------------
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
import logging
import os

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            # ADMIN LOGIN
            if user.is_superuser:
                return redirect("/admin-dashboard/")

            # USER LOGIN
            else:
                # If user has no emergency contact, prompt to add one before dashboard
                has_contact = EmergencyContact.objects.filter(user=user).exists()
                if not has_contact:
                    return redirect('add_emergency_contact')
                return redirect("/user-dashboard/")

    return render(request,"login.html")
# -----------------------------
# USER LOGOUT
# -----------------------------
def user_logout(request):
    logout(request)
    return redirect('/login/')


@login_required
def add_emergency_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        EmergencyContact.objects.create(user=request.user, name=name, phone_number=phone, email=email)
        messages.success(request, 'Emergency contact saved — you are now protected.')
        return redirect('/user-dashboard/')

    return render(request, 'add_emergency_contact.html')

# -----------------------------
# DASHBOARD
# -----------------------------
@login_required
def dashboard(request):

    alerts = AccidentReport.objects.count()
    contacts = EmergencyContact.objects.count()

    return render(request, "dashboard.html", {
        "alerts": alerts,
        "contacts": contacts
    })


# -----------------------------
# EMERGENCY ALERT PAGE
# -----------------------------
@login_required
def emergency_page(request):

    return render(request, "emergency.html")


# -----------------------------
# CONTACTS PAGE
# -----------------------------
@login_required
def contacts_page(request):

    contacts = EmergencyContact.objects.all()

    return render(request, "contacts.html", {
        "contacts": contacts
    })


# -----------------------------
# ALERT HISTORY
# -----------------------------
@login_required
def history_page(request):

    alerts = AccidentReport.objects.all()

    return render(request, "history.html", {
        "alerts": alerts
    })


# -----------------------------
# MAP DASHBOARD
# -----------------------------
@login_required
def map_dashboard(request):

    alerts = AccidentReport.objects.all()

    return render(request, "map_dashboard.html", {
        "alerts": alerts
    })


# -----------------------------
# SAVE ALERT (GPS)
# -----------------------------
@login_required
def save_alert(request):

    if request.method == "POST":

        data = json.loads(request.body)

        lat = data["latitude"]
        lon = data["longitude"]

        AccidentReport.objects.create(
            user=request.user,
            latitude=lat,
            longitude=lon
        )

        # Notify guardians (attempt SMS via Twilio if configured, otherwise email)
        notify_guardians(request.user, lat, lon)

        return JsonResponse({"status": "saved"})


def send_sms_via_twilio(to_number, message):
    try:
        from twilio.rest import Client
    except Exception:
        return False

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER')
    if not (account_sid and auth_token and from_number):
        return False

    try:
        client = Client(account_sid, auth_token)
        client.messages.create(body=message, from_=from_number, to=to_number)
        return True
    except Exception as e:
        logging.exception('Twilio send failed')
        return False


def notify_guardians(user, lat, lon):
    contacts = EmergencyContact.objects.filter(user=user)
    map_link = f"https://www.google.com/maps?q={lat},{lon}"
    message = f"Emergency alert from {user.username}. Location: {map_link}"

    for c in contacts:
        sent = False
        # try SMS (phone number must be in international format)
        if c.phone_number:
            sent = send_sms_via_twilio(c.phone_number, message)
        # fallback to email (console backend will print)
        if not sent and c.email:
            try:
                send_mail(
                    subject='Guardian Alert: emergency from your contact',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
                    recipient_list=[c.email]
                )
                sent = True
            except Exception:
                logging.exception('Failed to send guardian email')

    # Always also notify admin via console email for record (admins can monitor)
    try:
        admin_msg = f"User {user.username} triggered an emergency at {map_link}"
        send_mail('Admin Alert: Emergency', admin_msg, settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com', [a[1] for a in settings.ADMINS] if hasattr(settings, 'ADMINS') else [])
    except Exception:
        # ADMINS may be empty; ignore
        pass
    
from .models import AccidentReport, Profile

def admin_dashboard(request):

    alerts = AccidentReport.objects.select_related("user").all()

    return render(request,"admin_dashboard.html",{"alerts":alerts})

from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    return render(request,"user_dashboard.html",{"profile":profile})


from django.http import JsonResponse
from .models import AccidentReport

def get_alerts(request):

    alerts = AccidentReport.objects.select_related("user").all()

    data = []

    for alert in alerts:
        data.append({
            "name": alert.user.profile.name,
            "phone": alert.user.profile.phone_number,
            "lat": alert.latitude,
            "lng": alert.longitude,
        })

    return JsonResponse(data, safe=False)