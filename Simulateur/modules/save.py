#!usr/bin/python3
#coding: utf-8

import os
from composants import Avion

def save(chemin, avion, user, password):
    f = open(chemin,'w')
    lines = []
    for element in avion.reservoirs: lines.append("Reservoir {} {} ".format(element.nom, element.etat)),
    for element in avion.vannes: lines.append("Vanne {} {} ".format(element.nom, element.etat))
    for element in avion.vannesReservoirs: lines.append("VanneReservoir {} {} ".format(element.nom, element.etat))
    for element in avion.moteurs: lines.append("Moteur {} {} ".format(element.nom,element.source.nom))
    for element in avion.pompes: lines.append("Pompe {} {} ".format(element.nom, element.etat))
    print(lines)
    print("\n\n")
    f.writelines('\n'.join(lines))
    f.close()

def load(user, password):
    chemin = './Simulateur/save/' + user + "_" + password + ".txt"
    avion = Avion()
    index_values = {"p11":0,"p12":1,"p21":2,"p22":3,"p31":4,"p32":5,"v12":0,"v23":1,"v13":2,"vt12":0,"vt23":1,"Tank1":0,"Tank2":1,"Tank3":2,"M1":0,"M2":1,"M3":2}
    # fichier corrompu a gerer
    if not os.path.exists(chemin):
        raise SyntaxError("Impossible de charger la partie.")

    f = open(chemin,'r')
    for line in f.readlines():
        string = line.split(" ")
        instance_type, instance_nom = string[0], string[1]
        index = index_values[instance_nom]
        if instance_type == "Moteur": avion.moteurs[index].source = avion.reservoirs[index_values[string[2]]]
        if instance_type == "Vanne": avion.vannes[index].etat = string[2]
        if instance_type == "VanneReservoir": avion.vannesReservoirs[index].etat = string[2]
        if instance_type == "Reservoir": avion.reservoirs[index].etat = string[2]
        if instance_type == "Pompe": avion.pompes[index].etat = string[2]
    f.close()
    return avion
