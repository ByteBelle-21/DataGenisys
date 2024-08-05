import seaborn as sns
import seaborn.objects as so
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random


def graph_generator(df,input_col,corr_columns,categoricals,encoding_dict,target):
    graphs = []
    print(encoding_dict)
    if input_col== target:
        for col in corr_columns:
            df[input_col] = df[input_col].map(encoding_dict[input_col])
            # When both columns are categorical..but one of them is target
            if col in categoricals:
                df[col] = df[col].map(encoding_dict[col])
                sns.countplot(titanic, x=col, hue=input_col)
                print("count")
            # When one column is categorical and another is int or float..and one of them is target
            else:
                sns.kdeplot(data=df, x=col, hue=input_col,fill=True, common_norm=False, palette="crest",alpha=.5, linewidth=0,)
                print("kdeplot")
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image = base64.b64encode(buffer.read()).decode('utf-8')  
            graphs.append(f"data:image/png;base64,{image}") 
    else:
        if input_col in categoricals:
            df[input_col] = df[input_col].map(encoding_dict[input_col])
            for col in corr_columns:
                # When both columns are categorical..but none of them is target
                if col in categoricals:
                    df[col] = df[col].map(encoding_dict[col])
                    if df[col].nunique() > df[input_col].nunique() :
                        sns.FacetGrid(df, col=input_col, hue=target).map(sns.histplot, col)
                        print("FacetGrid")
                    else:
                        sns.FacetGrid(df, col=input_col, hue=target).map(sns.histplot,col,stat="count", multiple="stack")
                        plt.xlabel({col})
                        print("FacetGrid2")   
                # When one column is categorical and another is int or float..but none of them are target
                else:
                    sns.boxenplot(data=df, x=input_col, y=col, hue=target, gap=.2)
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                image = base64.b64encode(buffer.read()).decode('utf-8')  
                graphs.append(f"data:image/png;base64,{image}") 
        else:
            for col in corr_columns:
                # When one column is categorical and another is int or float..but none of them are target
                if col in categoricals:
                    df[col] = df[col].map(encoding_dict[col])
                    sns.boxenplot(data=df, x=col, y=input_col, hue=target, gap=.2)
                    print("lineplot")
                # When both columns are not categorical..and none of them is target
                else:
                    sns.FacetGrid(df, col=target).map_dataframe(sns.scatterplot, x=col, y=input_col)
                    print("scatterplot")
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                image = base64.b64encode(buffer.read()).decode('utf-8')  
                graphs.append(f"data:image/png;base64,{image}")              
    return graphs

