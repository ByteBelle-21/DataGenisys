from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import warnings

def column_bins(df,categorical_columns,cleaning_steps):
    warnings.filterwarnings('ignore', category=UserWarning, module='pandas')
    for col, dtype in df.dtypes.items():
        if col not in categorical_columns:
            # If the column represents datetime data
            if dtype == object and pd.to_datetime(df[col], errors='coerce').notna().sum()> len(df[col])/2:
                convert_to_datetime = pd.to_datetime(df[col], errors='coerce')
                earliest_datetime = convert_to_datetime.min()
                recent_datetime = convert_to_datetime.max()
                range_datetime = recent_datetime - earliest_datetime

                # if column represents date and time
                if convert_to_datetime.dt.date.any():
                    if convert_to_datetime.dt.time.any():
                        df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
                    else:
                        df[col] = pd.to_datetime(df[col],format='%m/%d/%Y', errors='coerce')

                    if range_datetime.days > 0 and range_datetime.days <= 7:
                        frequency = 'D'
                    elif range_datetime.days > 7 and range_datetime.days <= 30:
                        frequency = 'W'
                    elif range_datetime.days > 30 and range_datetime.days <= 366:
                        frequency = 'M'
                    elif range_datetime.days > 366:
                        frequency = 'Y'
                    
                # if column represents time
                elif not convert_to_datetime.dt.date.any() and convert_to_datetime.dt.time.any():
                    df[col] = pd.to_datetime(df[col],format='%I:%M:%S %p', errors='coerce')
                    total_seconds = range_datetime.total_seconds()
                    if total_seconds > 0 and total_seconds <= 60:
                        frequency = '12S'
                    elif total_seconds > 60 and total_seconds <= 3600:
                        frequency = '15T'
                    elif total_seconds > 3600 and range_datetime.days <= 86400:
                        frequency = 'H'
                    elif range_datetime.days > 86400:
                        frequency = 'D'
                
                bins = pd.date_range(start=earliest_datetime, end=recent_datetime, freq=frequency) 
                labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins) - 1)]
                df["temp_col"] = df[col]
                df[col] = pd.cut(df["temp_col"], bins=bins, labels=labels, include_lowest=True)
                df.drop(columns=["temp_col"], inplace=True)
                cleaning_steps.append(f"Transformed column '{col}' by binning with {len(bins) - 1} bins.")
            
            # If the column represents int or float data
            elif dtype == int or dtype == float:
                column_min = df[col].min()
                column_max = df[col].max()
                bins = np.linspace(column_min,column_max,6)
                if dtype == float:
                    labels = [f'{round(bins[i], 3)}-{round(bins[i+1], 3)}' for i in range(len(bins) - 1)]
                else:
                    labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins) - 1)]
                df["temp_col"] = df[col]
                df[col] = pd.cut(df["temp_col"], bins=bins, labels=labels, include_lowest=True)
                df.drop(columns=["temp_col"], inplace=True)
                cleaning_steps.append(f"Transformed column '{col}' by binning with {len(bins) - 1} bins.")

    return df, cleaning_steps
           
