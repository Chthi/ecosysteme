# -*- coding: utf-8 -*-

##################################################
##    fichier : vie.py
##    auteur : Thibault Charmet
##    version : 2.1
##    date : 20/01/2018
##    description : Ensemble de classes définissant la faune
##                  de l'écosystème
##################################################

# Tab size  : 4
# Soft tabs : YES

# Importation des librairies
import tkinter as tk
from random import random, randint
# from time import sleep
from math import sqrt, trunc

# Importation des modules
from ecosysteme.localisation import Position, Localisation
# from ecosysteme.graphiques import *
from ecosysteme.constants import UE




##################################################
##    Classe :             class vie():
##    Auteur :             Thibault Charmet
##    Docstring :          Classe qui contient toutes les classes simulant la vie.
##################################################

class Vie():
	""" Classe qui contient toutes les classes simulant la vie. """

	def __init__(self, dim, carte, pos, simulation):
		# dimention de l'environement
		self.dim = dim
		# environement graphique
		self.carte = carte
		# position sur la carte
		self.pos = pos
		self.simulation = simulation


	def voisins(self, rayon):
		lst_voisins = []
		for i in range(-rayon, rayon+1):
			# for j in range(abs(i) - rayon, rayon - abs(i) + 1):
			for j in range(-rayon, rayon+1):
				if not (i==0 and j==0):
					vos = Position((self.pos.x+i) % self.dim.x, (self.pos.y+j) % self.dim.y)
					lst_voisins.append(vos)
		return lst_voisins


##################################################
##    Classe :            class flore():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui contient toutes les classes simulant des animaux
##################################################

class Flore(Vie):
	""" classe qui contient toutes les classes simulant des plantes """


##################################################
##    Classe :            class herbe(flore):
##    Auteur :             Thibault Charmet
##    Docstring :            class qui simule une herbe
##################################################

