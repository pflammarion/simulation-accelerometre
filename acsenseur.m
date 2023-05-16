%%  G5E_Accelerometre.m

%-------------------------
%
% Groupe G5E
%
% Analyse de l'accélération d'un ascenseur lors de sa déscente
%
%-------------------------


clc;
close all;
clear variables;


% A déterminer graphiquement


point_equilibre_acceleration = 1;
point_equilibre_deceleration = 1;

acceleration_seuil_max = 1.1;
acceleration_seuil_min = -0.88;



%% Configuration et importation des données
opts = delimitedTextImportOptions("NumVariables", 5);

% Configuration de la longueur et du délimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ";";

% Configuration des noms et types de colonnes
opts.VariableNames = ["time", "Var2", "Var3", "azms2", "Var5"];
opts.SelectedVariableNames = ["time", "azms2"];
opts.VariableTypes = ["double", "string", "string", "double", "string"];

% Configuration des propriétés du fichier
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Configuration des propriétées des variables
opts = setvaropts(opts, ["Var2", "Var3", "Var5"], "WhitespaceRule", "preserve");
opts = setvaropts(opts, ["Var2", "Var3", "Var5"], "EmptyFieldRule", "auto");
opts = setvaropts(opts, ["time", "azms2"], "DecimalSeparator", ",");
opts = setvaropts(opts, ["time", "azms2"], "ThousandsSeparator", ".");

% Importation de la donnée
data = readtable("descente.csv", opts);

%% Convertion en type de sortie
data = table2array(data);

%% Clear temporaire des variables
clear opts

time = data(:,1);
accel = data(:,2);

%% Plot de l'acceleration en fonction du temps
figure(1);
plot(time, accel, Color='r');
hold on;

%% Recherche du min et du max
[min_peaks, min_locs] = findpeaks(-accel, 'MinPeakHeight', acceleration_seuil_min);
[max_peaks, max_locs] = findpeaks(accel, 'MinPeakHeight', acceleration_seuil_max);

%% Plot des points de début et de fin


% Inversion du signal pour trouver le point de départ
accel_reversed = accel(end:-1:1);
max_locs_reversed = length(accel) - max_locs;
start_point_reversed_acc = find(accel_reversed(max_locs_reversed:end) < point_equilibre_acceleration, 1);

min_locs_reversed = length(accel) - min_locs;
start_point_reversed_dece = find(accel_reversed(min_locs_reversed:end) > point_equilibre_deceleration, 1);



% Inversion de l'indice pour obtenir le point de départ dans le signal original
debut_acc = length(accel) - (start_point_reversed_acc + max_locs_reversed);
fin_acc = find(accel(max_locs:end) < point_equilibre_acceleration, 1) + max_locs;

debut_dece = length(accel) - (start_point_reversed_dece + min_locs_reversed);
fin_dece = find(accel(min_locs:end) > point_equilibre_deceleration, 1) + min_locs;


plot(time(debut_acc), accel(debut_acc), 'bo', 'MarkerSize', 10, 'LineWidth', 1.4, 'Color', 'g');
plot(time(fin_dece), accel(fin_dece), 'bo', 'MarkerSize', 10, 'LineWidth', 1.4, 'Color', 'b');


%% Plot final

grid on;
xlabel('Temps (s)');
ylabel('Accélération (m/s^2)');
title('Profil de l''accélération lors de la descente de l''ascenseur');
legend('Accélération', 'Début de la descente', 'Fin de la descente');

g = 9.81;
mean_acc = (mean(accel(debut_acc:fin_acc)) * g)-g;
mean_dece = (mean(accel(debut_dece:fin_dece)) * g)-g;

delta_acc = time(debut_acc) - time(fin_acc);
delta_dece = time(debut_dece) - time(fin_dece);

disp("L'acceletration est positive de " + time(debut_acc) + " s à " + time(fin_acc) + " s avec une accelération moyenne de " + mean_acc + " m/s^2")
disp("L'acceletration est negative de " + time(debut_dece) + " s à " + time(fin_dece) + " s avec une deceleration moyenne de " + mean_dece + " m/s^2")

disp(" ")

vitesse_acc = mean_acc * delta_acc;
distance_acc = mean_acc * delta_acc^2;

vitesse_dece = mean_dece * delta_dece;
distance_dece = mean_dece * delta_dece^2;

disp("On en déduit une acceleration pendant " + distance_acc + " m" + " à une vitesse de " + abs(vitesse_acc) + " m/s")
disp("On en déduit une deceleration pendant " + abs(distance_dece) + " m" + " à une vitesse de " + vitesse_dece + " m/s")

disp(" ");

disp("La distance parcouru enttre l'acceleration et la décélération est calculée par x(t)=v1*t+x0")
distance_parcourue = vitesse_acc * (time(fin_acc)-time(debut_dece));
disp("Elle est de " + distance_parcourue + " m")

disp(" ");

distance_tot = distance_acc + distance_parcourue + abs(distance_dece);
temps_tot = time(fin_dece) - time(debut_acc);

disp("Ce qui fait un total de " + distance_tot + " m en " + temps_tot +  " s");

