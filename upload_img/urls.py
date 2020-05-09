from django.urls import path
from . import views
from .views import FileFieldView


urlpatterns = [
	path('',views.home,name="home"),
	path('upload/',FileFieldView.as_view(),name="Upload"),
]