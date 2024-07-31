import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .nan_handler import NaN_handler
from .data_encoder import category_encoder

def home_page(request):
    return render(request,'datagenisys/home_page.html')

def about_us(request):
     return render(request,'datagenisys/about_us.html')

def get_dataset(request):
    got_data = False
    if request.method == 'POST':
        csv_file = request.FILES['csvFile']
        target_variable = request.POST['targetVariable']
        categorical_columns = request.POST['categoricalNumeric']
        Numeric_categorical_columns = []
        if(categorical_columns!="No"):
            Numeric_categorical_columns = [column.strip() for column in categorical_columns.split(',')]
        dataframe = pd.read_csv(csv_file)
        false_target = False
        if(target_variable  not in dataframe.columns):
            false_target = True 
        got_data = True
        data_initial_info = []
        data_cleaning_steps = []
        for col, dtype in dataframe.dtypes.items():
            data_initial_info.append((col,dtype,dataframe[col].isnull().sum())) 

        # Handle the missing values int the dataframe
        dataframe,data_cleaning_steps = NaN_handler(dataframe,Numeric_categorical_columns, data_cleaning_steps)
        dataframe, data_cleaning_steps,Numeric_categorical_columns = category_encoder(dataframe,data_cleaning_steps,Numeric_categorical_columns)
        
        cleaned_dataset = []  
        for col, dtype in dataframe.dtypes.items():
            cleaned_dataset.append((col,dtype,dataframe[col].isnull().sum()))  



        
       
        context = {
            'false_target': false_target,
            'got_data': got_data,
            'data_initial_info':data_initial_info,
            'data_cleaning_steps' : data_cleaning_steps,
            'cleaned_dataset':cleaned_dataset,
        }

        return render(request, 'datagenisys/about_us.html', context)
    return render(request, 'datagenisys/about_us.html', {'got_data': got_data})

