import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random


def graph_generator(df,dependent_col,categorical_columns,datetime_columns):
    # this dataframe already contains newly created columns
    correlation_matrix = df.corr()
    relevant_columns= {}
    processed_pairs = set()
    for col in correlation_matrix.columns:
        correlations = correlation_matrix[col]
        correlations = correlations.abs()
        correlations = correlations.drop(col)
        threshold = correlations.quantile(0.75)
        strongly_related_columns = correlations[correlations.abs() > threshold].index.tolist()
        new_correlated_cols = []
        for related_col in strongly_related_columns:
            col_pair = tuple(sorted([col,related_col]))
            if col_pair not in processed_pairs:
                processed_pairs.add(col_pair)
                new_correlated_cols.append(related_col)
        if new_correlated_cols:
            relevant_columns[col] = new_correlated_cols
                
    print(relevant_columns)
    
        
        

    """
    correlation_matrix = df.corr()[dependent_col]
    correlations = correlation_matrix.drop(dependent_col)
    correlations = correlations.abs()
    lower_percentile = correlations.quantile(0.25)
    upper_percentile = correlations.quantile(0.75)
    
    graphs = []
    for col in strongly_related_columns:
        if col not in datetime_columns['original_col']:
            plt.figure(figsize=(6,5))
            if col in categorical_columns:
                temp_df = pd.DataFrame(df.groupby(col)[dependent_col].sum())
                total_bars = len(temp_df)
                colors = sns.color_palette('husl', total_bars)
                plot_choice  = random.choice(['bar','pie'])
                if total_bars > 2 and plot_choice == 'pie' :
                    plt.pie(temp_df[dependent_col], labels=temp_df.index, autopct='%1.1f%%', colors=colors)
                else:
                    sns.barplot(x=col,y=dependent_col, data=temp_df, palette=colors)
                    plt.xlabel(col)
                    plt.ylabel(f"No. of {dependent_col}")

            else:
                total_values = df[dependent_col].nunique()
                colors = sns.color_palette('husl', total_values)
                sns.kdeplot(data=df, x=col, hue=dependent_col, common_norm=False, fill=True)
                #sns.boxenplot(x=dependent_col, y=col, data=df,palette='coolwarm')

            plt.title(f"Relationship between {col} and {dependent_col}")
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image = base64.b64encode(buffer.read()).decode('utf-8')  
            graphs.append(f"data:image/png;base64,{image}")
    return graphs
"""



    
    
       
    
