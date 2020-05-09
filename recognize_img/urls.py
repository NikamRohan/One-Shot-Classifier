from django.urls import path
from . import views
from .views import FileFieldView


urlpatterns = [
	path('recognize/',FileFieldView.as_view(),name = "Recognize"),

]