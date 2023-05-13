import matplotlib.pyplot as plt
import pandas as pd

GRAVITY = 9.81

def filter_data(filename):
    df = pd.read_csv(filename, delimiter=';')
    df['gFz'] = df['gFz'].str.replace(',', '.').astype(float)
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time'].tolist()
    y = df['gFz'].tolist()
    return x, y

def calculate_acceleration(x, y):
    nb_valeur_acceleration = 0
    nb_valeur_deceleration = 0
    acceleration = 0
    deceleration = 0
    # déterminé graphiquement mais pourrait être fait par le programme
    ta1 = 2.5   # Temps de début d'accélération
    ta2 = 5   # Temps de fin d'accélération
    td1 = 10   # Temps de début de décélération
    td2 = 12.5   # Temps de fin de décélération
    for i in range(len(x)):
        t = x[i]
        v = y[i]
        if ta1 < t < ta2:
            acceleration += v
            nb_valeur_acceleration += 1
        if td1 < t < td2:
            deceleration += v
            nb_valeur_deceleration += 1
    if nb_valeur_acceleration > 0:
        acceleration = (acceleration * GRAVITY / nb_valeur_acceleration) - GRAVITY
    if nb_valeur_deceleration > 0:
        deceleration = (deceleration * GRAVITY / nb_valeur_deceleration) - GRAVITY
    return acceleration, deceleration

x, y = filter_data("./montée.csv")

plt.plot(x, y, 'ro')
plt.title('Vitesse d\'un ascenseur en fonction du temps')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.show()

acceleration, deceleration = calculate_acceleration(x, y)

print('Acceleration:', round(acceleration, 2), 'm/s^2')
print('Deceleration:', round(deceleration, 2), 'm/s^2')

