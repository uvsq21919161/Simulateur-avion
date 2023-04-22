#!usr/bin/python3
#coding: utf-8

from datetime import datetime
from os import makedirs
from os.path import isfile,isdir
from tkinter import CENTER, END, LEFT, NW, RIGHT, Entry, StringVar, Tk, Button, PhotoImage, Canvas
from save import save, load
from composants import Avion

source_path = "./Simulateur"
image_path = source_path + "/images"
modules_path = source_path + "/modules"
data_path = source_path + "/data"
save_path = source_path + "/save"
score_path = source_path + "/score"

score = 0
tours = 0


def update(avion,thisCanva):
    elements_panne = [element for element in avion.reservoirs + avion.pompes + avion.vannes + avion.vannesReservoirs]
    for item in elements_panne:
        if item.etat in ("ouvert","marche","fermee","arret","panne","vide","plein"): thisCanva.refresh(item.nom,item.etat)
    for i in range(3):
        thisCanva.canvas.create_rectangle(115+i*200, 80, 195+i*200, 120)

def change_etat(element,avion,canva,panneaucanva):
    global score, tours
    if element is not None:
        element.new_etat()
    update(avion,canva)
    if avion.verif_panne() == True:
        tours += 1
        # save here dans file
        if avion.resolve_panne():
            score += 1
        if avion.nbr_pannes_tanks() == 3 or avion.nbr_pannes_pompes() > 3:
            canva.canvas.destroy()
            panneaucanva.destroy()
            can = Canvas(root, bg='black',highlightthickness=0,height = 620, width = 1280)
            can.pack()
            fond = PhotoImage(file= image_path + "/fond.png")
            can.create_image(0,0,image=fond,anchor=NW)
            can.image = fond
            scorefinal = (int(score)*10)/int(tours)
            can.create_text(640, 310, text=f"Félicitation, votre score {scorefinal}/10",fil="white",font=('Arial 15 bold'))
            chemin = f'./Simulateur/score/{user}_{passw}.txt'
            date = datetime.today().strftime('%d/%m')
            if isdir(chemin) is False:
                with open(chemin,'w') as f:
                    f.write(f'{scorefinal},{date}')
            else:
                with open(chemin,'a') as f:
                    f.write(f'{scorefinal},{date}')
            Button(can,bg='black',fg='white',bd=5,text="Exit",padx=10, pady=10,command= lambda: root.destroy()).place(x=640 ,y=340)

    avion.alea_pannes()

def change_etat2(element,avion,canva):
    if element is not None:
        element.new_etat()
    update(avion,canva)


def change_panne(element,avion,canva):
    if element is not None:
        element.new_panne()
    update(avion,canva)
    
    
