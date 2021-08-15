# -*- coding: utf-8 -*-

##################################################
##    fichier : ecosysteme.py
##    auteur : Thibault Charmet
##    version : 2.1
##    date : 20/01/2018
##    description : Génère sur mesure une simulation d'écosystème virtuel
##################################################

# Tab size  : 4
# Soft tabs : YES


# Importation des librairies
from random import randint
import tkinter as tk

# Importation des modules
# from ecosysteme.graphiques import *
from ecosysteme.constants import UE
from ecosysteme.simulation import Simulation


##    Prototype :            def lancement(Paramètres):
##    Auteur :             Thibault Charmet
##    Objectif :            lancer une simulation d'écosystème
##    Pré-conditions :    le dictionaire animaux et la liste echelles doivent exister, échelle doit
##                        contenir les objets Tkinter scale contenant les valeurs des animaux
##    Retour :            aucun

def lancement():
	i, L, H = 0, echelle_largeur.get(), echelle_hauteur.get()
	for animal in animaux:
		animaux[animal] = echelles[i].get()
		i += 1
	print(animaux)

	window.destroy()
	ecosysteme = Simulation(animaux, L, H)
	ecosysteme.run()
	del ecosysteme




def actualise(event):
	frame['width'] = echelle_largeur.get()
	frame['height'] = echelle_hauteur.get()
	frame['scrollregion'] = (0, 0, 0, echelle_hauteur.get())



def mode_lags():
	if do_you_want_to_lag.get() == "oui":
		echelle_largeur["to"] = 1600
		echelle_hauteur["to"] = 1600
		echelle_largeur["tickinterval"] = 380
		echelle_hauteur["tickinterval"] = 380
		for echelle in echelles:
			echelle["to"] = 1000
			echelle["tickinterval"] = 200
		message["text"] = "Attention dans ces conditions vous faites sauter toutes les sécurités garantissant \n que votre état de santé reste stable dans le meilleur des mondes possibles."
	else:
		echelle_largeur["to"] = 400
		echelle_hauteur["to"] = 400
		echelle_largeur["tickinterval"] = 50
		echelle_hauteur["tickinterval"] = 50
		for echelle in echelles:
			echelle["to"] = 50
			echelle["tickinterval"] = 25
			message["text"] = ""



def bouger(event):
	frame.scan_dragto(event.x, event.y, 10)

def prendre(event):
	frame.scan_mark(event.x, event.y)




#--------------------------------------------------------------------------------------
#                                   Début du programme
#--------------------------------------------------------------------------------------


# nombre d'entitées par défault
animaux = {"biche" : 0, "loup" : 0}
# fenêtre de choix des options
window = tk.Tk()

window.title('Ecosystem simulator')
echelles = list()
for animal in animaux:
	echelle = tk.Scale(window, orient="horizontal", from_=0, to=50, resolution=1,tickinterval=25, length=200, label="Nombre de " + animal + " : ")
	echelle.set(randint(0,20))
	echelle.pack()
	echelles.append(echelle)

frame = tk.Canvas(window, width=20, height=20, borderwidth="2", background="#000ddd555", confine="False", scrollregion=(0, 0, 0, 0), xscrollincrement=1)
echelle_largeur = tk.Scale(window, orient="horizontal", from_=20, to=400, resolution=UE, tickinterval=50, length=400, label="Largeur de l'environement :", command=actualise)
echelle_hauteur = tk.Scale(window, orient="horizontal", from_=20, to=400, resolution=UE, tickinterval=50, length=400, label="Hauteur de l'environement :", command=actualise)
echelle_largeur.set(200)
echelle_hauteur.set(200)
echelle_largeur.pack()
echelle_hauteur.pack()
frame.pack()
frame.bind("<Button-1>",prendre)
frame.bind("<Motion>",bouger)

zone_options = tk.Canvas(window, width=80, height=40)
zone_options.pack()
do_you_want_to_lag = tk.StringVar()
check_for_lags = tk.Checkbutton(zone_options, variable=do_you_want_to_lag, command=mode_lags, text='Activer le mode lag ', onvalue='oui', offvalue='non', anchor='sw')
check_for_lags.pack(side = tk.LEFT)
check_for_lags.deselect()

truc = tk.Checkbutton(zone_options, text='truc qui sert à rien', anchor='se')
truc.pack(side = tk.RIGHT)
machin = tk.Checkbutton(zone_options, text='machin qui sert à rien')
machin.pack(side = tk.TOP)

bouton_run = tk.Button(zone_options, text="Lancer", command=lancement, anchor='s')
bouton_run.pack(side = tk.BOTTOM) # side = BOTTOM

message = tk.Label(window, text="")
message.pack()

window.mainloop()
