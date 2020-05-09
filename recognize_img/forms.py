from django import forms

class FileFieldForm1(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))