class Panneau(object):
    def __init__(self,root,avion,sys):
        self.root = root
        self.canvas = Canvas(self.root, width=600, height=620, bg='black')
        self.canvas.pack(side = LEFT)
        self.structure = avion
        self.sys = sys

    def creer_boutons(self):
        self.canvas.create_text(300, 130, text="Boutons pour ouvrir/fermer les vannes",fil="white",font=('Arial 15 bold'))
        self.canvas.create_text(300, 160, text="et démarrer/arrêter les pompes :",fil="white",font=('Arial 15 bold'))
        # 1
        Button(self.canvas,bg='black',fg='white',bd=5,text="vt12",padx=7, pady=10,command= lambda: change_etat(self.structure.vannesReservoirs[0], self.structure, self.sys,self.canvas)).place(x=201, y=205)
        Button(self.canvas,bg='black',fg='white',bd=5,text="vt23",padx=7, pady=10, command= lambda: change_etat(self.structure.vannesReservoirs[1], self.structure, self.sys,self.canvas)).place(x=308, y=205)
        # 2
        Button(self.canvas,bg='black',fg='white',bd=5,text="p12",padx=10, pady=10, command= lambda: change_etat(self.structure.pompes[1], self.structure, self.sys,self.canvas)).place(x=144, y=300)
        Button(self.canvas,bg='black',fg='white',bd=5,text="p22",padx=10, pady=10, command= lambda: change_etat(self.structure.pompes[3], self.structure, self.sys,self.canvas)).place(x=254, y=300)
        Button(self.canvas,bg='black',fg='white',bd=5,text="p32",padx=10, pady=10, command= lambda: change_etat(self.structure.pompes[5], self.structure, self.sys)).place(x=364, y=300)
        # 3
        Button(self.canvas,bg='black',fg='white',bd=5,text="v12",padx=10, pady=10,command= lambda: change_etat(self.structure.vannes[0], self.structure, self.sys,self.canvas)).place(x=144 ,y=395)
        Button(self.canvas,bg='black',fg='white',bd=5,text="v13",padx=10, pady=10, command= lambda: change_etat(self.structure.vannes[1], self.structure, self.sys,self.canvas)).place(x=254, y=395)
        Button(self.canvas,bg='black',fg='white',bd=5,text="v23",padx=10, pady=10,command= lambda: change_etat(self.structure.vannes[2], self.structure, self.sys,self.canvas)).place(x=364, y=395)
        Button(self.canvas,bg='black',fg='white',bd=5,text="pass",padx=10, pady=10, command= lambda: change_etat(None, self.structure, self.sys,self.canvas)).place(x=254, y=480)
    
        global user,passw
        self.save_button = Button(self.canvas, text= "save", bd=5, bg="black",fg='white',command= lambda: self.save(self.structure,user,passw))
        self.save_button.place(x=10,y= 10)

    def creer_boutons2(self):
        self.canvas.create_text(300, 25, text="Ouvrir/fermer les vannes",fil="white",font=('Helvetica 15 bold', 12))
        self.canvas.create_text(300, 40, text="et démarrer/arrêter les pompes :",fil="white",font=('Helvetica 15 bold', 12))
        # 1
        Button(self.canvas,bg='black',fg='white',bd=5,text="vt12",padx=7, pady=10,command= lambda: change_etat2(self.structure.vannesReservoirs[0], self.structure, self.sys)).place(x=201, y=55)
        Button(self.canvas,bg='black',fg='white',bd=5,text="vt23",padx=7, pady=10, command= lambda: change_etat2(self.structure.vannesReservoirs[1], self.structure, self.sys)).place(x=308, y=55)
        # 2
        Button(self.canvas,bg='black',fg='white',bd=5,text="p12",padx=10, pady=10, command= lambda: change_etat2(self.structure.pompes[1], self.structure, self.sys)).place(x=144, y=150)
        Button(self.canvas,bg='black',fg='white',bd=5,text="p22",padx=10, pady=10, command= lambda: change_etat2(self.structure.pompes[3], self.structure, self.sys)).place(x=254, y=150)
        Button(self.canvas,bg='black',fg='white',bd=5,text="p32",padx=10, pady=10, command= lambda: change_etat2(self.structure.pompes[5], self.structure, self.sys)).place(x=364, y=150)
        # 3
        Button(self.canvas,bg='black',fg='white',bd=5,text="v12",padx=10, pady=10,command= lambda: change_etat2(self.structure.vannes[0], self.structure, self.sys)).place(x=144 ,y=245)
        Button(self.canvas,bg='black',fg='white',bd=5,text="v13",padx=10, pady=10, command= lambda: change_etat2(self.structure.vannes[1], self.structure, self.sys)).place(x=254, y=245)
        Button(self.canvas,bg='black',fg='white',bd=5,text="v23",padx=10, pady=10,command= lambda: change_etat2(self.structure.vannes[2], self.structure, self.sys)).place(x=364, y=245)

        self.canvas.create_text(300, 330, text="Déclencher les pannes sur les pompes",fil="white",font=('Helvetica 15 bold', 12))
        self.canvas.create_text(300, 345, text="ou les vidanges des réservoirs :", fill="white", font=('Helvetica 15 bold', 12))

        Button(self.canvas, text="P11", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[0], self.structure, self.sys)).place(x=144, y=395)
        Button(self.canvas, text="P12", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[1], self.structure, self.sys)).place(x=254, y=395)
        Button(self.canvas, text="P21", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[2], self.structure, self.sys)).place(x=364, y=395)
        Button(self.canvas, text="P22", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[3], self.structure, self.sys)).place(x=144, y=440)
        Button(self.canvas, text="P31", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[4], self.structure, self.sys)).place(x=254, y=440)
        Button(self.canvas, text="P32", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.pompes[5], self.structure, self.sys)).place(x=364, y=440)

        Button(self.canvas, text="Tank1", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.reservoirs[0], self.structure, self.sys)).place(x=144, y=485)
        Button(self.canvas, text="Tank2", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.reservoirs[1], self.structure, self.sys)).place(x=254, y=485)
        Button(self.canvas, text="Tank3", width=5, bd=5, font=('courrier', 12), bg='black', fg='white', command= lambda: change_panne(self.structure.reservoirs[2], self.structure, self.sys)).place(x=364, y=485)

        self.pass_button = Button(self.canvas,bg='black',fg='white',bd=5,text="pass",padx=10, pady=10, command= lambda: change_etat2(None, self.structure, self.sys))
        self.pass_button.place(x=500, y=245)

    def save(self,avion,user,passw):
        self.save_button.destroy()
        save(save_path + "/" + user + "_" + passw + ".txt",avion,user,passw)

class Root(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Login")
        self.geometry("1280x620")
        self.iconphoto(False,PhotoImage(file=image_path + "/petrole.png"))
        self.resizable(width=False,height=False)
        self.config(bg='white')
        
class Menu(object):
    def __init__(self,root):
        self.root = root
        self.canvas = Canvas(self.root,bg='black',highlightthickness=0,height = 620, width = 1280)
        fond = PhotoImage(file= image_path + "/fond.png")
        self.canvas.pack()
        self.canvas.create_image(0,0,image=fond,anchor=NW)
        self.canvas.image = fond

    def creer_menu(self):
        Button(self.canvas,bd=7,text = "Simulation",bg='black',fg='white',command = lambda : self.newRun()).place(relx=0.5,y=255, anchor=CENTER)
        Button(self.canvas,bd=7,text = "Demo",bg='black',fg='white',command = lambda : self.demoRun()).place(relx=0.5,y=345, anchor=CENTER)

    def newRun(self):
        self.canvas.destroy()
        Run = Login(self.root)
        Run.login()
        
    def demoRun(self):
        self.canvas.destroy()
        # Initialisation avion et canva
        avion = Avion()
        sys = Illustration(self.root)
        sys.creer_formes()
        panneau = Panneau(self.root,avion,sys)    
        update(avion,sys)
        panneau.creer_boutons2()

class Login(object):
    def __init__(self,root):
        self.root = root
        fond = PhotoImage(file= image_path + "/fond.png")
        self.canvas= Canvas(self.root,bg='black',highlightthickness=0,height = 620, width = 1280)
        self.canvas.pack()
        self.canvas.create_image(0,0,image=fond,anchor=NW)
        self.canvas.image = fond
        self.avion_log = None
        
    def verifsifichier(self,chemin):
        # Vérifie si le fichier existe sinon le crée
        if not isinstance(chemin,str): raise TypeError("Le chemin n'est pas une chaîne de charactères.")
        if isdir(data_path) is False: makedirs(data_path)
        if isdir(save_path) is False: makedirs(save_path)
        if isdir(score_path) is False: makedirs(score_path)
        if isfile(chemin) is False:
            f = open(chemin,'w')
            f.close()

    def connect(self):
        global user, passw 
        user, passw = username.get(),password.get()
        self.verifsifichier(data_path + '/Log.txt')
        #Parcours le fichier où sont stocké tous les identifiants, et si un identifiants correspond, l'authentification est valider, sinon renvoi un message d'erreur.
        with open(data_path + '/Log.txt','r',encoding='utf8') as f:
            line,trouve = f.readline(), 0
            while line != '':
                line=line.split(':')
                characters = '\n'
                line[1] = ''.join(x for x in line[1] if x not in characters)
                if user == line[0] and passw == line[1]:
                    trouve = 1
                    break
                line = f.readline()
            if trouve == 1:
                self.canvas.delete('nom','mdp','info','faux'),b1.destroy(),b2.destroy(),username.destroy(),password.destroy()
                self.canvas.create_text(640,310,text = f'Bonjour, {user}.',fill ="White",font=('Arial',18))
                self.canvas.bind("<Button-1>",lambda e: self.suivant(user,passw))
                self.canvas.create_text(640,380,text = "Veuillez, cliquer sur l'écran.",fill ="White",font=('Arial',12))
            else:
                self.canvas.create_text(640,195,text = 'Les identifiants sont faux.',fill = "red", font=('Arial',13),tag='faux')
                username.delete(0,END),password.delete(0,END)

    # Interface de l'inscription
    def registration_interface(self):
        global b3
        self.verifsifichier(data_path + '/Log.txt')
        # Delete
        self.canvas.delete('info','faux'),b1.destroy(),b2.destroy(),username.delete(0,END),password.delete(0,END)
        # Buttom
        b3 = Button(self.root,text = "S'inscrire",bg='black',fg='white',command = lambda : self.registration())
        b3.place(relx=0.5,y=330, anchor=CENTER)

    def registration(self):
        global user, passw
        with open(data_path + '/Log.txt','a',encoding='utf8') as f:
            # Stock le username et le mot de passe données et vérifie s'il n'est pas vide.
            # si oui renvoi un message d'erreur
            user, passw = username.get(),password.get()
            if user == '' or passw == '':
                self.canvas.delete('alreadyuse')
                self.canvas.create_text(640,195, text = 'Veuillez remplir.',fill = "red", font=('Arial',13),tag='filled')
            #Sinon parcours le fichier où sont stocké tous les identifiants, et si un identifiants correspond, renvoi un message d'erreur, sinon crée un compte avec ses identifiants
            else:
                with open(data_path + '/Log.txt','r',encoding='utf8') as f:
                    line,trouve = f.readline(), 0
                    while line != '':
                        line=line.split(':')
                        characters = '\n'
                        line[1] = ''.join(x for x in line[1] if x not in characters)
                        if user in line[0] and passw in line[1]:
                            trouve = 1
                            break
                        line = f.readline()
                if trouve == 1 :
                    self.canvas.delete('filled')
                    self.canvas.create_text(640,195, text = 'Identifiants déjà utilisés.',fill = "red", font=('Arial',13),tag='alreadyuse')
                else:
                    with open(data_path + '/Log.txt','a',encoding='utf8') as f:
                        ecrire = f'{username.get()}:{password.get()}\n'
                        f.write(ecrire)
                    username.destroy(),
                    password.destroy(),
                    b3.destroy(),
                    self.canvas.delete('nom','mdp','filled','alreadyuse')
                    self.canvas.create_text(640,310,text = f'Bonjour, {user}.',fill ="White",font=('Arial',18))
                    self.canvas.bind("<Button-1>",lambda e: self.suivant(user,passw))

    def suivant(self,user,passw):
        self.canvas.destroy()
        file_syn = save_path + "/" + user + "_" + passw + ".txt"
        if not isfile(file_syn):
            self.avion_log = Avion()
            f = open(file_syn, "w")
            f.close()
            save(file_syn, self.avion_log, user, passw)
            self.avion_log.alea_pannes()
        else:
            self.avion_log = load(user, passw)
        sys = Illustration(self.root)
        sys.creer_formes()
        print(sys.canvas)
        panneau = Panneau(self.root,self.avion_log,sys)
        update(self.avion_log,sys)
        panneau.creer_boutons()
        Historique(sys.canvas,user,passw)

    def login(self):
        global username,password,b1,b2
        # StringVar
        username,password = StringVar(), StringVar()
        # Text
        self.canvas.create_text(640,220,text = "Entrer un nom.",fill = "white", font=('Arial',13),tag='nom')
        self.canvas.create_text(640,270, text = "Entrer un mot de passe.",fill = "white", font=('Arial',13),tag='mdp')
        self.canvas.create_text(640,365, text = "Pas de compte, inscrivez-vous.",fill = "white", font=('Arial',10),tag='info')
        # Entry
        username = Entry(self.root,width=30,textvariable=username)
        password = Entry(self.root,width=30,textvariable=password,show= '*')
        # Button
        b1 =Button(self.root, text = "Se connecter",bg='black',fg='white',command = lambda : self.connect())
        b2 =Button(self.root,text = "S'inscrire",bg='black',fg='white',command = lambda : self.registration_interface())
        # Place
        username.place(relx=0.5,y=240, anchor=CENTER),password.place(relx=0.5,y=290, anchor=CENTER),b1.place(relx=0.5,y=330, anchor=CENTER),b2.place(relx=0.5,y=400, anchor=CENTER)

class Illustration(object):
    rotation = 15
    couleurs_pompes = ["green","red","yellow"]
    couleurs_contenants = ['#ff5a00','#00821a','#ffca00',"#323232"]

    def __init__(self,root):
        self.root = root
        self.canvas = Canvas(root, width=700, height=620, bg='white')
        self.canvas.pack(side=RIGHT)
        self.canvas.pack()

    def __get_couleur(self,etat): 
        return Illustration.couleurs_pompes[0] if etat == "marche" else Illustration.couleurs_pompes[1] if etat == "arret" else Illustration.couleurs_pompes[2]

    def __get_rotation(self,etat):
        return Illustration.rotation if etat == "ouvert" else 0

    def __get_contenant(self,etat,couleur):
        return Illustration.couleurs_contenants[3] if etat == "vide" else couleur

    def refresh_p11(self,etat):
        self.canvas.create_oval(120,85,150,115, fill=self.__get_couleur(etat))
        self.canvas.create_text(135,100, text='p11', fill='white')

    def refresh_p12(self,etat):
        self.canvas.create_oval(160,85,190,115, fill=self.__get_couleur(etat))
        self.canvas.create_text(175,100, text='p12', fill='white')

    def refresh_p21(self,etat):
        self.canvas.create_oval(120+200,85,150+200,115,fill=self.__get_couleur(etat))
        self.canvas.create_text(135+200,100, text='p11', fill='white')

    def refresh_p22(self,etat):
        self.canvas.create_oval(160+200,85,190+200,115,fill=self.__get_couleur(etat))
        self.canvas.create_text(175+200,100, text='p12', fill='white')

    def refresh_p31(self,etat):
        i = 2
        self.canvas.create_oval(120+i*200,85,150+i*200,115,fill=self.__get_couleur(etat))
        self.canvas.create_text(135+i*200,100, text='p11', fill='white')

    def refresh_p32(self,etat):
        i = 2
        self.canvas.create_oval(160+i*200,85,190+i*200,115,fill=self.__get_couleur(etat))
        self.canvas.create_text(175+i*200,100, text='p12', fill='white')

    def refresh_v12(self, etat):
        rotation = self.__get_rotation(etat)
        self.canvas.create_oval(180,280,220,320, fill ='black')
        self.canvas.create_rectangle(195-rotation,280+rotation,205+rotation,320-rotation, width=2, fill ='white', outline= 'black')

    def refresh_v13(self, etat):
        rotation = self.__get_rotation(etat)
        self.canvas.create_oval(370,155,410,195, fill ='black')
        self.canvas.create_rectangle(385-rotation,155+rotation,395+rotation,195-rotation, width=2, fill ='white', outline= 'black')

    def refresh_v23(self, etat):
        rotation = self.__get_rotation(etat)
        self.canvas.create_oval(440,325,480,365, fill ='black')
        self.canvas.create_rectangle(455-rotation,325+rotation,465+rotation,365-rotation, width=2, fill ='white', outline= 'black')

    def refresh_vt12(self, etat):
        rotation = self.__get_rotation(etat)
        self.canvas.create_oval(230,55,270,95, fill ='black')
        self.canvas.create_rectangle(245-rotation,55+rotation,255+rotation,95-rotation, width=2, fill ='white', outline= 'black')

    def refresh_vt23(self, etat):
        rotation = self.__get_rotation(etat)
        self.canvas.create_oval(430,55,470,95, fill ='black')
        self.canvas.create_rectangle(445-rotation,55+rotation,455+rotation,95-rotation, width=2, fill ='white', outline= 'black')

    def refresh_tank1(self,etat):
        couleur = self.__get_contenant(etat,Illustration.couleurs_contenants[0])
        self.canvas.create_rectangle(100, 75, 200, 125,fill=couleur,width=0)
        self.canvas.create_polygon(100, 75, 200, 75, 200, 25, fill=couleur)
        self.canvas.create_text(170,67, text='Tank1', fill='black',font=('Arial','15'))

    def refresh_tank2(self,etat):
        couleur = self.__get_contenant(etat,Illustration.couleurs_contenants[1])
        self.canvas.create_rectangle(300, 25, 400, 125,fill=couleur,width=0)
        self.canvas.create_text(350,67, text='Tank2', fill='black',font=('Arial','15'))

    def refresh_tank3(self,etat):
        couleur = self.__get_contenant(etat,Illustration.couleurs_contenants[2])
        self.canvas.create_rectangle(500, 75, 600, 125,fill=couleur,width=0)
        self.canvas.create_polygon(500, 25, 500, 75, 600, 75, fill=couleur)
        self.canvas.create_text(535,67, text='Tank3', fill='black',font=('Arial','15'))

    def refresh(self, element_nom, etat):
        fonctions = {
            "Tank1":self.refresh_tank1, "Tank2":self.refresh_tank2, "Tank3":self.refresh_tank3,
            "p11":self.refresh_p11,"p12":self.refresh_p12,"p21":self.refresh_p21,"p22":self.refresh_p22,"p31":self.refresh_p31,"p32":self.refresh_p32,"v12":self.refresh_v12,
            "v23":self.refresh_v23,"v13":self.refresh_v13,"vt12":self.refresh_vt12,"vt23":self.refresh_vt23,
        }
        fonction = fonctions.get(element_nom)
        if fonction is not None:
            fonction(etat)
        else:
            raise ValueError("Le nom de la vanne ou de la pompe n'est pas dans le dictionnaire de fonctions.")

    def creer_formes(self):
        # Les lignes entre les carres
        self.canvas.create_line(200, 75, 300, 75)
        self.canvas.create_line(400, 75, 500, 75)
        # Les lignes entre les rectangles :
        # Les lignes de gauche
        self.canvas.create_line(150,125,150,300)
        self.canvas.create_line(125,375,125,250)
        # Les lignes de droite
        self.canvas.create_line(550,125,550,345)
        self.canvas.create_line(570,375,570,175)
        # La ligne horizontale pour v13
        self.canvas.create_line(150,175,571,175)
        # La petite ligne horizontale entre t1 et m1
        self.canvas.create_line(150,250,125,250)
        # La ligne du milieu
        self.canvas.create_line(350,125,350,375)
        # La ligne horizontale
        self.canvas.create_line(150,300,350,300)
        self.canvas.create_line(350,345,550,345)
        self.canvas.create_line(550,245,571,245)
        # Les 3 rectangles du bas
        self.canvas.create_rectangle(105, 375, 145, 475,fill='#808080',width=0)
        self.canvas.create_rectangle(330, 375, 370, 475,fill='#808080',width=0)
        self.canvas.create_rectangle(550, 375, 590, 475,fill='#808080',width=0)
        self.canvas.create_text(125,425, text='M1', fill='black',font=('Arial','15'))
        self.canvas.create_text(350,425, text='M2', fill='black',font=('Arial','15'))
        self.canvas.create_text(570,425, text='M3', fill='black',font=('Arial','15'))
        # Les vannes
        self.canvas.create_text(200,270, text='V12', fill='black', font=('Arial','13','bold'))
        self.canvas.create_text(460,315, text='V23', fill='black', font=('Arial','13','bold'))
        self.canvas.create_text(390,145, text='V13', fill='black', font=('Arial','13','bold'))
        # Les pompes des réservoirs
        for i in range(3):
            self.canvas.create_rectangle(115+i*200, 80, 195+i*200, 120)
        # Les vannes pour réservoir
        self.canvas.create_text(250,40, text='VT12', fill='black', font=('Arial','13','bold'))
        self.canvas.create_text(450,40, text='VT23', fill='black', font=('Arial','13','bold'))

class Historique(object):
    def __init__(self,canvas,username,password):
        global histo
        self.canvas = canvas
        self.username = username
        self.password = password
        histo = Button(self.canvas,text = "Historique",bg='black',fg='white',command = lambda : self.historic(self.canvas,self.username,self.password))
        histo.place(x=605,y=20)
        self.help_button = Button(self.canvas,text = " ? ",bd=5,bg='black',fg='white',command = lambda : self.aide())
        self.help_button.place(x=340,y=530)
    def historic(self,syscanva,user,passw):
        global quit, Histocanvas
        histo.destroy()
        chemin = f'./Simulateur/score/{user}_{passw}.txt'
        Histocanvas = Canvas(syscanva, width=700, height=620, bg='black')
        Histocanvas.pack()
        Histocanvas.create_text(350,75, text=user, fill='white',font=('Arial','20'))
        # Verifie si un fichier avec les identifiants existe.
        if isfile(chemin) is True:
            with open(chemin)as f:
                liste,ligne=[],f.readline()
                while ligne != '':
                    characters = '\n'
                    ligne = ''.join(x for x in ligne if x not in characters)
                    ligne = ligne.split(',')
                    liste.extend(ligne)
                    ligne = f.readline()
                indice = 0
                for i in range(len(liste)//2):
                    Histocanvas.create_rectangle(100,110+20*i,600,130+20*i,fill ='black',outline='white')
                    Histocanvas.create_text(225,122.5+20*i, text=liste[indice+1], fill='white',font=('Arial','9'))
                    Histocanvas.create_line(350,110+20*i,350,130+20*i,fill='white')
                    Histocanvas.create_text(475,122.5+20*i, text=liste[indice], fill='white',font=('Arial','9'))
                    indice +=2
        # Sinon retourne un message.
        else:
            Histocanvas.create_text(350,125, text='Aucun score encore enregistrer', fill='white',font=('Arial','14'))
        quit = Button(Histocanvas,text=' X ',bg='black',fg='white',command = lambda : self.quit(syscanva))
        quit.place(x=20,y=20)
        
    def quit(self,syscanva):
        # Supprime le canvas et le bouton pour quitter l'historique. Et réaffiche un nouveau bouton historique.
        quit.destroy(), Histocanvas.destroy()
        histo = Button(syscanva,text = "Historique",bg='black',fg='white',command = lambda : self.historic(syscanva,self.username,self.password))
        histo.place(x=605,y=20)
    
        self.help_button = Button(self.canvas,text = " ? ",bd=5,bg='black',fg='white',command = lambda : self.aide())
        self.help_button.place(x=340,y=530)
        
    def aide(self):
        self.help_button.destroy()
        aide_canvas = Canvas(self.canvas,width=600, height=100, bg='grey')
        aide_canvas.place(x=50,y=500)
        aide_canvas.create_rectangle(30,550,550,600,fill='grey',outline='grey',tag='aide')
        # Vanne ouverte
        aide_canvas.create_oval(10,10,30,30, fill ='black',outline='white')
        aide_canvas.create_rectangle(19,11,22,30, width=2, fill ='white', outline= 'white')
        aide_canvas.create_text(80,20, text=': Vanne ouverte', fill='white',font=('Arial','10'))
        # Vanne fermée
        aide_canvas.create_oval(10,45,30,65, fill ='black',outline='white')
        aide_canvas.create_rectangle(11,54,29,57, width=2, fill ='white', outline= 'white')
        aide_canvas.create_text(80,55, text=': Vanne fermée', fill='white',font=('Arial','10'))
        # Pompes en marche
        aide_canvas.create_oval(10,80,30,100, fill ='green',outline='')
        aide_canvas.create_text(90,90, text=': Pompe en marche', fill='white',font=('Arial','10'))
        # Pompes en arret
        aide_canvas.create_oval(210,10,230,30, fill ='red',outline='')
        aide_canvas.create_text(283,20, text=': Pompe en arret', fill='white',font=('Arial','10'))
        # Pompes en panne
        aide_canvas.create_oval(210,45,230,65, fill ='#FFA4A4',outline='')
        aide_canvas.create_text(287,55, text=': Pompe en panne', fill='white',font=('Arial','10'))
        # Reservoir plein:
        aide_canvas.create_rectangle(210,80,230,100, fill ='#ff5a00',outline='')
        aide_canvas.create_rectangle(217,80,223,100, fill ='#00821a',outline='')
        aide_canvas.create_rectangle(223,80,230,100, fill ='#ffca00',outline='')
        aide_canvas.create_text(284,90, text=': Reservoir plein', fill='white',font=('Arial','10'))
        # Reservoir vide:
        aide_canvas.create_rectangle(400,10,420,30, fill ='#2C2C2C',outline='')
        aide_canvas.create_text(470,20, text=': Reservoir vide', fill='white',font=('Arial','10'))
        quithelp = Button(self.canvas,text=' X ',bg='black',fg='white',command = lambda : self.quithelp(quithelp,aide_canvas))
        quithelp.place(x=500,y=560)

    def quithelp(self,quithelp,aide_canvas):
        quithelp.destroy()
        aide_canvas.destroy()
        help_button = Button(self.canvas,text = " ? ",bd=5,bg='black',fg='white',command = lambda : self.aide())
        help_button.place(x=340,y=530)
        help = Button(self.canvas,text = " ? ",bd=5,bg='black',fg='white',command = lambda : self.aide())
        help.place(x=340,y=530)

if __name__ == "__main__":
    root = Root()
    menu = Menu(root)
    menu.creer_menu()
    root.mainloop()