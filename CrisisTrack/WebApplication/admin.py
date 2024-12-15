from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Incident

# Register your models here.
# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'organization')}),
    )
    list_display = ('username', 'email', 'role', 'organization', 'is_staff')
    list_filter = ('role', 'organization', 'is_staff')

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Incident)