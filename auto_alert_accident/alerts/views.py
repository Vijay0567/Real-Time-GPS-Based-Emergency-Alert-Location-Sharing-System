from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import AccidentReport, EmergencyContact, Profile
import json


# -----------------------------
# USER REGISTRATION
# -----------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile

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
                return redirect("/user-dashboard/")

    return render(request,"login.html")
# -----------------------------
# USER LOGOUT
# -----------------------------
def user_logout(request):
    logout(request)
    return redirect('/login/')

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

        return JsonResponse({"status": "saved"})
    
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