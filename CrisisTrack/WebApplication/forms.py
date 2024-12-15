from django import forms
from django.contrib.auth import get_user_model
from .models import Incident, IncidentCategory

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    # Adding extra fields for your custom user model
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'organization')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set the password
        if commit:
            user.save()
        return user

class IncidentCreationForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['category', 'description', 'organization']  # Exclude status from form fields

    # Status choices (you can keep this, though it's no longer needed in the form)
    status_choices = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default value of status to 'New', but keep it hidden from the form
        self.instance.status = 'New'
