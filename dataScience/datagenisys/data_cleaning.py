def df_cleaning(df,cleaning_steps):
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
        # If column contains all unique string values
        elif dtype==object and df[col].nunique() == len(df[col]):
            df = df.drop(col,axis=1)
            cleaning_steps.append(f"Dropped column {col}, because it contains either unique identifiers or random data.")

    return df,cleaning_steps