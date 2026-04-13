import pandas as pd
from typing import Tuple

try:
    from prophet import Prophet
except ImportError:
    Prophet = None
import statsmodels.api as sm


def forecast_demand(df: pd.DataFrame, column: str = 'demand', periods: int = 30, freq: str = 'D') -> Tuple[pd.DataFrame, object]:
    """
    Forecast future demand using Prophet if available, otherwise fallback to an ARIMA model.
    Parameters:
        df (pd.DataFrame): Time-indexed DataFrame containing the target column.
        column (str): Name of the demand column in df.
        periods (int): Number of future periods to forecast.
        freq (str): Frequency string (e.g., 'D' for daily).
    Returns:
        Tuple[pd.DataFrame, object]: Forecast dataframe and fitted model object.
    """
    # Make a copy and drop missing values
    df = df.copy()
    df = df.dropna(subset=[column])

    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        if 'date' in df.columns:
            df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)

    # Sort by index
    df = df.sort_index()

    # Use Prophet when available
    if Prophet is not None:
        # Prepare DataFrame for Prophet
        prophet_df = df[[column]].reset_index().rename(columns={'index': 'ds', column: 'y'})
        model = Prophet()
        model.fit(prophet_df)
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], model

    # Fallback to SARIMAX/ARIMA model using statsmodels
    model = sm.tsa.statespace.SARIMAX(
        df[column],
        order=(1, 1, 1),
        seasonal_order=(0, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    result = model.fit(disp=False)

    # Generate forecast
    forecast_result = result.get_forecast(steps=periods)
    idx = pd.date_range(df.index[-1], periods=periods + 1, freq=freq)[1:]
    conf_int = forecast_result.conf_int()

    forecast_df = pd.DataFrame({
        'ds': idx,
        'yhat': forecast_result.predicted_mean,
        'yhat_lower': conf_int.iloc[:, 0],
        'yhat_upper': conf_int.iloc[:, 1]
    })
    return forecast_df, result
