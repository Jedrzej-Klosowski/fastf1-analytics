import fastf1
import pandas as pd
import os
import logging

cache_dir = './fastf1_cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

fastf1.Cache.enable_cache(cache_dir)

#logging.disable(logging.WARNING)
logging.disable(logging.CRITICAL)

session = fastf1.get_session(2021, "Abu Dhabi", 5)
session.load()

drivers_abbrs = []
while True:
    abbr = input("Enter the abbreviations of F1 drivers' surnames [-1 to exit]: ").strip()
    if abbr == "-1":
        break
    drivers_abbrs.append(abbr.upper())

df = session.laps[session.laps['Driver'].isin(drivers_abbrs)]

def format_time(df: pd.DataFrame) -> pd.Series:
    lap_time = pd.to_timedelta(df['LapTime'], errors='coerce')
    components = lap_time.dt.components
    minutes = components['minutes'].fillna(0).astype(int)
    seconds = components['seconds'].fillna(0).astype(int)
    milliseconds = (components['microseconds'].fillna(0) // 1000).astype(int)

    formatted = (
        minutes.astype(int).astype(str)
        + ':'
        + seconds.astype(int).astype(str).str.zfill(2)
        + '.'
        + milliseconds.astype(int).astype(str).str.zfill(3)
    )
    return formatted.where(lap_time.notna(), pd.NA)

def format_DataFrame(df) -> pd.DataFrame:
    if df.empty:
        print("No data available for the specified drivers.")
        return df
    df = df.drop(columns = ['Time', 'FastF1Generated', 'IsAccurate', 'Deleted', 'DeletedReason',
                            'Stint','PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time',
                            'Sector1SessionTime', 'Sector2SessionTime', 'Sector3SessionTime',
                            'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'IsPersonalBest',
                            'FreshTyre', 'Team', 'LapStartTime', 'DriverNumber',
                            'LapStartDate', 'TrackStatus', 'Position',
                            'FastF1Generated', 'IsAccurate'])
    df['LapTime'] = format_time(df)
    return df

print(df.columns)
print(format_DataFrame(df))