import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .nan_handler import NaN_handler
from .data_encoder import category_encoder
from .correlations import get_corr
from .graphs import graph_generator
import json

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

        datetime_cols = {
            'original_col' :[],
            'new_cols' :[]
        }

        dataframe, data_cleaning_steps,Numeric_categorical_columns,data_encoding_map, datetime_cols = category_encoder(dataframe,data_cleaning_steps,Numeric_categorical_columns,datetime_cols)
        correlation_dict = get_corr(dataframe)
        cleaned_dataset = []
        print(correlation_dict)

        for col, dtype in dataframe.dtypes.items():
            if col != target_variable:
                graphs_url = graph_generator(dataframe,col,correlation_dict[col],False,Numeric_categorical_columns)
            else:
                graphs_url = graph_generator(dataframe,col,correlation_dict[col],True,Numeric_categorical_columns)
                
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



