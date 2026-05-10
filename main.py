import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
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

df = session.laps[session.laps['Driver'].isin(drivers_abbrs)].copy()

def format_DataFrame(df) -> pd.DataFrame:
    if df.empty:
        print("No data available for the specified drivers.")
        sys.exit(0)
    df = df[['Driver', 'LapNumber', 'LapTime', 'IsAccurate', 'LapTimeInSeconds']].copy()
    df['LapTime'] = format_time(df)
    return df

def format_time(df: pd.DataFrame) -> pd.Series:
    lap_time = pd.to_timedelta(df['LapTime'], errors='coerce')
    minutes = lap_time.dt.components['minutes'].fillna(0).astype(int)
    seconds = lap_time.dt.components['seconds'].fillna(0).astype(int)
    total_seconds = lap_time.dt.total_seconds()
    milliseconds = ((total_seconds % 1) * 1000).round(0).astype(int)

    formatted = (
        minutes.astype(str)
        + ':' +
        seconds.astype(str).str.zfill(2)
        + '.' +
        milliseconds.astype(str).str.zfill(3)
    )
    return formatted.where(lap_time.notna(), pd.NA)

def add_LapTimeInSeconds(df: pd.DataFrame) -> pd.DataFrame:
    lap_time = pd.to_timedelta(df['LapTime'], errors='coerce')
    total_seconds = lap_time.dt.total_seconds()
    df = df.copy()
    df.loc[:, 'LapTimeInSeconds'] = total_seconds
    return df

def plot_driver_comparasion(df: pd.DataFrame) -> None:
    
    fig, ax = plt.subplots(figsize=(10, 6))
    drivers = df['Driver'].unique()

    for driver in drivers:
        driver_data = df[df['Driver'] == driver]

        ax.plot(driver_data['LapNumber'], 
                driver_data['LapTimeInSeconds'], 
                label=f"Driver {driver}",
                marker='o')

    ax.set_title('Lap time comparasion')
    ax.set_xlabel('Lap number')
    ax.set_ylabel('Lap time [in seconds]')
    ax.legend()
    plt.savefig('LineChart.png')
    plt.show()
    
    
df= df[df['IsAccurate'] == True].pick_quicklaps()
df = add_LapTimeInSeconds(df)
print(format_DataFrame(df))
plot_driver_comparasion(df)