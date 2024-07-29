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
        categorical_columns = request.POST['categoricalNumeric']
        if(categorical_columns!="No"):
            Numeric_categorical_columns = [column.strip() for column in categorical_columns.split(',')]
        dataframe = pd.read_csv(csv_file)
        false_target = False
        if(target_variable  not in dataframe.columns):
            false_target = True 
        got_data = True
        column_info = []
        data_cleaning_steps = []
        for col, dtype in dataframe.dtypes.items():
            column_info.append((col,dtype,dataframe[col].isnull().sum()))  
            if dtype== object:
                if(dataframe[col]=="").sum() ==0 and dataframe[col].isnull().sum() > 0:
                    dataframe[col] = dataframe[col].replace(np.nan,'none')
                    data_cleaning_steps.append(f"pandas detected None string as NaN in {col} column. So replaced None with none")     
                elif (dataframe[col]=="").sum()/len(dataframe[col]) < 0.5:
                    dataframe[col] = dataframe[col].replace(np.nan,'Unknown')
                    data_cleaning_steps.append(f"Replaced the missing values in {col} column with 'Unknown'")
                elif (dataframe[col]=="").sum()/len(dataframe[col]) >= 0.5 :
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"The {col} had more than 50% missing values and it has been dropped.")
            elif dtype == int or dtype == float : 
                if (dataframe[col]=="").sum()/len(dataframe[col]) >= 0.5 :
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"The {col} had more than 50% missing values and it has been dropped.")
                elif col in Numeric_categorical_columns:
                     pass
                else:
                    col_mean = dataframe[col].mean()
                    dataframe[col] = dataframe[col].replace(np.nan, col_mean)


        context = {
            'false_target': false_target,
            'got_data': got_data,
            'column_info':column_info,
            'data_cleaning_steps' : data_cleaning_steps,
        }
        return render(request, 'datagenisys/about_us.html', context)
    return render(request, 'datagenisys/about_us.html', {'got_data': got_data})

