import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .nan_handler import NaN_handler
from .data_encoder import category_encoder
from .binning import column_bins
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
        
        cleaned_dataset = []  
        for col, dtype in dataframe.dtypes.items():
            cleaned_dataset.append((col,dtype,dataframe[col].isnull().sum()))  

        graph_urls = graph_generator(dataframe,target_variable,Numeric_categorical_columns,datetime_cols)
        
        """
        for col in dataframe.columns:
            if col != target_variable and col not in datetime_cols['original_col'] :
                if col in Numeric_categorical_columns or col in datetime_cols['new_cols'] :
                    graph_urls.append(graph_generator(dataframe,col,target_variable,True))
                else:
                    graph_urls.append(graph_generator(dataframe,col,target_variable,False))
        """
        context = {
            'false_target': false_target,
            'got_data': got_data,
            'data_initial_info':data_initial_info, 
            'data_cleaning_steps' : data_cleaning_steps,
            'cleaned_dataset':cleaned_dataset,
            'graph_urls':graph_urls
        }

        return render(request, 'datagenisys/about_us.html', context)
    return render(request, 'datagenisys/about_us.html', {'got_data': got_data})




