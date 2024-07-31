import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .nan_handler import NaN_handler
from .data_encoder import category_encoder
from .binning import column_bins
from .data_cleaning import df_cleaning

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
        # Drop the columns which contains IDs or random data
        dataframe, data_cleaning_steps = df_cleaning(dataframe,data_cleaning_steps)
        
        temp_df = pd.DataFrame()
        for col, dtype in dataframe.dtypes.items():
            if (dtype==int or dtype== float) and col not in Numeric_categorical_columns:
                temp_df[col] = dataframe[col]

        # Store the data into bins except the provided categorical columns as they are already grouped together
        dataframe, data_cleaning_steps = column_bins(dataframe,Numeric_categorical_columns,data_cleaning_steps)
        # Encode the data into integer data type
        dataframe, data_cleaning_steps,Numeric_categorical_columns,data_encoding_map = category_encoder(dataframe,data_cleaning_steps,Numeric_categorical_columns)
        
        graph_df = pd.DataFrame()
        for col in dataframe.columns:
            if col in temp_df.columns :
                graph_df[col] = temp_df[col]
            else:
                graph_df[col] = dataframe[col]

        print(graph_df.dtypes)
        print(dataframe.dtypes)

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

