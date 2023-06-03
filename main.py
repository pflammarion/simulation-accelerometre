import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

x, y = None, None
noise = None
velocity_noise = None
velocity = None
position = None
fig = None
ax = None
canvas = None
analysis_text_widget = None
g = 9.81

def filter_data_car(filename):
    df = pd.read_csv(filename, delimiter=';')
    if filename == "./data/bruit.csv":
        df["time"] = df["time"].str.replace(',', '.').astype(float)

    df["gFy"] = df["gFy"].str.replace(',', '.').astype(float)
    y = df["gFy"]
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time']
    y = y - y[0]

    return x, y

def filter_data_elevator(filename):
    df = pd.read_csv(filename, delimiter=';')
    df['gFz'] = df['gFz'].str.replace(',', '.').astype(float)
    df = df.drop_duplicates(subset='time', keep='last')
    x = df['time']
    y = df['gFz']
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

def display_analysis_car(speed):
    global fig, ax, canvas, analysis_text_widget

    x, y = filter_data_car("./data/bruit.csv")
    noise = calculate_instantaneous_velocity(y, x)

    filename = f"./data/{speed}.csv"
    x, y = filter_data_car(filename)

    y = y * g
    velocity_noise = calculate_instantaneous_velocity(y, x)
    velocity = filter_velocity(velocity_noise, noise)
    position = calculate_instanctaneous_position(velocity, x)

    if fig is None:
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=3)

    ax.clear()
    ax.plot(x[:-1], velocity * 3.6, 'bo', label='Vitesse sans bruit (en m/s)', markersize=2, zorder=5)
    ax.set_ylabel('Vitesse (en km/h)')
    ax.set_xlabel('Temps (s)')
    ax.set_title(f"Profil de la vitesse d'une voiture de 0 à {speed} km/h à partir de l'accélération")

    if speed == "30":
        seuil_acceleration_haut = 5
        seuil_acceleration_bas = 4
    elif speed == "45":
        seuil_acceleration_haut = 3.5
        seuil_acceleration_bas = 1
    else :
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

    colors = ['purple', 'orange']
    for passage_index in passage:
        color_index = passage.index(passage_index) % len(colors)
        color = colors[color_index]
        label_text = "passage de vitesse " + str(passage.index(passage_index) + 1)
        ax.vlines(x[passage_index], np.min(velocity_noise * 3.6), np.max(velocity_noise * 3.6), colors=color, linestyles='dashed', label=label_text)

    ax.hlines(int(speed), x[0], x[len(x) - 1], colors='red', linestyles='dashed', label='Vitesse compteur')

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left', bbox_to_anchor=(0, 0.95))
    ax.grid(True)


    delta_velocity_car = int(speed) - (np.amax(velocity) * 3.6)
    delta_velocity_car_pourcentage = delta_velocity_car / int(speed) * 100

    time_to_max = x.iloc[np.argmax(velocity)] - x.iloc[np.argmin(velocity)]
    trajet_length = position.iloc[np.argmax(velocity)] - position.iloc[np.argmin(velocity)]

    analysis_text = f"L'erreur entre la vitesse réelle et la vitesse affichée de la voiture est de {round(delta_velocity_car, 2)} km/h par rapport à {speed} km/h, soit {round(delta_velocity_car_pourcentage, 2)}%\n\n"
    analysis_text += f"La voiture a atteint sa vitesse maximale en {round(time_to_max, 2)} secondes et {round(trajet_length, 2)} m"

    if analysis_text_widget is None:
        analysis_text_widget = tk.Text(root, height=6, width=90)
        analysis_text_widget.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    analysis_text_widget.delete("1.0", tk.END)
    analysis_text_widget.insert(tk.END, analysis_text)

    canvas.draw()

