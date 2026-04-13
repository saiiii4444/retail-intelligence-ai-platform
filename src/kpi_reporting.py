import pandas as pd


def generate_kpis(df, demand_col='demand', anomaly_col='anomaly', inventory_col='inventory', period='W'):
    """
    Generate high-level business KPIs from retail analytics data.

    Parameters:
        df (pd.DataFrame): DataFrame with demand, anomaly flag, and inventory.
        demand_col (str): Column containing demand values.
        anomaly_col (str): Column containing anomaly flags (boolean/int).
        inventory_col (str): Column containing inventory level values.
        period (str): Resampling period for time-based KPIs (e.g., 'W' for weekly).

    Returns:
        dict: Dictionary of KPI names and values.
    """
    # Ensure DataFrame has datetime index for resampling
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError('DataFrame index must be a DatetimeIndex for KPI resampling')

    kpis = {}

    # Total demand and average weekly demand
    total_demand = df[demand_col].sum()
    weekly_demand = df[demand_col].resample(period).sum().mean()
    kpis['total_demand'] = total_demand
    kpis['average_weekly_demand'] = weekly_demand

    # Anomaly rate
    anomaly_rate = df[anomaly_col].mean()
    kpis['anomaly_rate'] = anomaly_rate

    # Average inventory level
    avg_inventory = df[inventory_col].mean()
    kpis['average_inventory_level'] = avg_inventory

    # Stockout events (inventory below demand)
    stockouts = (df[inventory_col] <= df[demand_col]).sum()
    kpis['stockout_events'] = stockouts

    return kpis
