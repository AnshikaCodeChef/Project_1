from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.conf import settings

from .forms import BookForm
from .models import Book
import pandas as pd


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        data = clean_data(uploaded_file)
        partition(data)
        round(data)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)






def clean_data(file):
    data = pd.read_excel(file,index_col= None)
    data.to_csv("csvfile.csv", encoding='utf-8')
    data = data.dropna(axis=0, subset=['Accepted Compound ID'])
    return data

def partition(data):
    data_PC = data[data['Accepted Compound ID'].str.contains("[ ]PC$",regex=True)]
    PC_path = settings.MEDIA_ROOT + '\data_PC'
    data_PC.to_csv(PC_path, index=False)
    data_LPC = data[data['Accepted Compound ID'].str.contains("[ ]LPC$",regex=True)]
    LPC_path = settings.MEDIA_ROOT + '\data_LPC'
    data_LPC.to_csv(LPC_path, index=False)
    data_plas = data[data['Accepted Compound ID'].str.contains("[ ]plasmalogen$",regex=True)]
    plas_path = settings.MEDIA_ROOT + '\data_plas'
    data_plas.to_csv(plas_path, index=False)

def round(data):
    round_reten_time = data['Retention time (min)'].round(decimals=0)
    data_new = data
    data_new['Retention Time Roundoff (in mins)'] = round_reten_time
    New_path = settings.MEDIA_ROOT + '\data_new'
    data_new.to_csv(New_path, index=False)