def display_analysis_elevator():
    global fig, ax, canvas, analysis_text_widget

    filename = f"./data/montee.csv"
    x, y = filter_data_elevator(filename)

    debut_acc, fin_acc, debut_dece, fin_dece = calculate_acceleration_elevator(x, y)

    if fig is None:
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=3)

    ax.clear()
    ax.plot(x, y, 'bo', label="Force en g", markersize=2)
    ax.set_ylabel('G Force')
    ax.set_xlabel('Temps (s)')
    ax.set_title("Profil de l'accélération lors de la montée de l'ascenseur sur 3 étages")

    mean_acc = (np.mean(y[debut_acc:fin_acc]) * g) - g
    mean_dece = (np.mean(y[debut_dece:fin_dece]) * g) - g

    delta_acc = x[debut_acc] - x[fin_acc]
    delta_dece = x[debut_dece] - x[fin_dece]

    vitesse_acc = mean_acc * delta_acc
    distance_acc = mean_acc * delta_acc ** 2

    vitesse_dece = mean_dece * delta_dece
    distance_dece = mean_dece * delta_dece ** 2

    distance_parcourue = vitesse_acc * (x[fin_acc] - x[debut_dece])

    distance_tot = distance_acc + distance_parcourue + np.abs(distance_dece)

    temps_tot = x[fin_dece] - x[debut_acc]

    ax.vlines(x[debut_acc], np.min(y), np.max(y), colors='purple', linestyles='dashed', label='Début de la montée')
    ax.vlines(x[fin_dece], np.min(y), np.max(y), colors='red', linestyles='dashed', label='Fin de la montée')

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.65, 0.95))
    ax.grid(True)

    analysis_text = f"L'ascenseur parcourt {round(distance_tot, 2)} mètres en {round(temps_tot, 2)} secondes.\nSon accélération et sa décélération sont équivalentes, car la vitesse est nulle au départ comme à l'arrivée.\nElles sont de {round(mean_acc,2)} m/s^2, soit une vitesse atteinte de {round(vitesse_dece,2)} m/s."

    if analysis_text_widget is None:
        analysis_text_widget = tk.Text(root, height=6, width=90)
        analysis_text_widget.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    analysis_text_widget.delete("1.0", tk.END)
    analysis_text_widget.insert(tk.END, analysis_text)

    canvas.draw()


def calculate_acceleration_elevator(x, y):
    min_index = np.argmin(y)
    max_index = np.argmax(y)

    point_equilibre_acceleration = 1
    point_equilibre_deceleration = 1

    for i in range(max_index, -1, -1):
        if y[i] < point_equilibre_acceleration:
            debut_acc = i
            break

    for i in range(max_index+1, len(y)):
        if y[i] < point_equilibre_acceleration:
            fin_acc = i
            break

    for i in range(min_index, -1, -1):
        if y[i] > point_equilibre_deceleration:
            debut_dece = i
            break

    for i in range(min_index+1, len(y)):
        if y[i] > point_equilibre_deceleration:
            fin_dece = i
            break



    return debut_acc, fin_acc, debut_dece, fin_dece


def button_click(file):
    display_analysis_car(file)

def simulation_ascenseur():
    display_analysis_elevator()
    button_30.grid_remove()
    button_45.grid_remove()
    button_80.grid_remove()



def simulation_voiture():
    button_30.grid(row=1, column=0, padx=10, pady=10)
    button_45.grid(row=1, column=1, padx=10, pady=10)
    button_80.grid(row=1, column=2, padx=10, pady=10)

    if canvas is not None:
        ax.clear()
        canvas.draw()

    if analysis_text_widget is not None:
       analysis_text_widget.delete("1.0", tk.END)


root = tk.Tk()
root.title("Simulations accélérometre")
root.geometry("800x850")

button_choice_1 = tk.Button(root, text="Simulation ascenseur", command=lambda: simulation_ascenseur())
button_choice_1.grid(row=0, column=0, padx=10, pady=10)

button_choice_2 = tk.Button(root, text="Simulation voiture", command=lambda: simulation_voiture())
button_choice_2.grid(row=0, column=1, padx=10, pady=10)

button_30 = tk.Button(root, text="30 km/h", command=lambda: button_click("30"))

button_45 = tk.Button(root, text="45 km/h", command=lambda: button_click("45"))

button_80 = tk.Button(root, text="80 km/h", command=lambda: button_click("80"))

root.mainloop()
