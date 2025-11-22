# FEATURES (X)
# TARGET (y)
def get_features_target(df):
    if df is None: return None

    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    return X, y
