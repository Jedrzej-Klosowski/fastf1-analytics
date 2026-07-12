import sys
import logging
import fastf1.plotting
from fastf1_analytics.data import setup_cache, get_session, add_LapTimeInSeconds, is_accurate
from fastf1_analytics.utils import format_DataFrame
from fastf1_analytics.io import get_drivers_from_input
from fastf1_analytics.plotting import plot_driver_comparsion, get_driver_colors
def main():
    logging.disable(logging.CRITICAL)
    setup_cache()
    fastf1.plotting.setup_mpl(
        mpl_timedelta_support=True,
        color_scheme="fastf1"
    )
    session = get_session(2021, "Abu Dhabi", 5)
    drivers_abbrs = get_drivers_from_input()
    df = is_accurate(session.laps, drivers_abbrs)
    df = add_LapTimeInSeconds(df)
    try:
        print(format_DataFrame(df))
    except ValueError as e:
        print(e)
        sys.exit(0)
    driver_colors = get_driver_colors(drivers_abbrs, session)
    plot_driver_comparsion(df, driver_colors)

if __name__ == "__main__":
    main()