Ce présent dossier contient les deux simulations du G5E pour l'Etat de l’Art à propos des Accéléromètres Industriels (MEMS et autres)

## Simulation 1

_Construction d'un dispositif pour mesurer l'accélération linéaire à l'aide d'un accéléromètre._ Pour cette simulation, nous avons utilisé un accéléromètre MEMS. Dans le cas de l'utilisation de ce capteur nous avons utilisé l'application "Physics Toolbox Suite" qui enregistre en temps réel les données de l'accéléromètre implémenté dans un smartphone.
    
_Montée dans un ascenseur et effectuer des mesures d'accélération linéaire à différents moments de la montée ou de la descente._ Pour cette étape, nous sommes montés dans un ascenseur et avons effectué des mesures d'accélération linéaire lors de la montée ou de la descente de celui-ci. Nous avons enregistré les données en utilisant un smartphone.
    
_Analyse des données pour déterminer la vitesse de l'ascenseur au cours du temps._ Pour cette étape, nous allons utiliser un logiciel de traitement de données (MATLAB ainsi que Python) pour analyser les données et déterminer la vitesse de l'ascenseur au cours du temps. Nous allons tracer un graphique de l'accélération en fonction du temps pour visualiser les résultats qui en découlent.


Nous avons utilisé l’application "Physics Toolbox Suite" pour enregistrer les varia-
tion de l’accélération de la pesanteur à la surface de la Terre en fonction du temps lors
de la montée d’un ascenseur sur 3 étages. Nous avons dans un premier temps analysé
ce tableau pour en déduire les données qui nous intéressaient.

![img.png](img/donneeasc.png)


Comme nous pouvons le remarquer dans ce tableau, la première colonne nous permet de définir l’instant où la mesure a été prise. Les autres colonnes sont respectivement
l’accélération en x, en y, en z et la somme de ces forces. Dans le cadre de cette expérience nous souhaitons analyser les variations de l’accélération par rapport à l’axe z. La
somme totale des forces ne serait pas intéressante car l’ascenseur ayant une trajectoire
purement verticale, cela ne ferait qu’ajouter du bruit à nos valeurs.

Nous n’allons donc garder que le temps et la mesure de l’accélération en z que nous
allons afficher sur un graphique pour une meilleure visualisation du jeu de données.


Dans un premier temps, nous avons fait notre simulation sur le logiciel MATLAB.
Une fois le jeu de données chargé, nous obtenons le graphique suivant :

![img.png](img/graphasc.png)

Sur ce graphique, nous remarquons par analyse graphique une augmentation
de l’accélération de 2,5 secondes à 5 seconde, une stabilisation pendant 5 secondes, et
une décélération durant 2,5 secondes. Nous allons donc diviser notre programme en
3 parties distinctes : la phase d’accélération, la phase de vitesse constante, et la phase
de décélération. Pour que notre algorithme soit juste, nous avons défini une vitesse de
départ et d’arrivée à 0 m/s. Nous en déduisons le graphique suivant :

![img.png](img/analyseasc.png)


Nous avons fait une moyenne de l’accélération que nous avons préalablement multipliée par l’accélération de la pesanteur standard que nous avons notée "g", pour
convertir nos valeurs en accélération. Nous avons pris pour nos analyses une valeur de g
de 9, 81 m/s^2.

Une fois ces moyennes calculées, nous pouvons en déduire la vitesse maximale atteinte à la suite de l’accélération qui est donnée par :

![img.png](img/calc1.png)

Nous pouvons ensuite en déduire la distance parcourue par l’ascenseur en calculant
la distance parcourue lors de l’accélération, lors de la phase durant laquelle la vitesse
est constante, et durant la décélération. Nous restons dans le cas où la vitesse à l’origine
est 0 m/s.

![img.png](img/calc2.png)

Nous obtenons après ces calculs les résultats suivant lors de l’analyse de la montée
d’un ascenseur sur 3 étages :

```

L'accélération est positive de 2.57 s à 4.62 s avec une accélération moyenne de 0.47 m/s^2
L'accélération est negative de 10.04 s à 12.00 s avec une deceleration moyenne de -0.49 m/s^2

On en déduit une accélération pendant 1.96 m à une vitesse de 0.95 m/s
On en déduit une deceleration pendant 1.89 m à une vitesse de 0.96 m/s

La distance parcourue entre l'accélération et la décélération est calculée par x(t)=v1*t+x0
Elle est de 5.17 m

Ce qui fait un total de 9.02 m en 9.43 s

```

Une fois ce programme réalisé et cohérent avec l’expérience, nous avons décidé de
l’implémenter aussi en Python. Nous obtenons les mêmes résultats

#### Nous obtenons ce graphique :

![img.png](img/screen_asc.png)


