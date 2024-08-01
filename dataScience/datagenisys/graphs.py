import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def graph_generator(df,dependent_col,temp_df):
    graph_urls = []
    for col in df.columns:
        if col != dependent_col:
            plt.figure(figsize=(6,4))
            if col in temp_df.columns:
                sns.lineplot(x=col,y=dependent_col,data=df)
            else:
                temp_df = pd.DataFrame(df.groupby(col)[dependent_col].sum())
                sns.barplot(x=col,y=dependent_col, data=temp_df)
        plt.xlabel(col)
        plt.ylabel(dependent_col)
        plt.title(f"Relationship between {col} and {dependent_col}")
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image = base64.b64encode(buffer.read()).decode('utf-8')  
        graph_urls.append(f"data:image/png;base64,{image}")

    return graph_urls