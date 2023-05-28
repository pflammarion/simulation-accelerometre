
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filenames = ["30", "50", "80"]

plt.figure().clear()
plt.close()
plt.cla()
plt.clf()

def filter_data(filename):

    df = pd.read_csv(filename, delimiter=';')
    if (filename == "./data/bruit.csv") :
        df["time"] = df["time"].str.replace(',', '.').astype(float)

    df["gFy"] = df["gFy"].str.replace(',', '.').astype(float)
    y = df["gFy"]
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time']
    y = y - y[0]

    return x, y


def calculate_instantaneous_velocity(acceleration, time_interval):
    return (acceleration[:-1] * np.diff(time_interval)).cumsum()

def calculate_noise(x, y, time):
    index = np.where(x > time)[0][0]
    return (y[index]/time) * x[:-1]

def filter_velocity(velocity_noise, noise):
    if len(velocity_noise) < len(noise):
        return velocity_noise - noise[:len(velocity_noise)]
    else:
        noise_extended = np.repeat(noise.iloc[-1], len(velocity_noise))
        noise_extended = noise_extended[:len(velocity_noise)]
        return velocity_noise - noise_extended


# to remove the constant noise
x, y = filter_data("./data/bruit.csv")
noise = calculate_instantaneous_velocity(y, x)

for filename in filenames:
    x, y = filter_data(f"./data/{filename}.csv")
    y = y * 9.81
    velocity_noise = calculate_instantaneous_velocity(y, x)

    velocity = filter_velocity(velocity_noise, noise)


    fig, ax = plt.subplots()
    ax2 = ax.twinx()


    ax2.plot(x[:-1], y[:-1], 'green', markersize=1, zorder=0)
    ax2.set_ylabel('Acceleration en G')

    ax.plot(x[:-1], velocity_noise * 3.6, 'bo', label='Vitesse avec bruit (en m/s)', markersize=2, zorder=10)
    ax.plot(x[:-1], velocity * 3.6, 'ro', label='Vitesse sans bruit (en m/s)', markersize=2, zorder=5)
    ax.set_ylabel('Vitesse (en km/h)')

    plt.title("Profil de l'accélération et de la vitesse d'une voiture de 0 à " + filename + " km/h")
    ax.set_xlabel('Temps (s)')

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left')

    plt.grid(True)
    plt.show()
