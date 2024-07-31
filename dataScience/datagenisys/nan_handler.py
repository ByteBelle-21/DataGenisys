from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

def NaN_handler(df, categorical_columns,cleaning_steps):
    for col, dtype in df.dtypes.items():
        # if column contains string values
        if dtype == object:
            # When pandas misinterpretes None as Nan, but None represents a value 
            if(df[col]=="").sum() ==0 and df[col].isnull().sum() > 0:
                df[col] = df[col].replace(np.nan,'none')
                cleaning_steps.append(f"pandas detected None string as NaN in {col} column. So replaced None with none") 
                
            # When more than 30% values are missing 
            elif (df[col]=="").sum()/len(df[col]) >= 0.3 :
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"The {col} had more than 30% missing values and it has been dropped.")
                
            # When percentage of missing value is less than 30%
            elif (df[col]=="").sum()/len(df[col]) * 100 < 0.3 and (df[col]=="").sum()/len(df[col]) > 0 :
                imputer = SimpleImputer(strategy ='most_frequent')
                df[col] = imputer.fit_transform(df[[col]]).ravel()
                cleaning_steps.append(f"Replaced the missing values in {col} column with most frequent value")
                


        # if column contains integers or floats
        elif dtype == int or dtype == float :
            # When more than 30% values are missing 
            if df[col].isnull().sum()/len(df[col]) >= 0.3 :
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"The {col} had more than 30% missing values and it has been dropped.")
            
            # When percentage of missing value is less than 30% 
            elif df[col].isnull().sum()/len(df[col]) * 100 < 0.3 and df[col].isnull().sum()/len(df[col]) > 0 :
                if col in categorical_columns:
                    imputer = SimpleImputer(strategy ='most_frequent')
                    df[col] = imputer.fit_transform(df[[col]]).ravel()
                    cleaning_steps.append(f"Replaced the missing values in {col} column with most frequent value")
                else:
                    column_mean = df[col].mean()
                    df[col] = df[col].replace(np.nan, column_mean)
                    cleaning_steps.append(f"Replaced the missing values in {col} column with column mean")
           
        elif dtype == bool:
            # When more than 30% values are missing 
            if df[col].isnull().sum()/len(df[col]) >= 0.3 :
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"The {col} had more than 30% missing values and it has been dropped.")
                
            # When percentage of missing value is less than 30%
            elif df[col].isnull().sum()/len(df[col]) * 100 < 0.3 and df[col].isnull().sum()/len(df[col]) > 0 :
                mode_value = df[col].mode()[0]
                df[col].fillna(mode_value, inplace=True)
                cleaning_steps.append(f"Replaced the missing values in {col} column with mode value {mode_value}")
    
    return df,cleaning_steps;
 
                


    
    
            

