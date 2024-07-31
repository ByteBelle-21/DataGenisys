from sklearn.preprocessing import LabelEncoder
import pandas as pd



def category_encoder(df, cleaning_steps,categorical_columns):
    for col, dtype in df.dtypes.items():
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

        # When the column contains string data
        elif dtype == object:
            # if column does not contains datetime data
            if pd.to_datetime(df[col], errors='coerce').notna().sum() == 0 :
                # If column contains some categories
                if df[col].nunique() < len(df[col]):
                    encoder = LabelEncoder()
                    df[col] = encoder.fit_transform(df[col])
                    df[col] = df[col].astype(int)
                    categorical_columns.append(col)
                    cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
                # If column contains all unique string values
                elif df[col].nunique() == len(df[col]):
                    df = df.drop(col,axis=1)
                    cleaning_steps.append(f"Dropped column {col}, because it contains either unique identifiers or random data.")
        # If column contains boolean  data
        elif dtype == bool:
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            df[col] = df[col].astype(int)
            categorical_columns.append(col)
            cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
       
    return df,cleaning_steps,categorical_columns