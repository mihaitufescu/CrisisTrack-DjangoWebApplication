# CrisisTrack

**CrisisTrack** is a Django-based web application for reporting, managing, and educating users about cybersecurity incidents. It offers a user-friendly interface for submitting incidents, accessing relevant guidelines, and receiving administrative feedback.

## Features

- User registration, login, and logout functionality
- Authenticated incident reporting with categorization
- Admin interface for reviewing and responding to reported incidents
- Email notifications to users upon incident review
- Search functionality for cybersecurity guidelines
- Database models for incidents, recommendations, categories, and guidelines
- Structured documentation and configuration for on-premise deployments

## Technologies Used

- Django (Python)
- PostgreSQL (or your configured database)
- HTML/CSS templates (with Django templating)
- Apache NiFi (optional, for external pipeline integration)
- SMTP for email notifications
- Docker (optional for deployment)
- Apache Airflow and AWS (used for separate data engineering components, if integrated)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- PostgreSQL or SQLite
- Virtualenv (recommended)
