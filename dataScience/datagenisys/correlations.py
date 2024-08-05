
def get_corr(df):
    correlation_matrix = df.corr()
    relevant_columns= {}
    for col in correlation_matrix.columns:
        correlations = correlation_matrix[col]
        correlations = correlations.abs()
        correlations = correlations.drop(col)
        threshold = correlations.quantile(0.75)
        strongly_related_columns = correlations[correlations.abs() > threshold].index.tolist()
        relevant_columns[col] = strongly_related_columns
    return relevant_columns