class Herbe(Flore):
	""" classe qui simule l'herbe """

	# teintes de l'herbe en fonction de sa densité
	teintes = {10:"#187B01", 9:"#298C12", 8:"#3A9D23", 7:"#4BAE34", 6:"#5CBF45", 5:"#6DCF56", 4:"#7EDF67", 3:"#8FEF78", 2:"#BFFFAB", 1:"#D8DEAA", 0:"#E0CDA9"}
	# identifiant des entitées herbe
	ID = 0

	def __init__(self, dim, carte, simulation):
		if Herbe.ID > (dim.x*dim.y):
			print("Attention il n'y a plus de place pour l'herbe ici.")
		self.nom = "herbe"
		# On détermine la position du bloc d'herbe en fonction de son ordre d'apprition
		# self.x = (Herbe.ID*UE) % dim.x +(UE//2)
		# self.y = (Herbe.ID*UE) // dim.x *UE +(UE//2)
		self.x = (Herbe.ID % dim.x)*UE + (UE//2)
		self.y = (Herbe.ID // dim.x)*UE + (UE//2)
		# définition de l'environement
		Vie.__init__(self, dim, carte, Position(self.x, self.y), simulation)
		self.pos = Position(Herbe.ID % dim.x, Herbe.ID // dim.x)
		# print(self.pos.x, self.pos.y)
		# print("Je suis une herbe"+str(Herbe.ID)+": ("+str(self.x)+","+str(self.y)+")")
		self.density = 100
		self.GR = 1 # grow region : the distance where grass can sow other fields
		self.image = carte.create_rectangle(self.x,self.y, self.x+UE,self.y+UE, fill=Herbe.teintes[self.density // 10], width=0)
		Herbe.ID += 1


	def grow(self):
		if self.density < 100:
			total_density = 0
			for pos in self.voisins(self.GR):
				voisin = self.simulation.localisation.getInstance(pos, "herbe")
				total_density += voisin.density
			self.density = min(trunc(self.density + self.density*0.005 + total_density*0.0005 + 1), 100)
			# print("grow, seeds, roots", self.density*0.005, total_density*0.0005, 1)
			#print("total density : "+str(total_density))
			#print("grow => "+str(trunc(self.density*0.01 + total_density*0.001 + 1)))
			if self.density < 0 :
				raise Exception("Density = "+str(self.density))
			self.carte.delete(self.image)
			self.image = self.carte.create_rectangle(self.x,self.y, self.x+UE,self.y+UE, fill=Herbe.teintes[self.density // 10], width=0)


##################################################
##    Classe :            class faune():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui contient toutes les classes simulant des animaux
##################################################

class Faune(Vie):
	""" classe qui contient toutes les classes simulant des animaux """
	nombre_moyen_petits = {"biche" : (20,(1,2)), "loup" : (20,(1,4))}
	vieillesse = {"biche" : (1300, 1820), "loup" : (1040, 1800)} # en jours
	actif = {"biche" : (2, 4), "loup" : (1, 3)}
	total_hunger = {"biche" : 100, "loup" : 140}
	agilite = {"biche" : (1,5), "loup" : (1,1)}
	age_reproduction = {"biche" : 40, "loup" : 50} # en jours
	state = "walk" # fight, flight, eat, breed, walk / sleep
	alive = True
	age = 0

##    Prototype :            def getLocalDistance(pos, largeur, x, y):
##    Auteur :             Thibault Charmet
##    Retour :            Retourne le distance réelle qui sépare un objet de localisation et un autre objet défini par ses coordonnées.
##    Pré-conditions :    pos in [0,largeur-1*hauteur-1] et x, y in [0, largeur-1][0, hauteur-1]

	# def getLocalDistance(pos, largeur, x, y):
	# 	return sqrt((x - (pos // largeur))**2 + (y - (pos % largeur))**2)

	@staticmethod
	def distance(pos, x, y):
		return sqrt( (x - pos.x)**2 + (y - pos.y)**2 )

##    Prototype :            def getNearest(self, nom, state):
##    Auteur :             Thibault Charmet
##    Retour :            Retourne l'entité la plus proche de soi ayant un nom et un état préscis. Pour prendre n'importe quel état state doit valoir None.
##                        Retourne None si aucune entité correspondant aux critères n'est trouvé.
##    Pré-conditions :    state = None => state ne devient plus une contrainte. nom existant.

	def getNearest(self, nom, state=None):
		dist, res = None, None
		for x in range(0, self.dim.x):
			for y in range(0, self.dim.y):
				if (dist == None) or (self.distance(self.pos, x, y) < dist):
					for entity in self.simulation.localisation.tab[x][y]:
						# if (entity is self):
						# 	print("print((entity is self))")
						if (entity.nom == nom) and ((state == None) or (entity.state == state)) and (entity is not self):
							dist = self.distance(self.pos, x, y)
							res = entity
		return res


	def getValeur(self, probabilite):
		valeur = probabilite[0]
		if 10*random() <= probabilite[1]:
			valeur += 1
		return valeur

	def moveRandom(self):
		self.simulation.localisation.delocalise(self)
		mouvement = self.getValeur(self.vitesse)
		xd, yd = randint(-1, 1) * mouvement, randint(-1, 1) * mouvement
		self.pos = Position((self.pos.x + xd)% self.dim.x, (self.pos.y + yd)% self.dim.y)
		self.carte.coords(self.image, self.pos.x*UE-self.r, self.pos.y*UE-self.r, self.pos.x*UE+self.r, self.pos.y*UE+self.r)
		self.carte.tag_raise(self.image, self.simulation.localisation.getInstance(self.pos, "herbe").image )
		self.simulation.localisation.localise(self)


	def get_xd(self, entity, mouvement):
		if (entity.pos.x - self.pos.x) >= 0:
			xd = min(mouvement, entity.pos.x - self.pos.x)
		else:
			xd = max(-mouvement, entity.pos.x - self.pos.x)
		mouvement -= abs(xd)
		return (mouvement, xd)

	def get_yd(self, entity, mouvement):
		if (entity.pos.y - self.pos.y) >= 0:
			yd = min(mouvement, entity.pos.y - self.pos.y)
		else:
			yd = max(-mouvement, entity.pos.y - self.pos.y)
		mouvement -= abs(yd)
		return (mouvement, yd)

	def moveToward(self, entity):
		self.simulation.localisation.delocalise(self)
		mouvement = self.getValeur(self.vitesse)
		if (randint(0,1) == 0):
			(mouvement, xd) = self.get_xd(entity, mouvement)
			(mouvement, yd) = self.get_yd(entity, mouvement)
		else:
			(mouvement, yd) = self.get_yd(entity, mouvement)
			(mouvement, xd) = self.get_xd(entity, mouvement)

		# print(str(xd)+","+str(yd))
		self.pos = Position((self.pos.x + xd)% self.dim.x, (self.pos.y + yd)% self.dim.y)
		self.carte.coords(self.image, self.pos.x*UE-self.r, self.pos.y*UE-self.r, self.pos.x*UE+self.r, self.pos.y*UE+self.r)
		self.carte.tag_raise(self.image, self.simulation.localisation.getInstance(self.pos, "herbe").image)
		self.simulation.localisation.localise(self)

	def moveAway(self, entity):
		self.simulation.localisation.delocalise(self)
		mouvement = self.getValeur(self.vitesse)
		if (randint(0,1) == 0):
			xd = mouvement * (-1 if (entity.pos.x - self.pos.x) > 0 else 1)
			yd = 0
		else:
			xd = 0
			yd = mouvement * (-1 if (entity.pos.y - self.pos.y) > 0 else 1)

		# print(str(xd)+","+str(yd))
		self.pos = Position((self.pos.x + xd)% self.dim.x, (self.pos.y + yd)% self.dim.y)
		self.carte.coords(self.image, self.pos.x*UE-self.r, self.pos.y*UE-self.r, self.pos.x*UE+self.r, self.pos.y*UE+self.r)
		self.carte.tag_raise(self.image, self.simulation.localisation.getInstance(self.pos, "herbe").image)
		self.simulation.localisation.localise(self)

	def reproduction(self, entity):
		if (entity.pos.y == self.pos.y) and (entity.pos.x == self.pos.x):
			petits = self.getValeur(Faune.nombre_moyen_petits[self.nom][1])
			# print("petits", petits)
			for p in range(0, petits):
				entity.hunger -= Faune.nombre_moyen_petits[self.nom][0]
				self.hunger -= Faune.nombre_moyen_petits[self.nom][0]
				# create a child of the same class
				if self.nom == "biche":
					petit = Biche(self.dim, self.carte, self.pos, self.simulation)
				elif self.nom == "loup":
					petit = Loup(self.dim, self.carte, self.pos, self.simulation)
				else:
					raise Exception("Espèce inconnue : "+self.nom)
				petit.hunger = 2*Faune.nombre_moyen_petits[self.nom][0]
				self.simulation.recensement.append(petit)
			self.state = "walk"
			entity.state = "walk"
				

##################################################
##    Classe :            class biche(faune):
##    Auteur :             Thibault Charmet
##    Docstring :            class qui simule une biche
##################################################

class Biche(Faune):
	""" classe qui simule une biche """
	def __init__(self, dim, carte, pos, simulation):
		# nom de l'espèce
		self.nom = "biche"
		# environement
		Vie.__init__(self, dim, carte, pos, simulation)
		# barre de faim
		self.hunger = self.total_hunger[self.nom]
		# barre de vie
		self.life = 100
		# vitesse de déplacement
		self.vitesse = self.agilite[self.nom]

		# rayon du cercle graphiquement
		self.r = 2
		# représentation graphique
		self.image = carte.create_oval(self.pos.x*UE - self.r, self.pos.y*UE - self.r,
									   self.pos.x*UE + self.r, self.pos.y*UE + self.r,
									   fill="Brown", outline="Green", width="0")
	 
		# print("Je suis une biche: ("+str(self.x)+","+str(self.y)+")")


	def move(self):
		if (self.hunger >= 85) and (self.age >= self.age_reproduction[self.nom]):
			self.state = "breed"
			partenaire = self.getNearest("biche", "breed")
			if partenaire != None:
				self.moveToward(partenaire)
				self.reproduction(partenaire)
			else:
				self.moveRandom()
		elif randint(0, 0) == 0:
			predateur = self.getNearest("loup")
			if predateur:
				self.moveAway(predateur)
			else :
				self.moveRandom()
			self.state = "walk"
			# self.state = "eat"
			self.manger() # système de faim/danger
		else:
			self.state = "walk"
			self.moveRandom()
			# self.state = "eat"
			self.manger() # système de faim/danger
		# print(self.hunger)
		self.age += 1
		self.hunger -= randint(self.actif[self.nom][0], self.actif[self.nom][1])
		if self.age >= self.vieillesse[self.nom][0]:
			trop_vieux = randint(0, self.vieillesse[self.nom][1] - self.vieillesse[self.nom][0])
			self.alive = (trop_vieux == 0)
		self.alive = self.alive and (self.hunger > 0)

	def manger(self):
		herbe = self.simulation.localisation.getInstance(self.pos, "herbe")
		kg = min([100-self.hunger, 15, herbe.density])
		self.hunger += kg
		herbe.density -= kg
		if herbe.density < 0 :
			raise Exception("Density = "+str(herbe.density))


##################################################
##    Classe :            class loup(faune):
##    Auteur :             Thibault Charmet
##    Docstring :            class qui simule un loup
##################################################

class Loup(Faune):
	""" classe qui simule un loup """
	def __init__(self, dim, carte, pos, simulation):
		# nom de l'espèce
		self.nom = "loup"
		# environement
		Vie.__init__(self, dim, carte, pos, simulation)
		# barre de faim
		self.hunger = self.total_hunger[self.nom]
		# barre de vie
		self.life = 70
		# vitesse de déplacement
		self.vitesse = self.agilite[self.nom]

		# rayon du cercle graphiquement
		self.r = 2
		# représentation graphique
		self.image = carte.create_oval(self.pos.x*UE - self.r, self.pos.y*UE - self.r,
									   self.pos.x*UE + self.r, self.pos.y*UE + self.r,
									   fill="Grey", outline="Black", width="0")
		# print("Je suis un loup: ("+str(self.x)+","+str(self.y)+")")


	def move(self):
		if (self.hunger >= 120) and (self.age >= self.age_reproduction[self.nom]):
			self.state = "breed"
			partenaire = self.getNearest("loup", "breed")
			if partenaire != None:
				self.moveToward(partenaire)
				self.reproduction(partenaire)
			else:
				self.moveRandom()
		elif self.hunger > 100:
			self.moveRandom()
		else:
			proie = self.getNearest("biche", None) # liste proie
			if proie != None:
				self.moveToward(proie)
				if (self.pos.x == proie.pos.x) and (self.pos.y == proie.pos.y):
					self.manger(proie)
			else:
				self.moveRandom()
		# print(self.hunger)
		self.age += 1
		self.hunger -= randint(self.actif[self.nom][0], self.actif[self.nom][1])
		if self.age >= self.vieillesse[self.nom][0]:
			trop_vieux = randint(0, self.vieillesse[self.nom][1] - self.vieillesse[self.nom][0])
			self.alive = (trop_vieux == 0)
		self.alive = self.alive and (self.hunger > 0)


	def manger(self, proie): # liste des proies
		kg = min([self.total_hunger[self.nom]-self.hunger, self.total_hunger[self.nom], proie.hunger]) # faire système de meute / partage ou une viande qui tombe au sol...
		self.hunger += kg
		# print("Miam !"+str(self.hunger))
		proie.hunger -= kg
		proie.alive = False
