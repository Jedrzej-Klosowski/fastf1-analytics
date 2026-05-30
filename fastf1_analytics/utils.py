import pandas as pd

def format_DataFrame(df) -> pd.DataFrame:
    if df.empty:
        raise ValueError("No data available for the specified drivers.")
    df = df[['Driver', 'LapNumber', 'LapTime', 'IsAccurate', 'LapTimeInSeconds']].copy()
    df['LapTime'] = format_time(df)
    return df

def format_time(df: pd.DataFrame) -> pd.Series:
    lap_time = pd.to_timedelta(df['LapTime'], errors='coerce')
    minutes = lap_time.dt.components['minutes'].fillna(0).astype(int)
    seconds = lap_time.dt.components['seconds'].fillna(0).astype(int)
    total_seconds = lap_time.dt.total_seconds().fillna(0)
    milliseconds = ((total_seconds % 1) * 1000).round(0).astype(int)

    formatted = (
        minutes.astype(str)
        + ':' +
        seconds.astype(str).str.zfill(2)
        + '.' +
        milliseconds.astype(str).str.zfill(3)
    )
    formatted = formatted.where(lap_time.notna(), pd.NA)
    return formatted