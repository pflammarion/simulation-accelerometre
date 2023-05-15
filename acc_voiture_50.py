from statistics import mean

import matplotlib.pyplot as plt
import pandas as pd

g = 9.81
point_equilibre_acceleration = 0.2
point_equilibre_deceleration = 0.2

acceleration_seuil_max = 0.6
acceleration_seuil_min = -0.05

filename = "80.csv"
colname = "gFy"

def filter_data(filename):
    df = pd.read_csv(filename, delimiter=';')
    df[colname] = df[colname].str.replace(',', '.').astype(float)
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time'].tolist()
    y = df[colname].tolist()
    return x, y

def calculate_acceleration(x, y):

    min_index = y.index(min(y))
    max_index = y.index(max(y))


    for i in range(max_index, -1, -1):
        if y[i] < point_equilibre_acceleration:
            debut_acc = 400
            break

    for i in range(max_index+1, len(y)):
        if y[i] < point_equilibre_acceleration - 0.2:
            fin_acc = 1600
            break

    for i in range(min_index, -1, -1):
        if y[i] > point_equilibre_deceleration - 0.2:
            debut_dece = 1601
            break

    for i in range(min_index+1, len(y)):
        if y[i] > point_equilibre_deceleration:
            fin_dece = 2374
            break


    return debut_acc, fin_acc, debut_dece, fin_dece

x, y = filter_data(filename)

plt.plot(x, y, 'ro')
plt.title('Profil de l''accélération lors de la descente de l\'idir ')
plt.xlabel('Temps (s)')
plt.ylabel('Accélération (en m/s^-2)')
plt.show()

debut_acc, fin_acc, debut_dece, fin_dece = calculate_acceleration(x, y)

print(debut_acc, fin_acc, debut_dece, fin_dece)

mean_acc = (mean(y[debut_acc:fin_acc]) * g)-g
mean_dece = (mean(y[debut_dece:fin_dece]) * g)-g

delta_acc = x[debut_acc] - x[fin_acc]
delta_dece = x[debut_dece] - x[fin_dece]

print("L'acceletration est positive de {:.2f} s à {:.2f} s avec une accelération moyenne de {:.2f} m/s^2".format(x[debut_acc], x[fin_acc], mean_acc))
print("L'acceletration est negative de {:.2f} s à {:.2f} s avec une deceleration moyenne de {:.2f} m/s^2".format(x[debut_dece], x[fin_dece], mean_dece))

print("")

vitesse_acc = mean_acc * delta_acc
distance_acc = abs(mean_acc * delta_acc**2)

vitesse_dece = mean_dece * delta_dece
distance_dece = abs(mean_dece * delta_dece**2)

print("On en déduit une acceleration pendant {:.2f} m à une vitesse de {:.2f} m/s".format(distance_acc, abs(vitesse_acc)))
print("On en déduit une deceleration pendant {:.2f} m à une vitesse de {:.2f} m/s".format(abs(distance_dece), vitesse_dece))

print("")


distance_tot = distance_acc + abs(distance_dece)
temps_tot = x[fin_dece] - x[debut_acc]

print("Ce qui fait un total de {:.2f} m en {:.2f} s".format(distance_tot, temps_tot))