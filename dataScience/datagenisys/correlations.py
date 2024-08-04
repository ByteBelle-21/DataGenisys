
def get_corr(df):
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
    return relevant_columns