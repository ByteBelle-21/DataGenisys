import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse


def home_page(request):
    return render(request,'datagenisys/home_page.html')

def about_us(request):
     return render(request,'datagenisys/about_us.html')

def get_dataset(request):
    got_data = False
    if request.method == 'POST':
        csv_file = request.FILES['csvFile']
        target_variable = request.POST['targetVariable']
        dataframe = pd.read_csv(csv_file)
        false_target = False
        if(target_variable  not in dataframe.columns):
            false_target = True 
        got_data = True
        column_info = []
        data_cleaning = {}
        for col, dtype in dataframe.dtypes.items():
            column_info.append((col,dtype,dataframe[col].isnull().sum()))
        context = {
            'false_target': false_target,
            'got_data': got_data,
            'column_info':column_info,
        }
        return render(request, 'datagenisys/about_us.html', context)
    return render(request, 'datagenisys/about_us.html', {'got_data': got_data})

