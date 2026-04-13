import pandas as pd

def detect_anomalies(df, column='demand', window=7):
    df = df.copy()
    df['rolling_mean'] = df[column].rolling(window=window).mean()
    df['rolling_std'] = df[column].rolling(window=window).std()
    df['z_score'] = (df[column] - df['rolling_mean']) / df['rolling_std']
    df['anomaly'] = df['z_score'].abs() > 2
    return df
