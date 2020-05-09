from django.shortcuts import render
from .models import Recognize_Image,Predicted_Class
from django.conf import settings
from .forms import FileFieldForm1
from django.views.generic.edit import FormView

# FACENET Imports
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os
import torchvision
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

import pickle
from PIL import Image


class FileFieldView(FormView):
    form_class = FileFieldForm1
    template_name = 'recognize_img/img_recognize.html'
    success_url = "../recognize_img/"

    def post(self,request,*args,**kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')

        if form.is_valid():

            for f in files:
                image = Recognize_Image(img=f)
                image.save()
                #print(image)
                img_url = os.path.join(settings.BASE_DIR,"media/uploaded_imgs_for_recognition/",str(f))
                img = Image.open(img_url)
                

                self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                self.mtcnn = MTCNN()
                self.resnet = InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
                x_aligned = self.mtcnn(img,return_prob = False)
                if x_aligned is not None:
                    aligned = torch.stack([x_aligned]).to(self.device)
                    e = self.resnet(aligned).detach().cpu()

                    pickled_file = open('embedding_pickle','rb')
                    pf = pickle.load(pickled_file)
                    # print(pf.items())
                    min_dist = 1000
                    for k,v in pf.items():
                        for i in range(v.shape[0]):
                            dist = (e-v[i]).norm().item()
                            # print(dist,k)
                            if dist<min_dist:
                                min_dist = dist
                                name = k
                    url_img = "http://127.0.0.1:8000/media/uploaded_imgs_for_recognition/" + str(f)
                    if min_dist<0.95:
                        self.context = {
                            'predicted_person': name,
                            'img_url' : url_img,
                            'flag' : 1
                        }
                        f=1
                    else:
                        name = 'Unknown'
                        self.context = {
                            'predicted_person': name,
                            'img_url' : url_img,
                            'flag' : 0
                        }
                        f=1
                    # print(self.context)
                    # print(name,min_dist)
                    # print("---------------------")
                    pickled_file.close()

                else:
                    url_img = "http://127.0.0.1:8000/media/uploaded_imgs_for_recognition/" + str(f)
                    name = 'No Face Detected in Image'
                    self.context = {
                        'predicted_person': name,
                        'img_url' : url_img,
                        'flag' : -1
                    }

                for file in files:
                    image = Predicted_Class(img_predicted = file,p_name = name)    
                    image.save()


            return self.form_valid(form,f)

        else:
            return self.form_invalid(form)

    def form_valid(self,form,f):
        response = super().form_valid(form)
        if f:
            return render(self.request,"recognize_img/recognized.html", self.context)
        else:
            return render(self.request,"recognize_img/noface.html", self.context)

