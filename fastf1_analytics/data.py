import os
import fastf1
import pandas as pd

def setup_cache(cache_dir='../fastf1_cache'):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

def get_session(year=2021, gp="Abu Dhabi", session_num=5):
    session = fastf1.get_session(year, gp, session_num)
    session.load()
    return session

def add_LapTimeInSeconds(df: pd.DataFrame) -> pd.DataFrame:
    lap_time = pd.to_timedelta(df['LapTime'], errors='coerce')
    df = df.copy()
    df.loc[:, 'LapTimeInSeconds'] = lap_time.dt.total_seconds()
    return df

def is_accurate(laps, drivers_abbrs):
    if hasattr(laps, 'pick_quicklaps'):
        laps = laps.pick_quicklaps()
    laps = laps[laps['IsAccurate'] == True]
    laps = laps[laps['Driver'].isin(drivers_abbrs)]
    return laps.copy()