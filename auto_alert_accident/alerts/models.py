from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)




class AccidentReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def map_link(self):
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

    def __str__(self):
        return f"{self.latitude}, {self.longitude} - {self.timestamp}"
