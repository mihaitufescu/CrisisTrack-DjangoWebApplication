from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, IncidentCreationForm, ReviewIncidentForm
from django.contrib.auth.decorators import login_required
from .models import Incident, IncidentGuideline, IncidentCategory, Recommendation
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.db.models import Count
import io
import urllib, base64
from django.contrib import messages
import dotenv
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(BASE_DIR, '.env')
dotenv_file = dotenv.find_dotenv(dotenv_path)
load_dotenv(dotenv_file)


# Home View
def index(request):
    return render(request, 'index.html', {
        'app_name': 'CrisisTrack',
        'app_description': 'O platforma de educare si raportare a incidentelor cibernetice.'
    })

# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentification/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'authentification/login.html', {'error': 'Invalid username or password'})
    return render(request, 'authentification/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def create_incident(request):
    if request.method == 'POST':
        form = IncidentCreationForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()


            messages.success(request, "Incidentul a fost creat cu succes!")


            return HttpResponseRedirect(request.path)  

    else:
        form = IncidentCreationForm()

    return render(request, 'create_incident.html', {'form': form})

@login_required
def incident_list(request):
    if not request.user.is_superuser:

        messages.error(request, "Accesul este restricționat. Doar administratorii pot vizualiza această pagină.")

        return redirect('index')
    incidents = Incident.objects.all()
    categories = IncidentCategory.objects.all()
    print(f"Number of incidents: {incidents.count()}")
    return render(request, 'incidents_list.html', {
        'incidents': incidents,
        'categories': categories,
    })

def guidelines(request):
    return render(request, 'guidelines.html')

def guideline_detail(request, incident_type):
    guideline = get_object_or_404(IncidentGuideline, incident_type=incident_type)
    steps = guideline.steps.split("\\n") 
    print(steps)
    return render(request, 'guideline_detail.html', {
        'incident_type': guideline.incident_type,
        'description': guideline.description,
        'steps': steps,
        'video_url': guideline.video_url,
        'research_papers': guideline.get_research_papers(),
    })

def review_incident(request, incident_id):

    incident = get_object_or_404(Incident, id=incident_id)
    

    if request.method == 'GET':
        form = ReviewIncidentForm()
        return render(request, 'review_incident.html', {'incident': incident, 'form': form})
    

    elif request.method == 'POST':
        form = ReviewIncidentForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data['custom_message']
            
 
            if incident.reported_by.email:
                from_email = os.getenv('SMTP_HOST')  
                
                try:
                    send_mail(
                        subject=f"Incident Update: {incident.title}",
                        message=f"Dear {incident.reported_by.username},\n\n{custom_message}\n\nYour incident titled '{incident.title}' has been processed. Please check for updates.",
                        from_email=from_email, 
                        recipient_list=[incident.reported_by.email],
                    )
                    incident.status = 'Rezolvat'
                    incident.save()
                except Exception as e:
                    messages.error(request, "There was an error sending the email. Please try again.")
                    return render(request, 'review_incident.html', {'incident': incident, 'form': form})
                
 
                messages.success(request, "Răspunsul a fost trimis cu succes!")
                return HttpResponseRedirect(request.path)
            else:
                messages.error(request, "No email address found for the user.")
                return render(request, 'review_incident.html', {'incident': incident, 'form': form})
    
    return render(request, 'review_incident.html', {'incident': incident, 'form': form})

def incident_search(request):
    query = request.GET.get('query', '')
    

    guideline = IncidentGuideline.objects.filter(
        incident_type__icontains=query
    ).first()  
    
    if guideline:

        return redirect('guideline_detail', incident_type=guideline.incident_type)
    

    return redirect('index')

def recommendation_list(request):
    recommendations = IncidentGuideline.objects.all()
    print(recommendations)
    return render(request, 'recommendations_list.html', {'recommendations': recommendations})

@login_required
def user_incidents(request):
    incidents = Incident.objects.filter(reported_by=request.user)
    
    return render(request, 'user_incidents.html', {'incidents': incidents})
