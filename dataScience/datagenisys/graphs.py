import seaborn as sns
import seaborn.objects as so
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random


def graph_generator(df,input_col,corr_columns,categoricals,target):
    graphs = []
    if input_col== target:
        for col in corr_columns:
            
            # When both columns are categorical..but one of them is target
            if col in categoricals:
                sns.countplot(df, x=col, hue=input_col)
                plt.title(f"Distribution of {col} by {input_col}")
                plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title=target)
                plt.tight_layout()
                
            # When one column is categorical and another is int or float..and one of them is target
            else:
                color_palette = sns.mpl_palette("viridis", 8)
                sns.kdeplot(data=df, x=col, hue=input_col,fill=True, common_norm=False, palette=color_palette,alpha=.5, linewidth=0,)
                plt.title(f"Density Plot of {col} by {input_col}")
                plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title=target)
                plt.tight_layout()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image = base64.b64encode(buffer.read()).decode('utf-8')  
            graphs.append(f"data:image/png;base64,{image}") 
    else:
        if input_col in categoricals:     
            for col in corr_columns:
                # When both columns are categorical..but none of them is target
                if col in categoricals:
                    if df[col].nunique() > df[input_col].nunique() :
                        plot = sns.FacetGrid(df, col=input_col, hue=target).map(sns.histplot,col,stat="count", multiple="stack")
                        for ax in plot.axes.flat:
                            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
                            ax.set_xlabel(input_col)
                        plt.title(f"Distribution of {col} by {input_col}")
                        plt.legend(loc='upper left', bbox_to_anchor=(1, 1),  title=target)
                        plt.tight_layout()
                        
                    else:
                        plot = sns.FacetGrid(df, col=col, hue=target).map(sns.histplot,input_col,stat="count", multiple="stack")
                        for ax in plot.axes.flat:
                            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                            ax.set_xlabel(col)
                        plt.title(f"Distribution of {input_col} by {col}")
                        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title=target)
                        plt.tight_layout()
         
                # When one column is categorical and another is int or float..but none of them are target
                else:
                    sns.boxenplot(data=df, x=input_col, y=col, hue=target, gap=.2)
                    plt.title(f"Distribution of {input_col} Across different {col}")
                    plt.legend(loc='upper left', bbox_to_anchor=(1, 1),  title=target)
                    plt.tight_layout()
                    
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
                    sns.boxenplot(data=df, x=col, y=input_col, hue=target, gap=.2)
                    plt.title(f"Distribution of {col} Across different {input_col}")
                    plt.legend(loc='upper left', bbox_to_anchor=(1, 1),  title=target)
                    plt.tight_layout()
                    
                # When both columns are not categorical..and none of them is target
                else:
                    sns.FacetGrid(df, col=target).map_dataframe(sns.scatterplot, x=col, y=input_col)
                    plt.title(f"Relationship Between {input_col} and {col}")
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                image = base64.b64encode(buffer.read()).decode('utf-8')  
                graphs.append(f"data:image/png;base64,{image}")              
    return graphs

