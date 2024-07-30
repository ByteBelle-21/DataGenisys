import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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
            if dtype == object:
                if(dataframe[col]=="").sum() ==0 and dataframe[col].isnull().sum() > 0:
                    dataframe[col] = dataframe[col].replace(np.nan,'none')
                    data_cleaning_steps.append(f"pandas detected None string as NaN in {col} column. So replaced None with none")     
                elif (dataframe[col]=="").sum()/len(dataframe[col]) * 100 <= 0.3 and (dataframe[col]=="").sum()/len(dataframe[col]) * 100 > 30 :
                    imputer = SimpleImputer(strategy ='most_frequent')
                    dataframe[col] = imputer.fit_transform(dataframe[[col]]).ravel()
                    data_cleaning_steps.append(f"Replaced the missing values in {col} column with most frequent value")
                elif (dataframe[col]=="").sum()/len(dataframe[col]) > 0.3 and (dataframe[col]=="").sum()/len(dataframe[col]) < 0.5:
                    dataframe[col] = dataframe[col].replace(np.nan,'Unknown')
                    data_cleaning_steps.append(f"Replaced the missing values in {col} column with 'Unknown'")
                elif (dataframe[col]=="").sum()/len(dataframe[col]) >= 0.5 :
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"The {col} had more than 50% missing values and it has been dropped.")
            elif dtype == int or dtype == float : 
                if dataframe[col].isnull().sum()/len(dataframe[col]) >= 0.5 :
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"The {col} had more than 50% missing values and it has been dropped.")
                elif col in Numeric_categorical_columns:
                    if dataframe[col].isnull().sum()/len(dataframe[col]) < 0.5 and dataframe[col].isnull().sum()/len(dataframe[col]) >0.3 :
                        replacer = dataframe[col].max() + 1
                        dataframe[col] = dataframe[col].replace(np.nan,replacer)
                        data_cleaning_steps.append(f"Replaced the missing values in {col} column with {replacer} value. This value indiates that data is missing")
                    elif dataframe[col].isnull().sum()/len(dataframe[col]) <= 0.3 and dataframe[col].isnull().sum()/len(dataframe[col]) > 0:
                        imputer = SimpleImputer(strategy ='most_frequent')
                        dataframe[col] = imputer.fit_transform(dataframe[[col]]).ravel()
                        data_cleaning_steps.append(f"Replaced the missing values in {col} column with most frequent value")
                elif dataframe[col].isnull().sum()/len(dataframe[col]) < 0.5 and dataframe[col].isnull().sum()/len(dataframe[col]) > 0:
                    col_mean = dataframe[col].mean()
                    dataframe[col] = dataframe[col].replace(np.nan, col_mean)
                    data_cleaning_steps.append(f"Replaced the missing values in {col} column with column mean")

        for col, dtype in dataframe.dtypes.items():
            if dtype == object:
                if len(dataframe[col].unique()) < len(dataframe[col]):
                    encoder = LabelEncoder()
                    dataframe[col] = encoder.fit_transform(dataframe[col])
                    dataframe[col] = dataframe[col].astype(int)
                    data_cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
                else:
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"Droped column {col}, beacuse it contains either unique identifiers or random data.") 
            elif dtype == int or dtype == float:
                # find more efficient method here
                if len(dataframe[col].unique()) == len(dataframe[col]) and (dataframe[col].max() - dataframe[col].min()) >= len(dataframe[col]) -1 :
                    dataframe = dataframe.drop(col,axis=1)
                    data_cleaning_steps.append(f"Droped column {col}, beacuse it contains either unique identifiers or random data.")
                else:
                    bins = np.linspace(dataframe[col].min(),dataframe[col].max(),6)
                    labels =[f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins)-1)]
                    dataframe["temp_col"] = dataframe[col]
                    dataframe[col] = pd.cut(dataframe["temp_col"],bins=bins,labels=labels,include_lowest = True)
                    data_cleaning_steps.append(f"Transformed column '{col}' by binning with {len(bins) - 1} bins: {', '.join(labels)}.")
                 
            #elif dtype == datetime:
            #elif dtype == bool:




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

