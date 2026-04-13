import pandas as pd


def calculate_inventory_risk(df, demand_col='demand', inventory_col='inventory', lead_time=7):
    """
    Calculates risk score for stockouts given forecasted demand and inventory levels.

    Parameters:
        df (pd.DataFrame): DataFrame containing demand and inventory columns.
        demand_col (str): Name of the demand column.
        inventory_col (str): Name of the inventory level column.
        lead_time (int): Number of periods to look ahead for projected demand.

    Returns:
        pd.DataFrame: DataFrame with projected demand and risk scores.
    """
    df = df.copy()
    # Project future demand over the lead_time horizon
    df['projected_demand'] = df[demand_col].rolling(window=lead_time).sum().shift(-lead_time+1)
    # Calculate risk score as the fraction of projected demand not covered by inventory
    df['risk_score'] = (df['projected_demand'] - df[inventory_col]) / df['projected_demand']
    # Replace negative scores with 0 (no risk) and handle division by zero
    df['risk_score'] = df['risk_score'].fillna(0).clip(lower=0, upper=1)
    return df[[inventory_col, 'projected_demand', 'risk_score']]
