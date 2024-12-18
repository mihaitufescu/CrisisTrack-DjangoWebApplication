from django import forms
from django.contrib.auth import get_user_model
from .models import Incident, IncidentCategory

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'organization')
        labels = {
            'username': 'Nume utilizator',
            'email': 'Email',
            'first_name': 'Prenume',
            'last_name': 'Nume',
            'organization': 'Organizație',
        }
        help_texts = {
            'username': 'Obligatoriu. Maxim 150 de caractere. Doar litere, cifre și caracterele @/./+/-/_ sunt permise.',
            'password': "Minim 8 caractere. Include litere, cifre si caractere speciale obligatoriu"
        }
        error_messages = {
            'username': {
                'required': 'Numele utilizatorului este obligatoriu.',
                'max_length': 'Numele utilizatorului nu poate depăși 150 de caractere.',
                'unique': 'Acest nume de utilizator este deja luat.',
            },
            'email': {
                'required': 'Adresa de email este obligatorie.',
                'invalid': 'Introduceti o adresă de email validă.',
            },
            'password1': {
                'required': 'Parola este obligatorie.',
                'min_length': 'Parola trebuie să aibă cel puțin 8 caractere.',
            },
            'password2': {
                'required': 'Confirmarea parolei este obligatorie.',
                'not_match': 'Parolele nu se potrivesc.',
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Această adresă de email este deja folosită.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parolele nu se potrivesc.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        # Automatically set the user role to 'Reporter' here
        user.role = 'reporter'
        
        if commit:
            user.save()
        return user

class IncidentCreationForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'category', 'description', 'organization']
        labels = {
            'title': 'Titlu',
            'category': 'Categorie',
            'description': 'Descriere',
            'organization': 'Organizație',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detaliază incidentul...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.status = 'Nou'

class ReviewIncidentForm(forms.Form):
    custom_message = forms.CharField(widget=forms.Textarea, label="Mesaj", required=True)