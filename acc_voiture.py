
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filenames = ["30", "45", "80"]
index = 0

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

def calculate_instanctaneous_position(velocity, time_interval):
    return (velocity * np.diff(time_interval)).cumsum()

def calculate_noise(x, y, time):
    index = np.where(x > time)[0][0]
    return (y[index]/time) * x[:-1]

def filter_velocity(velocity_noise, noise):
    if len(velocity_noise) < len(noise):
        velocity_temp = velocity_noise - noise[:len(velocity_noise)]
    else:
        noise_extended = np.repeat(noise.iloc[-1], len(velocity_noise))
        noise_extended = noise_extended[:len(velocity_noise)]
        velocity_temp = velocity_noise - noise_extended
    return velocity_temp + abs(np.amin(velocity_temp))


x, y = filter_data("./data/bruit.csv")
noise = calculate_instantaneous_velocity(y, x)

for filename in filenames:
    x, y = filter_data(f"./data/{filename}.csv")
    y = y * 9.81
    velocity_noise = calculate_instantaneous_velocity(y, x)

    velocity = filter_velocity(velocity_noise, noise)

    position = calculate_instanctaneous_position(velocity, x)


    fig, ax = plt.subplots()

    ax.plot(x[:-1], velocity * 3.6, 'bo', label='Vitesse sans bruit (en m/s)', markersize=2, zorder=5)
    ax.set_ylabel('Vitesse (en km/h)')

    plt.title("Profil de la vitesse d'une voiture de 0 à " + filename + " km/h à partir de l'accélération")
    ax.set_xlabel('Temps (s)')

    delta_velocity = (velocity_noise.iloc[-1] - velocity.iloc[-1]) / velocity.iloc[-1] * 100

    delta_velocity_car = int(filename) - (np.amax(velocity) * 3.6)

    delta_velocity_car_pourcentage = delta_velocity_car / int(filename) * 100

    print("L'erreur entre la vitesse réelle et la vitesse affiché de la voiture et de " + str(round(delta_velocity_car, 2)) + " km/h par rapport à " + filename +"km/h , soit " + str(round(delta_velocity_car_pourcentage, 2)) + " %")

    time_to_max = x.iloc[np.argmax(velocity)] - x.iloc[np.argmin(velocity)]
    trajet_length = position.iloc[np.argmax(velocity)] - position.iloc[np.argmin(velocity)]

    print("La voiture a atteint sa vitesse maximale en " + str(round(time_to_max, 2)) + " secondes et " + str(round(trajet_length, 2)) + " m")

    print(" ")

    if index == 0:
        # pour 30
        seuil_acceleration_haut = 5
        seuil_acceleration_bas = 4
        index += 1
    elif index == 1:
        # pour 50
        seuil_acceleration_haut = 3.5
        seuil_acceleration_bas = 1
        index += 1
    else :
        # pour 80
        seuil_acceleration_haut = 3.8
        seuil_acceleration_bas = -2.2

    passage = []
    depas = False
    last_index = 0

    for i in range(1, len(y)):
        if y[i] > seuil_acceleration_haut:
            depas = True
            last_index = i
        elif y[i] < seuil_acceleration_bas and depas and x[i] - x[last_index] < 1:
            passage.append(i)
            depas = False

    for passage_index in passage:
        ax.vlines(x[passage_index], np.min(velocity_noise * 3.6), np.max(velocity_noise * 3.6), colors='purple', linestyles='dashed', label='Passage de vitesse')

    ax.hlines(int(filename), x[0], x[len(x) - 1], colors='red', linestyles='dashed', label='Vitesse compteur')

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left')
    plt.grid(True)
    plt.show()