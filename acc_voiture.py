from statistics import mean

import matplotlib.pyplot as plt
import pandas as pd

filenames = ["30", "50", "80"]
colname = "gFy"

plt.figure().clear()
plt.close()
plt.cla()
plt.clf()


def filter_data(filename):
    df = pd.read_csv(filename, delimiter=';')
    df[colname] = df[colname].str.replace(',', '.').astype(float)
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time'].tolist()
    y = df[colname].tolist()
    y = [acc - y[0] for acc in y]
    return x, y


def calculate_instantaneous_velocity(acceleration, time_interval, initial_velocity):
    velocity = [initial_velocity]
    velocity.insert(0, 0)
    for i in range(1, len(acceleration) - 1):
        delta_t = time_interval[i + 1] - time_interval[i]
        delta_v = 0.5 * (acceleration[i + 1] + acceleration[i]) * delta_t
        v = velocity[i - 1] + delta_v
        velocity.append(v)
    return velocity


def calculate_distance(velocity, time_interval):
    distance = [0]
    for i in range(1, len(velocity)):
        delta_t = time_interval[i] - time_interval[i - 1]
        delta_d = 0.5 * (velocity[i] + velocity[i - 1]) * delta_t
        d = distance[i - 1] + delta_d
        distance.append(d)
    return distance


for filename in filenames:
    x, y = filter_data("./data/" + filename + ".csv")
    velocity = calculate_instantaneous_velocity(y, x, 0)

    plt.plot(x, y, 'ro', label='Acceleration (en m/s^2)', markersize=2)
    plt.plot(x, velocity, 'bo', label='Vitesse (en m/s)', markersize=2)

    plt.title("Profil de l'accélération et de la vitesse d'une voiture de 0 à " + filename + " km/h")
    plt.xlabel('Temps (s)')

    plt.legend()
    plt.show()
