from django import forms
# from django.contrib.auth.models import User
# from .models import Image,Person

# class UserName(forms.ModelForm):
# 	class Meta:
# 		model = Person
# 		fields = ['name']

# class UploadImgForm(forms.ModelForm):
# 	class Meta:
# 		model = Image
# 		fields = ['img']


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


