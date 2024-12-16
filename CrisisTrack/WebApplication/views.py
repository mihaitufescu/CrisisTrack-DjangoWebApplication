from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, IncidentCreationForm, ReviewIncidentForm
from django.contrib.auth.decorators import login_required
from .models import Incident, IncidentGuideline
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import urllib, base64

# Home View
def index(request):
    return render(request, 'index.html', {
        'app_name': 'CrisisTrack',
        'app_description': 'A platform to report and manage cybersecurity incidents efficiently.'
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
            incident.reported_by = request.user  # Attach the logged-in user to the incident
            incident.save()
            return redirect('index')  # Redirect to the list of incidents or any page you'd prefer
    else:
        form = IncidentCreationForm()
    return render(request, 'create_incident.html', {'form': form})

@login_required
def incident_list(request):
    # Get all incidents (no filtering on the server side)
    incidents = Incident.objects.all()
    print(f"Number of incidents: {incidents.count()}")
    return render(request, 'incidents_list.html', {
        'incidents': incidents,
    })

def guidelines(request):
    return render(request, 'guidelines.html')

def guideline_detail(request, incident_type):
    guideline = get_object_or_404(IncidentGuideline, incident_type=incident_type)
    steps = guideline.steps.split("\\n")  # your original line
    print(steps)
    return render(request, 'guideline_detail.html', {
        'incident_type': guideline.incident_type,
        'description': guideline.description,
        'steps': steps,
        'video_url': guideline.video_url,
        'research_papers': guideline.get_research_papers(),
    })

def review_incident(request, incident_id):
    # Fetch the incident by ID
    incident = get_object_or_404(Incident, id=incident_id)
    
    # You can now pass the incident to the template to display details
    incident = get_object_or_404(Incident, id=incident_id)
    
    # Handle GET request to show the form
    if request.method == 'GET':
        form = ReviewIncidentForm()
        return render(request, 'review_incident.html', {'incident': incident, 'form': form})
    
    # Handle POST request to process the form and send the email
    elif request.method == 'POST':
        form = ReviewIncidentForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data['custom_message']
            
            # Send email to the reported_by user
            if incident.reported_by.email:
                send_mail(
                    subject=f"Incident Update: {incident.title}",
                    message=f"Dear {incident.reported_by.username},\n\n{custom_message}\n\nYour incident titled '{incident.title}' has been processed. Please check for updates.",
                    from_email='admin@example.com',  # Replace with your admin email
                    recipient_list=[incident.reported_by.email],
                )
            
            # Redirect to the incident list page after sending the email
            return HttpResponseRedirect('/admin/WebApplication/incident/')  # Or redirect to any desired page
    
    return render(request, 'web_application/review_incident.html', {'incident': incident, 'form': form})