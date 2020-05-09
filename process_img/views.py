from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

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
import os


# Create your views here.
def process(request):
    pre = preprocess()
    print("Loading Of Model Parameters....")
    aligned_dict,names = pre.align()
    # print(aligned_dict,names)
    print("Images Have Been Aligned Successfully.....")
    embeddings_dict = pre.compute_embeddings(aligned_dict)
    #print(embeddings_dict)
    pickled_file = open('embedding_pickle','wb')
    # print(embeddings_dict)
    pickle.dump(embeddings_dict,pickled_file)
    pickled_file.close()
    print("Embeddings Of Aligned Images is computed Successfully....")
    # pickled_file = open('embedding_pickle','rb')
    # pf = pickle.load(pickled_file)
    # print(pf)
    # print("Done")
    # pickled_file.close()
    messages.success(request,f'Images Have Been Successfully Processed!')
    return redirect('home')


class preprocess:
    def __init__(self):

        self.workers = 0 if os.name == 'nt' else 4
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # print(f"Device Available is {self.device}")

        PATH = os.path.join(settings.BASE_DIR,"media/unaligned_images")
        self.dataset = datasets.ImageFolder(PATH)
        self.dataset.idx_to_class = {i:c for c,i in self.dataset.class_to_idx.items()}
        self.loader = DataLoader(self.dataset, collate_fn = lambda x : x[0], num_workers=self.workers)

        #print(self.dataset.idx_to_class)


        '''To visualise images '''
        # for x,y in self.loader:
  #             plt.imshow(x)
  #             print(y)
  #             plt.pause(5)

    def align(self):
        self.mtcnn = MTCNN()
        self.aligned = {}
        self.names= []
        self.i=0
        PATH = os.path.join(settings.BASE_DIR,"media/aligned_images")
        for x,y in self.loader:
            self.path = PATH + '/' + self.dataset.idx_to_class[y] + "/" + self.dataset.idx_to_class[y] + str(self.i) + ".jpg"
            #print(x,type(x))
            self.x_aligned,self.prob = self.mtcnn(x, save_path = self.path,return_prob=True)
            self.i+=1
            if self.x_aligned is not None:
                #print('Face detected with probability: {:8f}'.format(self.prob))
                if self.aligned.get(self.dataset.idx_to_class[y])==None:
                    self.aligned[self.dataset.idx_to_class[y]] = [self.x_aligned]
                else:
                    self.aligned.get(self.dataset.idx_to_class[y]).append(self.x_aligned)
                if self.dataset.idx_to_class[y] not in self.names:
                    self.names.append(self.dataset.idx_to_class[y])
        return self.aligned,self.names
    

    def compute_embeddings(self,aligned_dict):
        self.resnet = InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
        self.i=0
        self.embeddings={}
        for k,v in aligned_dict.items():
            v = torch.stack(v).to(self.device)
            embedding = self.resnet(v).detach().cpu()
            self.embeddings[k] = embedding
        # print(self.embeddings)
        return self.embeddings