from django.urls import path
from conversor import views

app_name = 'conversor'

urlpatterns = [
    path('', views.ConversorMonetario.as_view()),
]