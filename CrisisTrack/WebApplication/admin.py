from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from .models import User, Incident, IncidentCategory
from django.core.mail import send_mail
from django.urls import path, reverse
from django.shortcuts import render, redirect

# Register your models here.
# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'organization')}),
    )
    list_display = ('username', 'email', 'role', 'organization', 'is_staff')
    list_filter = ('role', 'organization', 'is_staff')

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'reported_by', 'reported_at', 'organization')
    list_filter = ('status', 'category', 'reported_at', 'organization')
    search_fields = ('title', 'description', 'reported_by__username')
    
    actions = ['review_incident', 'request_further_information', 'cancel_request', 'review_request']

    def request_further_information(self, request, queryset):
        for incident in queryset:
            if incident.reported_by.email:
                send_mail(
                    subject=f"Request for Further Information: {incident.title}",
                    message=f"Dear {incident.reported_by.username},\n\nWe require further information regarding your incident titled '{incident.title}'. Please provide additional details.",
                    from_email='admin@example.com',  
                    recipient_list=[incident.reported_by.email],
                )
            else:
                self.message_user(request, f"Incident '{incident.title}' does not have a valid email.")

        self.message_user(request, f"Requests for further information have been sent to {queryset.count()} reporters.")
    request_further_information.short_description = 'Request further information from the reporter'

    def cancel_request(self, request, queryset):
        for incident in queryset:
            if incident.reported_by.email:
                send_mail(
                    subject=f"Incident Cancelled: {incident.title}",
                    message=f"Dear {incident.reported_by.username},\n\nYour incident titled '{incident.title}' has been cancelled. Please reach out if you have any questions.",
                    from_email='admin@example.com',  
                    recipient_list=[incident.reported_by.email],
                )
            else:
                self.message_user(request, f"Incident '{incident.title}' does not have a valid email.")
            incident.delete()

        self.message_user(request, f"Cancel requests have been sent to {queryset.count()} reporters.")
    cancel_request.short_description = 'Cancel selected incident request'

    def review_request(self, request, queryset):
        # Get the first selected incident (assuming only one is selected)
        if queryset.count() == 1:
            incident = queryset.first()
            # Redirect to the custom review page with the incident ID
            return HttpResponseRedirect(f'/review_incident/{incident.id}/')
        
        self.message_user(request, "Please select exactly one incident to review.")
        return HttpResponseRedirect(request.get_full_path())  # Stay on the current page

    review_request.short_description = 'Review selected incident request'


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentCategory)