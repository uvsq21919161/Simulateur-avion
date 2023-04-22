#!usr/bin/python3
#coding: utf-8 

class Vanne(object):
    def __init__(self, nom, etat = "fermee"):
        self.nom = nom
        self.etat = etat
    
    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom,str):
            raise TypeError("Le nom de la vanne doit être une chaîne de caractères.")
        self._nom = nom

    @property
    def etat(self):
        return self._etat

    @etat.setter
    def etat(self, etat):
        if etat not in ("fermee","ouvert"):
            raise SyntaxError("La vanne ne peut être que dans l'état <ouvert> ou <fermee>.")
        if not isinstance(etat,str):
            raise TypeError("L'état de la vanne doit être une chaîne de caractères.")
        self._etat = etat

    def __str__(self):
        return "Vanne({},{})".format(self.nom, self.etat)

    def new_etat(self):
        if self.etat == "ouvert":
            self.etat = "fermee"
        elif self.etat == "fermee":
            self.etat = "ouvert"

class Pompe(object):
    def __init__(self, nom, etat = "marche"):
        self.nom = nom
        self.etat = etat

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom,str):
            raise TypeError("Le nom de la pompe doit être une chaîne de caractères.")
        self._nom = nom

    @property
    def etat(self):
        return self._etat

    @etat.setter
    def etat(self, etat):
        if etat not in ("arret","marche","panne"):
            raise SyntaxError("La pompe ne peut être que dans les états <arret>, <marche> ou <panne>.")
        if not isinstance(etat,str):
            raise TypeError("L'état de la pompe doit être une chaîne de caractères.")
        self._etat = etat

    def __str__(self):
        return "Pompe({},{})".format(self.nom, self.etat)

    def new_etat(self):
        if self.etat == "marche":
            self.etat = "arret"
        elif self.etat == "arret":
            self.etat = "marche"

    def new_panne(self):
        if self.etat == "marche":
            self.etat = "panne"
        elif self.etat == "arret":
            self.etat = "panne"
        elif self.etat == "panne":
            self.etat = "marche"

class Reservoir(object):
    def __init__(self, nom, etat = "plein", pompe = None, pompe_secours = None):
        self.nom = nom
        self.etat = etat
        self.pompe, self.pompe_secours = pompe, pompe_secours

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom,str):
            raise TypeError("Le nom du réservoir doit être une chaîne de caractères.")
        self._nom = nom

    @property
    def etat(self):
        return self._etat

    @etat.setter
    def etat(self, etat):
        if etat not in ("plein","vide"):
            raise SyntaxError("Le réservoir ne peut être que dans les états <plein> ou <vide>.")
        if not isinstance(etat,str):
            raise TypeError("L'état du réservoir doit être une chaîne de caractères.")
        self._etat = etat

    @property
    def pompe(self):
        return self._pompe

    @pompe.setter
    def pompe(self, pompe):
        if not isinstance(pompe,Pompe):
            raise SyntaxError("Le champ pompe du réservoir ne prend que des instances de Pompe")
        self._pompe = pompe

    @property
    def pompe_secours(self):
        return self._pompe_secours

    @pompe_secours.setter
    def pompe_secours(self, pompe_secours):
        if not isinstance(pompe_secours,Pompe):
            raise SyntaxError("Le champ pompe du réservoir ne prend que des instances de Pompe")
        self._pompe_secours = pompe_secours

    def __str__(self):
        return "Reservoir({},{})({},{})".format(self.nom, self.etat, self.pompe, self.pompe_secours)

    def new_panne(self):
        if self.etat == "plein":
            self.etat = "vide"
        elif self.etat == "vide":
            self.etat = "plein"

class Moteur(object):
    def __init__(self, nom, source = None):
        self.nom = nom
        self.source = source

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom,str):
            raise TypeError("Le nom du moteur doit être une chaîne de caractères.")
        self._nom = nom

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if not isinstance(source, Reservoir):
            raise SyntaxError("La source du moteur doit être un reservoir.")
        self._source = source

    def __str__(self):
        return "Moteur({},{})".format(self.nom,self.source.nom)

