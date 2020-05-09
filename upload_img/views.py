from django.shortcuts import render
from .models import Person,Image
#from .forms import UploadImgForm,UserName,
from .forms import FileFieldForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings

def home(request):
    return render(request,'upload_img/home.html')

# def upload(request):
#   if request.method=='POST':
#       p_form = UserName(request.POST)
#       i_form = UploadImgForm(request.POST,request.FILES)
#       if p_form.is_valid():
#           n = request.POST['name']
#           n_obj = Person.objects.filter(name = n)
#           if n_obj.exists():
#               name_obj = n_obj.first()
#           else:
#               name_obj = Person(name = n)
#               name_obj.save()
#       if i_form.is_valid():
#           for field in request.FILES.keys():
#               for formfile in request.FILES.getlist(field):
#                   print(formfile)
#                   image = Image(img=formfile,person = name_obj)
#                   image.save()
#   else:
#       p_form = UserName()
#       i_form = UploadImgForm()

#   context={
#       'p_form':p_form,
#       'i_form':i_form
#   } 

#   return render(request,'upload_img/upload.html',context)

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload_img/upload.html'
    success_url = "."

    def post(self,request,*args,**kwargs):
        person_name = request.POST['p_name']

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            p_obj = Person.objects.filter(name = person_name)

            if p_obj.exists():
                person_obj = p_obj.first()
            else:
                person_obj = Person(name=person_name)
                person_obj.save()

            for f in files:
                image = Image(img=f,person = person_obj)
                image.save()            

            messages.success(request,f'Images Have Been Successfully Uploaded!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)