Pour conclure cette simulation, nous pouvons dire que l’accéléromètre utilisé semble
avoir une bonne précision car nous sommes dans le bon ordre de grandeur. Cette simulation met en évidence les variations de l’accélération subie par les passagers, ce
programme pourrait aussi permettre de détecter des anomalies telles que des accélérations trop brusques, des secousses ou des vibrations. De plus, nous remarquons qu’un
ascenseur n’a pas d’accélération linéaire jusqu’à sa décélération et son arrêt, mais une
vitesse limite (0,96 m/s) atteinte en 2,5 secondes.


Il aurait été intéressant de comparer les différents profils d’ascenseur, sur un nombre
différent d’étages. De plus, nous aurions aussi pu analyser le profil d’accélération d’un
ascenseur lors de sa descente pour en tirer des conclusions quant au fonctionnement de
celui-ci.


## Simulation 2

_Fixation d’un accéléromètre à l’intérieur d’une voiture et utilisation pour mesurer
l’accélération linéaire de la voiture._ Pour cette simulation, vous avons fixé un
accéléromètre à l’intérieur d’une voiture pour que celui-ci ne bouge plus par
rapport au référentiel de la voiture. Nous avons ensuite effectué des mesures
d’accélération linéaire en conduisant la voiture dans différentes conditions de
conduite.

Nous avons effectué des mesures d’accélération linéaire jusqu'à différentes vitesses (ici, 30 km/h, 45 km/h, 80 km/h).

Nous avons ensuite analysé les données pour déterminer la vitesse de la voiture au cours du temps.
Pour cette étape, nous avons utilisé un programme python pour analyser les données et déterminer la vitesse de la voiture au cours
du temps. Nous allons tracer un graphique de la vitesse en fonction du temps
pour visualiser les résultats et les comparer à l'accélération.

#### Nous obtenons ces graphiques :

![img.png](img/screen_30.png)

Nous pouvons observer une augmentation linéaire de la vitesse avec un plat lors d'un passage de vitesse de la boite mécanique de la voiture.
La voiture atteint la vitesse de 30km/h à 4 seconde après le début de l'enregistrement.

![img_1.png](img/screen_45.png)

Comme lors de l'accélération de 0 à 30 km/h, nous avons une augmentation linéaire de la vitesse.
Avec un passage de vitesse entre 2 et 3 secondes et la vitesse de 50 km/h atteinte à partir de 5 secondes


![img_2.png](img/screen_80.png)



Cette courbe est moins facile à analyser. En effet, on remarque une décélération à partir de 11 secondes où la vitesse de 80 km/h est atteinte, les frottements induisent ce début de chute de vitesse.
Nous voyons aussi un passage de vitesse à 8 seconde.


```
L'erreur entre la vitesse réelle et la vitesse affiché de la voiture et de 2.27 km/h par rapport à 30km/h , soit 7.57 %
La voiture a atteint sa vitesse maximale en 3.37 secondes et 11.83 m
 
L'erreur entre la vitesse réelle et la vitesse affiché de la voiture et de 4.51 km/h par rapport à 45km/h , soit 10.02 %
La voiture a atteint sa vitesse maximale en 7.15 secondes et 43.35 m
 
L'erreur entre la vitesse réelle et la vitesse affiché de la voiture et de 6.33 km/h par rapport à 80km/h , soit 7.91 %
La voiture a atteint sa vitesse maximale en 9.43 secondes et 102.32 m

```

#### Analyse

Grâce aux données d'accélération mesurée, nous avons réussi à déterminer une vitesse et une distance.
Elle nous permet de pouvoir analyser des changements d'environnement qui affectent directement la vitesse.
Grâce aux données d'accélération mesurée, nous avons réussi à en déterminer une vitesse et une distance correspondante. L'on remarque également qu'avec les trois mesures (pour la voiture) les passages de vitesses se font au même moment, tout comme les décélérations due aux changements de vitesses.
Ces mesures et variations nous permettent de déduire les changements d'environnements de l'objet en mouvement (ascenseur ou voiture). L'usage d'accéléromètre est massivement utilisé dans quasi toutes les études de mouvements d'objets, par exemple les navettes spatiales.

Cependant notre précision n'est bien évidemment pas parfaite. Nos mesures ont été faites avec un capteur piézoélectriques ou piézorésistifs (grandement présent dans les smartphones), et possèdent une grande sensibilité aux interférences électromagnétiques et aux variations, ainsi les résultats sont soumis à un taux d'erreur plus ou moins grand lié aux conditions d'enregistrement. Mais, au vue de nos résultats, l'erreur (si elle existe) est très petite.
Nous pouvons donc penser à des utilisations pour prédire ou prévenir de problèmes potentiels dus aux accélérations comprenant les chutes, les collisions, du stress sur les organes internes et l'inconfort pour les passagers. Des accélérations excessives peuvent également causer des dommages aux objets et mettre en danger la sécurité des personnes. Il est donc essentiel de respecter les normes de sécurité d’accélération pour prévenir ces risques.
