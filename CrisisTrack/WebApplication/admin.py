from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Incident, IncidentCategory
from django.core.mail import send_mail

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

    actions = ['resolve_incidents']

    def resolve_incidents(self, request, queryset):
        # Send email to corresponding address when resolved
        for incident in queryset:
            # Send an email to the reported_by user's email
            send_mail(
                subject=f"Incident Resolved: {incident.title}",
                message=f"The incident '{incident.title}' has been resolved.",
                from_email='your_admin_email@example.com',
                recipient_list=[incident.reported_by.email],
            )
            # Update the status to 'resolved'
            incident.status = 'resolved'
            incident.save()

        self.message_user(request, f"{queryset.count()} incidents have been resolved and emails sent.")
    
    resolve_incidents.short_description = 'Mark selected incidents as resolved and notify by email'

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentCategory)