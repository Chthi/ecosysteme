# -*- coding: utf-8 -*-

##################################################
##    fichier : localisation.py
##    auteur : Thibault Charmet
##    version : 2.1
##    date : 20/01/2018
##    description : Ensemble de méthodes permettants de localiser 
##                  des entités sur une carte
##################################################

# Tab size  : 4
# Soft tabs : YES

# Importation des librairies
from random import randint

# Importation des modules
from ecosysteme.constants import UE



##################################################
##    Classe :            class Position():
##    Auteur :            Thibault Charmet
##    Docstring :         classe qui gère des positions
##    Pré-conditions :    
##################################################

class Position():
	""" classe qui gère des positions """
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def random(dim):
		return Position(randint(0, dim.x-1), randint(0, dim.y-1))



##################################################
##    Classe :            class Localisation():
##    Auteur :            Thibault Charmet
##    Docstring :         
##    Pré-conditions :    
##################################################

class Localisation():
	"""  """
	def __init__(self, dim):
		self.tab = list()
		for x in range(0, dim.x):
			self.tab.append([])
			for y in range(0, dim.y):
				self.tab[x].append([])


	def localise(self, objet):
		self.tab[objet.pos.x][objet.pos.y].append(objet)


	def delocalise(self, objet):
		# print("delocalise", objet.nom, objet.pos.x, objet.pos.y)
		# print(self.tab[objet.pos.x][objet.pos.y])
		self.tab[objet.pos.x][objet.pos.y].remove(objet)


	def getInstance(self, pos, nomInstance):
		# Progression dans la recherche de l'entité sur la position
		i, fin = 0, False
		# liste des entitées présentes à la position
		entites = self.tab[pos.x][pos.y]
		while i < len(entites) and not fin:
			fin = (entites[i].nom == nomInstance)
			i += 1
		if fin:
			return entites[i-1]
		else:
			return None
			# raise Exception("Instance not found for (x,y)= ("+str(pos.x)+","+str(pos.y)+"). trouvé : "+str(localisation[pos.x][pos.y]))



