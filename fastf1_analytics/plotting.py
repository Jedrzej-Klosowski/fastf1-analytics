import matplotlib.pyplot as plt

def plot_driver_comparsion(df) -> None:
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