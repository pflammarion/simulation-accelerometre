
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filenames = ["30", "50", "80", "bruit"]
colname = "gFy"

plt.figure().clear()
plt.close()
plt.cla()
plt.clf()


def filter_data(filename):
    if filename != "./data/bruit.csv" :
        df = pd.read_csv(filename, delimiter=';')
        df[colname] = df[colname].str.replace(',', '.').astype(float)
    else :
        df = pd.read_csv(filename, delimiter=',')
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time']
    y = df[colname]
    y = y - y[0]
    return x, y


def calculate_instantaneous_velocity(acceleration, time_interval):
    return (acceleration[:-1] * np.diff(time_interval)).cumsum()


def calculate_distance(velocity, time_interval):
    distance = [0]
    for i in range(1, len(velocity)):
        delta_t = time_interval[i] - time_interval[i - 1]
        delta_d = 0.5 * (velocity[i] + velocity[i - 1]) * delta_t
        d = distance[i - 1] + delta_d
        distance.append(d)
    return distance

plt.clf()

for filename in filenames:
    x, y = filter_data(f"./data/{filename}.csv")
    y = y * 9.81
    velocity = calculate_instantaneous_velocity(y, x)

    ax = plt.gca()
    ax2 = ax.twinx()


    ax.plot(x[:-1], y[:-1], 'ro', label='Acceleration (en m/s^2)', markersize=2)
    ax.set_ylabel('Acceleration (en m/s^2)')
    ax2.plot(x[:-1], velocity * 3.6, 'bo', label='Vitesse (en m/s)', markersize=2)
    ax2.set_ylabel('Vitesse (en km/h)')
    ax.grid()

    plt.title("Profil de l'accélération et de la vitesse d'une voiture de 0 à " + filename + " km/h")
    ax.set_xlabel('Temps (s)')

    plt.legend()
    plt.show()
