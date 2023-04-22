# Simulateur-avion
Projet effectué dans le cadre de mes études.  

Simulation du fonctionnement du système de carburant simplifié d'un avion de chasse. Ce simulateur a pour but d'entraîner les pilotes à gérer le système carburant en cas de crise.    

L'objectif de ce projet est de pratiquer la programmation orientée objet.

---
# Exécution du code
Pour exécuter la commande, placez-vous d'abord dans le chemin correspondant dans le terminal, puis exécutez-la.
```
make
```

---
## Le système carburant
Le système de carburant est composé de 3 réservoirs indépendants : Tank1, Tank2, Tank3.  
Avec un fonctionnement normal du système, chaque réservoir alimente son moteur: Tank1 alimente le moteur M1, Tank2 alimente le moteur M2 et Tank3 alimente le moteur M3.   
Il faut noter que les réservoirs Tank1 et Tank3 ont une plus grande capacité que le réservoir Tank2.  

Le carburant est acheminé aux moteurs à l'aide d'un système de pompes. Pour chaque réservoir il existe 2 pompes, une pompe primaire et une pompe de secours. Dans le fonctionnement normal, les pompes de secours sont arrêtées.
  
---
## Le tableau de bord du pilote
La partie du tableau de bord du pilote permettant de gérer le système carburant de l'avion. Le pilote peut réaliser les actions suivantes:
- Ouvrir ou fermer les vannes VT12 et VT23 (boutons VT12 et VT23 Figure 2);
- Ouvrir ou fermer les vannes V12, V13, V23 (boutons V12, V13 et V23 Figure 2);
- Démarrer ou arrêter les pompes de secours (boutons P12, P22 et P32 Figure 2).

