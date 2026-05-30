import sys
import logging
from fastf1_analytics.data import setup_cache, get_session, add_LapTimeInSeconds, is_accurate
from fastf1_analytics.utils import format_DataFrame
from fastf1_analytics.io import get_drivers_from_input
from fastf1_analytics.plotting import plot_driver_comparsion

def main():
    logging.disable(logging.CRITICAL)
    setup_cache()
    session = get_session(2021, "Abu Dhabi", 5)
    drivers_abbrs = get_drivers_from_input()
    df = is_accurate(session.laps, drivers_abbrs)
    df = add_LapTimeInSeconds(df)
    try:
        print(format_DataFrame(df))
    except ValueError as e:
        print(e)
        sys.exit(0)
    plot_driver_comparsion(df)

if __name__ == "__main__":
    main()