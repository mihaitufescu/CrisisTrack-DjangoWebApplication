from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_incident/', views.create_incident, name='create_incident'),
    path('incidents_list/', views.incident_list, name='incident_list'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('guideline/<str:incident_type>/', views.guideline_detail, name='guideline_detail'),
    path('review_incident/<int:incident_id>/', views.review_incident, name='review_incident'),
    path('incident_search/', views.incident_search, name='incident_search'),
    path('recommendations/', views.recommendation_list, name='recommendation_list'),
    path('my-incidents/', views.user_incidents, name='user_incidents'),
]
