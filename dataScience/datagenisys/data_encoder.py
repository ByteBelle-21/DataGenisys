from sklearn.preprocessing import LabelEncoder
import pandas as pd

def category_encoder(df, cleaning_steps,categorical_columns):
    encoded_value_map = {}
    for col, dtype in df.dtypes.items():     
        if df[col].nunique() < len(df[col]):
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col])
            df[col] = df[col].astype(int)
            categorical_columns.append(col)
            encoded_value_map[col] = dict(enumerate(encoder.classes_))
            cleaning_steps.append(f"Converted catogorical data in {col} column into numeric data.The mapping of your categorical values is as follows:{dict(enumerate(encoder.classes_))}")
       
    return df,cleaning_steps,categorical_columns,encoded_value_map