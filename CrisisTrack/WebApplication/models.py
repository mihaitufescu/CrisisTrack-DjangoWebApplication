from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('reporter', 'Reporter'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reporter')
    organization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Incident Categories Model
class IncidentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Recommendations Model
class Recommendation(models.Model):
    incident_category = models.ForeignKey(IncidentCategory, on_delete=models.CASCADE, related_name='recommendations')
    description = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.incident_category.name}"


# Incident Model
class Incident(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(IncidentCategory, on_delete=models.CASCADE, related_name='incidents')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    organization = models.CharField(max_length=255, blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category.name} ({self.status})"

class IncidentGuideline(models.Model):
    incident_type = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    steps = models.TextField()  # Use JSONField for structured data if needed
    video_url = models.URLField(max_length=500, blank=True, null=True)  # Optional video
    research_paper_links = models.TextField(blank=True, null=True)  # Store multiple links separated by newline

    def get_research_papers(self):
        # Split research_paper_links into a list for easy template rendering
        return self.research_paper_links.split("\n") if self.research_paper_links else []

    def __str__(self):
        return self.incident_type