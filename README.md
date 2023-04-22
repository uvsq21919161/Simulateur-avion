# Simulateur-avion
Projet effectué dans le cadre de mes études.  

Simulation du fonctionnement du système de carburant simplifié d'un avion de chasse. Ce simulateur a pour but d'entraîner les pilotes à gérer le système carburant en cas de crise.    

L'objectif de ce projet est de pratiquer la programmation orientée objet.

Projet réaliser en binome avec Mohamed Amine.
---
# Exécution du code
Pour exécuter le code, placez-vous d'abord dans le chemin correspondant dans le terminal, puis exécutez la commabde.
```
make
```

---
## Le système carburant
Le système de carburant est composé de 3 réservoirs indépendants : Tank1, Tank2, Tank3.  
Avec un fonctionnement normal du système, chaque réservoir alimente son moteur: Tank1 alimente le moteur M1, Tank2 alimente le moteur M2 et Tank3 alimente le moteur M3.   
Il faut noter que les réservoirs Tank1 et Tank3 ont une plus grande capacité que le réservoir Tank2.  

Le carburant est acheminé aux moteurs à l'aide d'un système de pompes. Pour chaque réservoir il existe 2 pompes, une pompe primaire et une pompe de secours. Dans le fonctionnement normal, les pompes de secours sont arrêtées.
![image](https://user-images.githubusercontent.com/72187742/233805763-da285366-c5d1-4217-94f2-dc545a07a0eb.png)

---
## Le tableau de bord du pilote
La partie du tableau de bord du pilote permettant de gérer le système carburant de l'avion. Le pilote peut réaliser les actions suivantes:
- Ouvrir ou fermer les vannes VT12 et VT23 (boutons VT12 et VT23 Figure 2);
- Ouvrir ou fermer les vannes V12, V13, V23 (boutons V12, V13 et V23 Figure 2);
- Démarrer ou arrêter les pompes de secours (boutons P12, P22 et P32 Figure 2).
![image](https://user-images.githubusercontent.com/72187742/233805787-af833f93-f811-4837-b3f8-8309c411f02e.png)

---
## Les pannes
Nous pouvons considérer le cas d'un réservoir qui se vide ou le cas d'une pompe qui tombe en panne. Pour remédier à ses pannes deux systèmes de reconfigurations sont prévus:
1. Les trois réservoirs sont reliés par des tuyaux pour équilibrer le niveau de carburant dans chaque réservoir. Si les vannes VT12 et VT23 sont fermées, le carburant peut circuler d'un réservoir à l'autre. Si l'un des réservoirs se vide, le pilote peut fermer les vannes VT12 et/ou VT23 pour remplir le réservoir vide avec le carburant provenant des autres réservoirs.
2. Chaque pompe peut alimenter n'importe lequel des trois moteurs. Chaque moteur a besoin d'une seule pompe pour être alimenté. Si l'une des pompes tombe en panne, le pilote peut démarrer la pompe secondaire. Si les 2 pompes sont en pannes, il est possible d'acheminer le carburant au moteur depuis un autre réservoir. Il suffit que le pilote démarre la pompe secondaire et ferme la vanne correspondante (V13, V12 ou V23).
