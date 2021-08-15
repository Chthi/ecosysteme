# -*- coding: utf-8 -*-

##################################################
##    fichier : simulation.py
##    auteur : Thibault Charmet
##    version : 2.1
##    date : 20/01/2018
##    description : Classe définissant une simulation d'écosystème
##################################################

# Tab size  : 4
# Soft tabs : YES

# Importation des librairies
import tkinter as tk
from random import random, randint
from time import sleep
from math import sqrt, trunc

# Importation des modules
# from ecosysteme.graphiques import *
from ecosysteme.localisation import Position, Localisation
from ecosysteme.vie import Biche, Loup, Herbe
from ecosysteme.constants import UE



##    fonction : tableau(x_dim, y_dim)
##    auteur : Thibault Charmet
##    description : créé un tableau à deux dimensions de taille x_dim, y_dim
##    param x_dim : premier index du tableau. Correspond à sa largeur. La case 0 est la plus à gauche.
##    param y_dim : second index du tableau. Correspond à sa hauteur. La case 0 est la plus en haut.
##    return : liste de listes de None

def tableau(x_dim, y_dim):
	tab = list()
	for x in range(0,x_dim):
		tab.append([])
		for y in range(0,y_dim):
			tab[x].append(None)
	return tab



def assigneEspece(nom, dim, carte, simulation, x=None, y=None, rand=False, *args, **kwargs):
	pos = Position.random(dim)
	if nom == "loup":
		etre_vivant = Loup(dim, carte, pos, simulation, *args, **kwargs)
	elif nom == "biche":
		etre_vivant = Biche(dim, carte, pos, simulation, *args, **kwargs)
	else:
		raise Exception("Espèce inconnue : "+nom)
	return etre_vivant




##################################################
##    Classe :            class simulation():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui simule un ecosystème
##    Pré-conditions :    largeur et hauteur (px) doivent êtres multiple de 4. entitées disponibles : biche, loup.
##################################################

