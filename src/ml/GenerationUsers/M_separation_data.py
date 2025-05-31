import pandas as pd
from sklearn.model_selection import train_test_split


def separation(path):
    df = pd.read_csv(path)

    X = df[[col for col in df.columns if not col.endswith('_s')]]

    y = df[[col for col in df.columns if col.endswith('_s')]]

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42, shuffle=True)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, shuffle=True)
    
    return X_train, y_train, X_val, y_val, X_test, y_test