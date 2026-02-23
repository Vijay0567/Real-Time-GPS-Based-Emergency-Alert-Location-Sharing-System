from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, EmergencyContact, AccidentReport


class AccidentReportAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'timestamp', 'status', 'view_map')

    def view_map(self, obj):
        return format_html(
            '<a href="https://www.google.com/maps?q={},{}" target="_blank">View Map</a>',
            obj.latitude,
            obj.longitude
        )

    view_map.short_description = "Location"

admin.site.register(Profile)
admin.site.register(EmergencyContact)
admin.site.register(AccidentReport, AccidentReportAdmin)