class Simulation():
	""" classe qui simule un ecosystème """
	def __init__(self, animaux = {"biche" : 2}, largeur = 40, hauteur = 40):
		# création de la fenêtre principale qui affichera l'environement
		self.root = tk.Tk()
		# dimensions de la carte (en pixels)
		self.size = Position(largeur, hauteur)
		# dimensions de l'environement (en UE : voir constantes)
		self.dim = Position(largeur // UE, hauteur // UE)
		# dictionnaire contenant l'ensemble des effectifs des entitées
		self.populace = animaux
		# temps depuis le début de la simulation
		self.temps = 0
		# vitesse actuelle de jeu
		self.vitesse = 1
		# liste des espèces éteintes
		self.extinction = []
		# tableau à deux dimensions contenant l'ensemble des entitées de la simulation
		self.localisation = Localisation(self.dim)
		# liste des entités tout juste créées
		self.recensement = list()
		# si on doit quitter la simulation en cours
		self.Quitter = False
		# si on doit ouvrir la fenêtre d'informations
		self.infos = False
		# la faune et la flore vivant dans la simulation
		self.faune = dict()
		self.flore = dict()


		# ensembles des éléments contenus dans la fenêtre
		self.interface = dict()
		# affichage du temps actuelle de jeu
		self.interface["Temps"] = tk.Label(self.root, text="Temps : "+str(self.temps), font="Arial 8", anchor='ne')
		self.interface["Temps"].pack()
		# Affichage des espèces éteintes
		self.interface["Extinction"] = tk.Label(self.root, text="Espèces éteintes : "+str(self.extinction), font="Arial 10", anchor='w')
		self.interface["Extinction"].pack()
		# Affichage de la carte
		self.interface["Carte"] = tk.Canvas(self.root, width=self.dim.x*UE, height=self.dim.y*UE, borderwidth=0, background="#E0CDA9", takefocus="1")
		self.interface["Carte"].pack()
		# Affichage des populations des espèces
		self.interface["Population"] = tk.Label(self.root, text="Population animal : \n"+str(animaux), font="Arial 10", anchor='w')
		self.interface["Population"].pack()
		# Affichage du bouton quitter
		self.interface["Quitter"]  = tk.Button(self.root, text="Stopper la simulation", command=self.Quit)
		self.interface["Quitter"].pack()
		# Affichage de la barre de changement de vitesse
		self.interface["Vitesse"] = tk.Scale(self.root, orient="horizontal", from_=1, to=10, resolution=1, tickinterval=9, length=100, label="Vitesse")
		self.interface["Vitesse"].pack()
		# Affichae du bouton ajoutant des informations
		self.interface["Informations"] = tk.Button(self.root, text="Obtenir des informations sur cet écosystème.", font="Arial 8", command=self.open_informations)
		self.interface["Informations"].pack()

		# création des entitées herbes
		self.flore["herbe"] = []
		for i in range(0, self.dim.x * self.dim.y):
			# On créé l'entité
			herbe = Herbe(dim=self.dim, carte=self.interface["Carte"], simulation=self)
			# On l'ajoute à la flore
			self.flore["herbe"].append(herbe)
			# On enregistre sa position sur la carte
			self.localisation.localise(herbe)

		print(str(self.dim.x * self.dim.y)+" éléments en théorie. en pratique : "+str(len(self.flore["herbe"])))

		# On créé les animaux
		for animal, nombre in animaux.items():
			# S'il y en à plus d'un on considère l'existence de l'espèce entière
			if nombre > 0:
				self.faune[animal] = []
				# On créé autant d'animaux de l'espèce que nécéssaire
				for i in range(0, nombre):
					# On créé l'entité
					etre_vivant = assigneEspece(animal, self.dim, self.interface["Carte"], self, rand=True) # create an animal with the good class
					# On l'ajoute à son espèce
					self.faune[animal].append(etre_vivant)
					# On enregistre sa position sur la carte
					self.localisation.localise(etre_vivant)

		print("animaux init")

	"""def pause(event):
		fen.after(100, pause)"""

	def Quit(self):
		self.Quitter = True

	def Quit_infos(self):
		self.infos = False
		self.fen_infos.destroy()

	def affiche_infos(self):
		self.interface["Liste"].get() # command=self.affiche_infos
		"('t0', 't1', ...)"

	def open_informations(self):
		# création de la fenêtre d'informations
		self.fen_infos = tk.Tk()
		# ajout d'une barre de scroll verticale
		yDefilB = tk.Scrollbar(self.fen_infos, orient='vertical')
		yDefilB.grid(row=0, column=1, sticky='ns')
		# ajout d'une barre de scroll horizontale
		xDefilB = tk.Scrollbar(self.fen_infos, orient='horizontal')
		xDefilB.grid(row=1, column=0, sticky='ew')
		# ajout d'une liste de chaines
		selection = tk.StringVar()
		self.interface["Liste"] = tk.Listbox(self.fen_infos, listvariable=selection, xscrollcommand=xDefilB.set, yscrollcommand=yDefilB.set, height="10")
		self.interface["Liste"].grid(row=0, column=0, sticky='nsew')
		# on lie la scrollbar et la liste
		xDefilB['command'] = self.interface["Liste"].xview
		yDefilB['command'] = self.interface["Liste"].yview
		# ajout du bouton pour fermer la fenêtre
		self.interface["Quitter infos"] = tk.Button(self.fen_infos, text="Fermer les informations.", command=self.Quit_infos)
		self.interface["Quitter infos"].grid(row=1, column=1, sticky='nsew')
		# par défault on ne quitte pas
		self.infos = True

	def actualise_infos(self):
		self.interface["Liste"].delete(0, tk.END)
		for nom, espece in self.faune.items():
			for individu in espece:
				self.interface["Liste"].insert(tk.END, nom +" "+ str(individu)[-11:-1])

	def eteindre(self):
		for espece, population in self.faune.items():
			if len(population) > 0:
				k = 0;
				while k < len(population):
					individu = population[k]
					# S'il est vivant on passe au suivant
					if individu.alive:
						k += 1
					else:
						# On efface la représentation graphique de l'animal
						self.interface["Carte"].delete(self.faune[espece][k].image)
						# On retire la localisation de l'animal
						self.localisation.delocalise(individu)
						# On supprime l'instance de l'animal
						del individu
						# On retire l'animal de la faune
						del self.faune[espece][k]
						# On fait décroitre la population
						self.populace[espece] -= 1
				# S'il ne reste plus d'animaux d'une espèce on la considère éteinte
				if (self.populace[espece] == 0):
					self.extinction.append(espece) # A species would become extinct if all animals of this species are missing.


	def recense(self):
		for baby in self.recensement:
			# On ajoute le nouveau né à la liste des individus de son espèce
			self.faune[baby.nom].append(baby)
			# la population augmente
			self.populace[baby.nom] += 1
			# On enregistre sa position sur la carte
			self.localisation.localise(baby)
		self.recensement = []


	def run(self):
		#self.root.bind("<Escape>",end)
		#self.root.bind("<KeyPress-p>",pause)
		
		# On génère la simulation tant que l'on ne demande pas de quitter
		while not self.Quitter:

			# Le temps avance
			self.temps += 1
			self.interface["Temps"]["text"] = "Temps : "+str(self.temps)

			# Les plantes grandissent
			for plantes in self.flore:
				for plante in self.flore[plantes]:
					plante = plante.grow()

			# Les animaux bougent se reproduisent
			# print("espèces : ", len(self.faune))
			for animal in self.faune:
				# print("individus : ", len(self.faune[animal]))
				for individu in self.faune[animal]:
					# ensemble des interactions de l'entité
					individu.move()
					self.recense()

			# On détruit les entitées mortes
			self.eteindre()

			# On actualise la fenêtre d'informations
			if self.infos:
				self.actualise_infos()

			# On actualise l'affichage de la population
			self.interface["Population"]["text"] = "Population animal : \n"+str(self.populace)
			# On actualise l'affichage des espèces éteintes
			self.interface["Extinction"]["text"] = "Espèces éteintes : "+str(self.extinction)
			# On actualise la fenêtre graphique principale
			self.root.update()
			# On actualise la valeur de la vitesse de simulation
			self.vitesse = self.interface["Vitesse"].get()
			# On attend pendant une periode égale à l'inverse de la fréquence
			sleep(1 / self.vitesse)
			#fen.after(100, run)

		# après avoir quitté on ferme la fenêtre
		self.root.destroy()




