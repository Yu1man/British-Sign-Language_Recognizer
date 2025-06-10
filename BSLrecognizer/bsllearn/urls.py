from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Video feed for real-time streaming
    path('video_feed/', views.video_feed, name='video_feed'),

    # Detection info for real-time updates
    path('detection_info/', views.detection_info, name='detection_info')
]