from django.urls import path
from .import views

urlpatterns = [
	path('process/',views.process,name = "Process"),

]