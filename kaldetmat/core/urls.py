from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('calculate/', views.calculate, name="calculate"),
    path('feedback/', views.feedback, name="feedback"),
]
