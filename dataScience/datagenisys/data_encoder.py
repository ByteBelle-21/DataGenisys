from sklearn.preprocessing import LabelEncoder
import pandas as pd

def category_encoder(df, cleaning_steps,categorical_columns):
    encoded_value_map = {}
    for col, dtype in df.dtypes.items():
        # When data is integer and does not represents categories
        if dtype == int and col not in categorical_columns:
            if df[col].nunique() == 1:
                unique_value = df[col].unique()[0]
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"Dropped column {col}, because it contains a constant value {unique_value} across all rows.")
            else:
                difference = df[col].diff()
                if (difference[1:]==1).all():
                    df = df.drop(col,axis=1)
                    cleaning_steps.append(f"Dropped column {col}, because it contains unique identifiers such as ID")
        elif dtype == float:
            if df[col].nunique() == 1:
                unique_value = df[col].unique()[0]
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"Dropped column {col}, because it contains a constant value {unique_value} across all rows.")
        elif dtype == bool:
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            df[col] = df[col].astype(int)
            categorical_columns.append(col)
            encoded_value_map[col] = dict(enumerate(encoder.classes_))
            cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
        elif dtype == object:
            if df[col].nunique() == 1:
                    unique_value = df[col].unique()[0]
                    df = df.drop(col,axis=1)
                    cleaning_steps.append(f"Dropped column {col}, because it contains a constant value {unique_value} across all rows.")

            else:
                if pd.to_datetime(df[col], errors='coerce').notna().sum()> len(df[col])/2:
                    converted_data = pd.to_datetime(df[col], errors='coerce')
                    if converted_data.dt.time.any():
                        if converted_data.dt.hour.nunique() < len(converted_data):
                            df['hour_sin'] = np.sin(2 * np.pi * (converted_data.dt.hour) / 24)
                            df['hour_cos'] = np.cos(2 * np.pi * (converted_data.dt.hour) / 24)
                        if converted_data.dt.minute.nunique() < len(converted_data):
                            df['minute_sin'] = np.sin(2 * np.pi * (converted_data.dt.minute) / 60)
                            df['minute_cos'] = np.cos(2 * np.pi * (converted_data.dt.minute) / 60)
                        if converted_data.dt.second.nunique() < len(converted_data):
                            df['second_sin'] = np.sin(2 * np.pi * (converted_data.dt.second) / 60)
                            df['second_cos'] = np.cos(2 * np.pi * (converted_data.dt.second) / 60) 
                          
                    if converted_data.dt.date.any():
                        if converted_data.dt.year.nunique() < len(converted_data):
                            df['year'] = converted_data.dt.year
                        if converted_data.dt.month.nunique() < len(converted_data):
                            df['month_sin'] = np.sin(2 * np.pi * (converted_data.dt.month) / 12)
                            df['month_cos'] = np.cos(2 * np.pi * (converted_data.dt.month) / 12)
                        if converted_data.dt.day.nunique() < len(converted_data):
                            df['day_sin'] = np.sin(2 * np.pi * (converted_data.dt.day) / 31)
                            df['day_cos'] = np.cos(2 * np.pi * (converted_data.dt.day) / 31)
                            
                    cleaning_steps.append(f"Converted datetime data in column {col} into numeric data using cyclic encoding")

                else:
                    if df[col].nunique() == len(df[col]):
                        df = df.drop(col,axis=1)
                        cleaning_steps.append(f"Dropped column {col}, because it contains either unique identifiers or random data.")
                    else:
                        encoder = LabelEncoder()
                        df[col] = encoder.fit_transform(df[col])
                        df[col] = df[col].astype(int)
                        categorical_columns.append(col)
                        encoded_value_map[col] = dict(enumerate(encoder.classes_))
                        cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
            

                




















        # If a column contains only one unique value across all rows
        if df[col].nunique() == 1:
            unique_value = df[col].unique()[0]
            df = df.drop(col,axis=1)
            cleaning_steps.append(f"Dropped column {col}, because it contains a constant value {unique_value} across all rows.")
        # if column contains integer unique IDs
        elif dtype == int:
            difference = df[col].diff()
            if (difference[1:]==1).all():
                df = df.drop(col,axis=1)
                cleaning_steps.append(f"Dropped column {col}, because it contains unique identifiers such as ID")
        # If column contains all unique string values
        elif dtype==object and df[col].nunique() == len(df[col]):
            df = df.drop(col,axis=1)
            cleaning_steps.append(f"Dropped column {col}, because it contains either unique identifiers or random data.")
        # When type is object, the columns containing all distinct data has been removed
        if dtype ==  object:
            # When data id datetime
            if pd.to_datetime(df[col], errors='coerce').notna().sum()> len(df[col])/2:
                pass
            else:
                encoder = LabelEncoder()
                df[col] = encoder.fit_transform(df[col])
                df[col] = df[col].astype(int)
                categorical_columns.append(col)
                encoded_value_map[col] = dict(enumerate(encoder.classes_))
                cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
       

        # When type is datetime
        # When type is boolean
        # When type is int or float



        if df[col].nunique() < len(df[col]):
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            df[col] = df[col].astype(int)
            categorical_columns.append(col)
            encoded_value_map[col] = dict(enumerate(encoder.classes_))
            cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
       
    return df,cleaning_steps,categorical_columns,encoded_value_map