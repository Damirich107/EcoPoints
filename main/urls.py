from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submissions/<int:submission_id>/', views.submission_detail, name='submission_detail'),
]