class Avion(object):
    def __init__(self):
        self.vannesReservoirs = [Vanne("vt12"), Vanne("vt23")]
        self.vannes = [Vanne("v12"), Vanne("v13"), Vanne("v23")]
        self.pompes = [Pompe("p11"), Pompe("p12","arret"), Pompe("p21"), Pompe("p22","arret"),Pompe("p31"), Pompe("p32","arret")]
        pompe_iter = iter(self.pompes)
        self.reservoirs = [
            Reservoir("Tank1","plein",next(pompe_iter),next(pompe_iter)), 
            Reservoir("Tank2","plein",next(pompe_iter),next(pompe_iter)), 
            Reservoir("Tank3","plein",next(pompe_iter),next(pompe_iter))]
        reservoir_iter = iter(self.reservoirs)
        self.moteurs = [Moteur("M1",next(reservoir_iter)), Moteur("M2",next(reservoir_iter)), Moteur("M3",next(reservoir_iter))]

    def verif_panne(self):
        value = False
        check_panne = ("vide","panne")
        for element in self.reservoirs + self.pompes:
            if element.etat in check_panne:
                value = True
        return value

    def affiche_avion(self):
        for element in self.reservoirs + self.vannes + self.vannesReservoirs:
            print(element)

    def panne(self, nom_element):
        value = False
        for element in self.reservoirs + self.pompes:
            if element.nom == nom_element:
                if isinstance(element,Pompe): element.etat, value = "panne", True
                if isinstance(element,Reservoir): element.etat, value = "vide", True
        return value

    def alea_pannes(self):
        import random
        noms_pompes = [element._nom for element in self.pompes]
        noms_tanks = [element._nom for element in self.reservoirs]
        if random.random() < 0.50:
            self.panne(random.choice(noms_pompes))
        else:
            self.panne(random.choices(noms_tanks,weights=[5,1,5],k=1)[0])

    def resolve_panne(self):
        return self.__solve_carburant() and self.__solve_pompe()

    def nbr_pannes_pompes(self):
        index = 0
        for element in self.pompes:
            if element.etat == "panne":
                index += 1
        return index

    def nbr_pannes_tanks(self):
        index = 0
        for element in self.reservoirs:
            if element.etat == "vide":
                index += 1
        return index

    def __solve_carburant(self):
        # true si solved false if pb
        index_composants = {"p11":0, "p12":1, "p21":2, "p22":3, "p31":4, "p32":5, "vt12":0, "vt23":1,"Tank1":0, "Tank2":1, "Tank3":2,"M1":0, "M2":1, "M3":2, "v12":0, "v13":1, "v23":2}
        if self.reservoirs[index_composants["Tank1"]].etat == 'plein' and self.reservoirs[index_composants["Tank2"]].etat == 'vide' and self.reservoirs[index_composants["Tank3"]].etat == 'vide':
            if self.vannesReservoirs[index_composants["vt12"]].etat == 'ouvert' and self.vannesReservoirs[index_composants["vt23"]].etat == 'ouvert':
                return True
            return False
        elif self.reservoirs[index_composants["Tank1"]].etat == 'vide' and self.reservoirs[index_composants["Tank2"]].etat == 'vide' and self.reservoirs[index_composants["Tank3"]].etat == 'vide':
            return False
        elif self.reservoirs[index_composants["Tank1"]].etat == 'vide' and self.reservoirs[index_composants["Tank2"]].etat == 'plein' and self.reservoirs[index_composants["Tank3"]].etat == 'vide':
            if self.vannesReservoirs[index_composants["vt12"]].etat == 'ouvert' and self.vannesReservoirs[index_composants["vt23"]].etat == 'ouvert':
                return True
            return False   
        elif self.reservoirs[index_composants["Tank1"]].etat == 'plein' and self.reservoirs[index_composants["Tank2"]].etat == 'plein' and self.reservoirs[index_composants["Tank3"]].etat == 'vide':
            if self.vannesReservoirs[index_composants["vt23"]].etat == 'ouvert':
                return True
            return False    
        elif self.reservoirs[index_composants["Tank1"]].etat == 'vide' and self.reservoirs[index_composants["Tank2"]].etat == 'vide' and self.reservoirs[index_composants["Tank3"]].etat == 'plein':
            if self.vannesReservoirs[index_composants["vt12"]].etat == 'ouvert' and self.vannesReservoirs[index_composants["vt23"]].etat == 'ouvert':
                return True
            return False   
        elif self.reservoirs[index_composants["Tank1"]].etat == 'plein' and self.reservoirs[index_composants["Tank2"]].etat == 'vide' and self.reservoirs[index_composants["Tank3"]].etat == 'plein':
            if self.vannesReservoirs[index_composants["vt12"]].etat == 'ouvert' or self.vannesReservoirs[index_composants["vt23"]].etat == 'ouvert':
                return True
            return False 
        elif self.reservoirs[index_composants["Tank1"]].etat == 'vide' and self.reservoirs[index_composants["Tank2"]].etat == 'plein' and self.reservoirs[index_composants["Tank3"]].etat == 'plein':
            if self.vannesReservoirs[index_composants["vt12"]].etat == 'ouvert':
                return True
            return False
        elif self.reservoirs[index_composants["Tank1"]].etat == 'plein' and self.reservoirs[index_composants["Tank2"]].etat == 'plein' and self.reservoirs[index_composants["Tank3"]].etat == 'plein':
            return True
        return False
        
    def __solve_pompe(self):
        index_composants = {"p11":0, "p12":1, "p21":2, "p22":3, "p31":4, "p32":5, "vt12":0, "vt23":1,"Tank1":0, "Tank2":1, "Tank3":2,"M1":0, "M2":1, "M3":2, "v12":0, "v13":1, "v23":2}
        if self.pompes[index_composants["p11"]].etat == 'panne':
            if self.pompes[index_composants["p12"]].etat == 'marche':
                return True
            elif self.pompes[index_composants["p22"]].etat == 'marche' and self.vannes[index_composants["v12"]].etat == 'ouvert':
                return True
            elif self.pompes[index_composants["p32"]].etat == 'marche' and self.vannes[index_composants["v13"]].etat == 'ouvert':
                return True
            return False

        if self.pompes[index_composants["p12"]].etat == 'panne':
            if self.pompes[index_composants["p11"]].etat == 'marche':
                return True
            if self.pompes[index_composants["p22"]].etat == 'marche' and self.vannes[index_composants["v12"]].etat == 'ouvert':
                return True
            if self.pompes[index_composants["p32"]].etat == 'marche' and self.vannes[index_composants["v13"]].etat == 'ouvert':
                return True
            return False
    
        if self.pompes[index_composants["p21"]].etat == 'panne':
            if self.pompes[index_composants["p22"]].etat == 'marche':
                return True
            if self.pompes[index_composants["p12"]].etat == 'marche' and self.vannes[index_composants["v12"]].etat == 'ouvert':
                return True
            if self.pompes[index_composants["p32"]].etat == 'marche' and self.vannes[index_composants["v23"]].etat == 'ouvert':
                return True
            return False
    
        if self.pompes[index_composants["p22"]].etat == 'panne':
            if self.pompes[index_composants["p21"]].etat == "marche":
                return True
            if self.pompes[index_composants["p12"]].etat == 'marche' and self.vannes[index_composants["v12"]].etat == 'ouvert':
                return True
            if self.pompes[index_composants["p32"]].etat == 'marche' and self.vannes[index_composants["v23"]].etat == 'ouvert':
                return True
            return False
    
        if self.pompes[index_composants["p31"]].etat == 'panne':
            if self.pompes[index_composants["p32"]].etat == 'marche':
                return True
            if self.pompes[index_composants["p22"]].etat == 'marche' and self.vannes[index_composants["v23"]].etat == 'ouvert':
                return True
            if self.pompes[index_composants["p12"]].etat == 'marche' and self.vannes[index_composants["v13"]].etat == 'ouvert':
                return True
            return False
    
        if self.pompes[index_composants["p32"]].etat == 'panne':
            if self.pompes[index_composants["p31"]].etat == 'marche':
                return True
            if self.pompes[index_composants["p22"]].etat == 'marche' and self.vannes[index_composants["v23"]].etat == 'ouvert':
                return True
            if self.pompes[index_composants["p12"]].etat == 'marche' and self.vannes[index_composants["v13"]].etat == 'ouvert':
                return True
            return False
        return True
