from django.contrib import admin
from .models import Recognize_Image,Predicted_Class
# Register your models here.

admin.site.register(Recognize_Image)
admin.site.register(Predicted_Class)
