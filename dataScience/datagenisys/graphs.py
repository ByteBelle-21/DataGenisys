import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random


def graph_generator(df,input_col,corr_columns,categoricals):
    graphs = []
    plt.figure(figsize=(6,5))
    if input_col in categoricals:
        for col in corr_columns:
            if col in categoricals:
                count_data = df.groupby([input_col , col]).size().unstack().fillna(0)
                count_data.plot(kind='bar', stacked=True)
                plt.xlabel(col)
                plt.ylabel(f"Counts for diffrent {col} values")
            else:
                sns.kdeplot(data=df, x=col, hue=input_col, common_norm=False, fill=True)
                plt.xlabel(col)
                plt.ylabel(f"Distribution of {col} values")
            plt.title(f"Relationship between {col} and {input_col}")
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image = base64.b64encode(buffer.read()).decode('utf-8')  
            graphs.append(f"data:image/png;base64,{image}")

    else:
        for col in corr_columns:
            if col in categoricals:
                sns.kdeplot(data=df, x=input_col, hue=col, common_norm=False, fill=True)
                plt.xlabel(input_col)
                plt.ylabel(f"Distribution of {input_col} values")
            else:
                sns.scatterplot(x=input_col, y=col, data=df)
                plt.xlabel(input_col)
                plt.ylabel(col)
            plt.title(f"Relationship between {col} and {input_col}")
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image = base64.b64encode(buffer.read()).decode('utf-8')  
            graphs.append(f"data:image/png;base64,{image}")                
    return graphs





    
    
       
    
