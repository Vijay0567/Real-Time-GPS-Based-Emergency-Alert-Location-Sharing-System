from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from .models import AccidentReport, EmergencyContact


def emergency_page(request):
    return render(request, "emergency.html")


def map_dashboard(request):
    accidents = AccidentReport.objects.all()
    return render(request, "map_dashboard.html", {"accidents": accidents})


@csrf_exempt
def save_alert(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            lat = data.get("latitude")
            lon = data.get("longitude")

            
            AccidentReport.objects.create(
                latitude=lat,
                longitude=lon
            )

            
            contacts = EmergencyContact.objects.all()
            recipient_list = [contact.email for contact in contacts]

            map_link = f"https://www.google.com/maps?q={lat},{lon}"

            send_mail(
                subject="🚨 Emergency Accident Alert!",
                message=f"""
Accident Alert Triggered!

Location:
{map_link}

Immediate assistance required.
""",
                from_email="system@alert.com",
                recipient_list=recipient_list,
                fail_silently=False,
            )

            return JsonResponse({"status": "🚨 Alert Sent to Emergency Contacts & Redirecting!"})

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"status": "Server Error"})

    return JsonResponse({"status": "Invalid Request"})
