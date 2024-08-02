import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import random


def graph_generator(df,independent_col,dependent_col,is_categorical):
    plt.figure(figsize=(6,5))
    if is_categorical==False:
        temp_df = df.groupby([independent_col, dependent_col]).size().reset_index(name='count')
        #sns.catplot(x=independent_col,y='count', data=temp_df,hue=dependent_col)
        sns.lineplot(data=temp_df, x=independent_col, y='count', hue=dependent_col, palette='coolwarm')
        plt.xlabel(independent_col)
        plt.ylabel(f"No. of {dependent_col}")
        #sns.lineplot(data=age_counts, x=independent_col, y='count', hue=dependent_col, palette='coolwarm')
        #sns.lineplot(x=independent_col,y=dependent_col,data=df)
    else:
        plot_choice  = random.choice(['bar','pie'])
        temp_df = pd.DataFrame(df.groupby(independent_col)[dependent_col].sum())
        total_bars = len(temp_df)
        colors = sns.color_palette('husl', total_bars)
        if plot_choice == 'bar':
            sns.barplot(x=independent_col,y=dependent_col, data=temp_df, palette=colors)
            plt.xlabel(independent_col)
            plt.ylabel(f"No. of {dependent_col}")
        else:
            plt.pie(temp_df[dependent_col], labels=temp_df.index, autopct='%1.1f%%', colors=colors)
    plt.title(f"Relationship between {independent_col} and {dependent_col}")
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image = base64.b64encode(buffer.read()).decode('utf-8')  
    return f"data:image/png;base64,{image}"
