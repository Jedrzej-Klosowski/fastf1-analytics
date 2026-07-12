import fastf1.plotting
import matplotlib.pyplot as plt
def plot_driver_comparsion(df, driver_colors) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    drivers = df['Driver'].unique()
    for driver in drivers:
        driver_data = df[df['Driver'] == driver]
        ax.plot(driver_data['LapNumber'], 
                driver_data['LapTimeInSeconds'], 
                label=f"Driver {driver}",
                marker='o',
                color=driver_colors.get(driver))
    ax.set_title('Lap time comparasion')
    ax.set_xlabel('Lap number')
    ax.set_ylabel('Lap time [in seconds]')
    ax.legend()
    plt.savefig('LineChart.png')
    plt.show()

def get_driver_colors(drivers_abbrs, session) -> list:
    driver_colors = {}
    for driver in drivers_abbrs:
        color = fastf1.plotting.get_driver_color(
            driver,
            session,
            colormap="official",
            exact_match=False
        )
        driver_colors[driver] = color
    return driver_colors