from datetime import datetime, timedelta

def column_bins(df,categorical_columns,cleaning_steps):
    for col, dtype in df.dtypes,items():
        if col not in categorical_columns:
            # If the column represents datetime data
            convert_to_datetime = pd.to_datetime(df[col], errors='coerce')
            if dtype == object and convert_to_datetime.notna().sum()> len(df[col])/2:
                earliest_datetime = df[col].min()
                recent_datetime = df[col].max()
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


    

                
                

            # If the column represents int or float data
