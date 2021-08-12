# -*- coding: utf-8 -*-

from tkinter import *
from random import *
from time import *
from math import *

#------------------------------------------------
#                 Constantes :
UE = 4 # UE pour unité élémentaire. C'est le coté (en px) de la plus petite case utilisé.
#------------------------------------------------

# faire graphique
# faire age des animaux
# mutations
# voir la fiche d'un animal random / ou la moyenne des espèces.
# faire la carte sans retour de l'autre coté
# généralisé move
# get nearest ne trouve pas d'entité sur la même pos / prendre en compte alive

#--------------------------------------------------------------------------------------
#                                   Décorateurs :
def GPS(fonction_sans_GPS):
    """ Décorateur chargé de délocaliser l'instance au début de la fonction puis le la localiser à la fin. """
    def fonction_avec_GPS(self, *param):
        delocalise(self, self.x, self.y, self.dim[0])
        fonction_sans_GPS(self, *param)
        localise(self, self.x, self.y, self.dim[0])
    return fonction_avec_GPS
#--------------------------------------------------------------------------------------


##################################################
##    Classe :            class simulation():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui simule un ecosystème
##    Pré-conditions :    largeur et hauteur (px) doivent êtres multiple de 4. entitées disponibles : biche, loup.
##################################################

class simulation():
    """ classe qui simule un ecosystème """
    def __init__(self, animaux = {"biche" : 2}, largeur = 40, hauteur = 40):
        self.root = Tk()
        self.temps = 0
        self.dim = (largeur, hauteur)
        self.populace = animaux
        self.vitesse = 1
        self.extinction = []
        self.interface = dict()
        self.interface["Temps"] = Label(self.root, text="Temps : "+str(self.temps), font="Arial 8", anchor='ne')
        self.interface["Temps"].pack()
        self.interface["Extinction"] = Label(self.root, text="Espèces éteintes : "+str(self.extinction), font="Arial 10", anchor='w')
        self.interface["Extinction"].pack()
        self.interface["Carte"] = Canvas(self.root,width=largeur,height=hauteur, borderwidth=0, background="#E0CDA9", takefocus="1")
        self.interface["Carte"].pack()
        self.interface["Population"] = Label(self.root, text="Population animal : \n"+str(animaux), font="Arial 10", anchor='w')
        self.interface["Population"].pack()
        self.Quitter = False
        self.interface["Quitter"]  = Button(self.root, text="Stopper la simulation", command=self.Quit)
        self.interface["Quitter"].pack()
        self.interface["Vitesse"] = Scale(self.root, orient="horizontal", from_=1, to=10, resolution=1, tickinterval=9, length=100, label="Vitesse")
        self.interface["Vitesse"].pack()
        self.interface["Informations"] = Button(self.root, text="Obtenir des informations sur cet écosystème.", font="Arial 8", command=self.open_informations)
        self.interface["Informations"].pack()
        self.infos = False
        self.faune = dict()
        self.flore = dict()
        self.flore["herbe"] = []
        for i in range(0, largeur*hauteur// (UE*UE)): # one step or grass is 4x4px
            etre_vivant = herbe(self.dim, self.interface["Carte"])
            self.flore["herbe"].append(etre_vivant)
        print(str(largeur*hauteur// (UE*UE))+" éléments en théorie. en pratique : "+str(len(self.flore["herbe"])))
        for animal, nombre in animaux.items():
            if nombre > 0:
                self.faune[animal] = []
                for i in range(0, nombre):
                    etre_vivant = assigneEspece(animal, self.dim, self.interface["Carte"], self.get_random_coords(self.dim[0]), self.get_random_coords(self.dim[1])) # create an animal with the good class
                    self.faune[animal].append(etre_vivant)
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

    def get_random_coords(self, bordure):
        return UE*randint(0, (bordure//UE)-1) + (UE // 2)

    def open_informations(self):
        self.fen_infos = Tk()
        yDefilB = Scrollbar(self.fen_infos, orient='vertical')
        yDefilB.grid(row=0, column=1, sticky='ns')
        xDefilB = Scrollbar(self.fen_infos, orient='horizontal')
        xDefilB.grid(row=1, column=0, sticky='ew')
        selection = StringVar()
        self.interface["Liste"] = Listbox(self.fen_infos, listvariable=selection, xscrollcommand=xDefilB.set, yscrollcommand=yDefilB.set, height="10")
        self.interface["Liste"].grid(row=0, column=0, sticky='nsew')
        xDefilB['command'] = self.interface["Liste"].xview
        yDefilB['command'] = self.interface["Liste"].yview
        self.interface["Quitter infos"] = Button(self.fen_infos, text="Fermer les informations.", command=self.Quit_infos)
        self.interface["Quitter infos"].grid(row=1, column=1, sticky='nsew')
        self.infos = True

    def actualise_infos(self):
        self.interface["Liste"].delete(0, END)
        for nom, espece in self.faune.items():
            for individu in espece:
                self.interface["Liste"].insert(END, nom +" "+ str(individu)[-11:-1])

    def eteindre(self):
        for nom, espece in self.faune.items():
            k = 0;
            while (len(espece) > 0) and (k < len(espece)):
                individu = espece[k]
                if individu.alive:
                    k += 1
                else:
                    self.interface["Carte"].delete(self.faune[nom][k].image) # Erasing of the graphic representation of the animal.
                    delocalise(individu, individu.x, individu.y, individu.dim[0]) # We clear the location of this animal.
                    del individu # We delete the instance of the animal.
                    # print(self.faune[nom][k])
                    del self.faune[nom][k] # We remove this animal of the animals list.
                    self.populace[nom] -= 1 # the population decrease
            if (self.faune[nom] == []) and (not nom in self.extinction):
                self.extinction.append(nom) # A species would become extinct if all animals of this species are missing.

    def recense(self):
        global recensement
        for baby in recensement:
            self.faune[baby.nom].append(baby)
            self.populace[baby.nom] += 1
        recensement = []

    def run(self):
        #self.root.bind("<Escape>",end)
        #self.root.bind("<KeyPress-p>",pause)
        while not self.Quitter:
            self.temps += 1
            self.interface["Temps"]["text"] = "Temps : "+str(self.temps)
            for plantes in self.flore:
                for plante in self.flore[plantes]:
                    if plante.density < 100:
                        plante = plante.grow()
            for animaux in self.faune:
                for individu in self.faune[animaux]:
                    individu = individu.move()
            self.eteindre()
            self.recense()
            if self.infos:
                self.actualise_infos()
            self.interface["Population"]["text"] = "Population animal : \n"+str(self.populace)
            self.interface["Extinction"]["text"] = "Espèces éteintes : "+str(self.extinction)
            self.root.update()
            self.vitesse = self.interface["Vitesse"].get()
            sleep(1 / self.vitesse)
            #fen.after(100, run)
        self.root.destroy()


##################################################
##    Classe :             class vie():
##    Auteur :             Thibault Charmet
##    Docstring :          Classe qui contient toutes les classes simulant la vie.
##################################################

class vie(simulation):
    """ Classe qui contient toutes les classes simulant la vie. """

    ##    Prototype :            def voisins(x, y, GR, largeur, hauteur):
    ##    Auteur :             Thibault Charmet
    ##    Objectif :            trouve les voisins de x,y compris dans un rectangle selon un critère de proximité R
    ##    Pré-conditions :    aucunes
    ##    Retour :            liste des voisins de x, y

    def voisins(x, y, GR, largeur, hauteur):
        lst_voisins = []
        GR = GR*UE # conversion of GR from pixel to elementary pixel (= 4x4px)
        for i in range(-GR,GR, UE):
            for j in range(-GR,GR, UE):
                if (x+i <= largeur-1-(UE//2)) and (y+j <= hauteur-1-(UE//2)) and (x+i >= (UE//2)) and (y+j >= (UE//2)):
                    lst_voisins.append((x+i,y+j))
        return lst_voisins;

##################################################
##    Classe :            class flore():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui contient toutes les classes simulant des animaux
##################################################

class flore(vie):
    """ classe qui contient toutes les classes simulant des plantes """


##################################################
##    Classe :            class herbe(flore):
##    Auteur :             Thibault Charmet
##    Docstring :            class qui simule une herbe
##################################################

class herbe(flore):
    """ classe qui simule l'herbe """
    teintes = {10:"#187B01", 9:"#298C12", 8:"#3A9D23", 7:"#4BAE34", 6:"#5CBF45", 5:"#6DCF56", 4:"#7EDF67", 3:"#8FEF78", 2:"#BFFFAB", 1:"#D8DEAA", 0:"#E0CDA9"}
    ID = 0
    def __init__(self, dim, carte):
        if herbe.ID == 0:
            print("ID réinitialisé chef !")
        if herbe.ID > (dim[0]*dim[1] // (UE*UE) -1):
            print("Attention il n'y a plus de place pour l'herbe ici.")
        self.nom = "herbe"
        self.carte = carte
        self.dim = dim
        self.x = (herbe.ID*4)  % dim[0] +2 # width
        self.y = (herbe.ID*4) // dim[0] *UE +2 # self.x and self.y are positions of the center of the grass entity.
        # print("Je suis une herbe"+str(herbe.ID)+": ("+str(self.x)+","+str(self.y)+")")
        self.density = 100
        self.GR = 1 # grow region : the distance where grass can sow other fields
        self.image = carte.create_rectangle(self.x,self.y, self.x+UE,self.y+UE, fill=herbe.teintes[self.density // 10], width=0)
        localise(self, self.x, self.y, self.dim[0])
        herbe.ID += 1

    def grow(self):
        if self.density < 100:
            total_density = 0
            for coordonnees in vie.voisins(self.x, self.y, self.GR, self.dim[0], self.dim[1]):
                voisin = getInstance(coordonnees, "herbe", self.dim[0])
                total_density += voisin.density
            self.density = min(trunc(self.density + self.density*0.01 + total_density*0.001 + 1), 100)
            #print("total density : "+str(total_density))
            #print("grow => "+str(trunc(self.density*0.01 + total_density*0.001 + 1)))
            if self.density < 0 :
                raise Exception("Density = "+str(self.density))
            self.carte.delete(self.image)
            self.image = self.carte.create_rectangle(self.x,self.y, self.x+UE,self.y+UE, fill=herbe.teintes[self.density // 10], width=0)


##################################################
##    Classe :            class faune():
##    Auteur :             Thibault Charmet
##    Docstring :            classe qui contient toutes les classes simulant des animaux
##################################################

class faune(vie):
    """ classe qui contient toutes les classes simulant des animaux """
    nombre_moyen_petits = {"biche" : (20,(1,2)), "loup" : (10,(1,9))}
    vieillesse = {"biche" : (1300, 1820), "loup" : (1040, 1800)} # en jours
    actif = {"biche" : (1, 2), "loup" : (1, 3)}
    total_hunger = {"biche" : 100, "loup" : 200}
    agilite = {"biche" : (1,2), "loup" : (1,6)}
    age_reproduction = {"biche" : 10, "loup" : 20} # en jours
    state = "walk" # fight, flight, eat, breed, walk / sleep
    alive = True
    age = 0

##    Prototype :            def getLocalDistance(pos, largeur, x, y):
##    Auteur :             Thibault Charmet
##    Retour :            Retourne le distance réelle qui sépare un objet de localisation et un autre objet défini par ses coordonnées.
##    Pré-conditions :    pos in [0,largeur-1*hauteur-1] et x, y in [0, largeur-1][0, hauteur-1]

    def getLocalDistance(pos, largeur, x, y):
        return sqrt((x - (pos // largeur))**2 + (y - (pos % largeur))**2)

##    Prototype :            def getNearest(self, nom, state):
##    Auteur :             Thibault Charmet
##    Retour :            Retourne l'entité la plus proche de soi ayant un nom et un état préscis. Pour prendre n'importe quel état state doit valoir None.
##                        Retourne None si aucune entité correspondant aux critères n'est trouvé.
##    Pré-conditions :    state = None => state ne devient plus une contrainte. nom existant.

    def getNearest(self, nom, state):
        dist, res = None, None
        for pos in range(0, len(localisation)):
            if (dist == None) or (faune.getLocalDistance(pos, self.dim[0], self.x, self.y) < dist):
                for k in range(0, len(localisation[pos])):
                    if (localisation[pos][k].nom == nom) and ((state == None) or (localisation[pos][k].state == state)) and ((localisation[pos][k].x != self.x) or (localisation[pos][k].y != self.y)):
                        dist = faune.getLocalDistance(pos, self.dim[0], self.x, self.y)
                        res = localisation[pos][k]
        return res

    def getValeur(probabilite):
        valeur = probabilite[0]
        if 10*random() <= probabilite[1]:
            valeur += 1
        return valeur

    @GPS
    def moveRandom(self):
        Mouvement = faune.getValeur(self.vitesse)
        xd, yd = randint(-1, 1)*UE * Mouvement, randint(-1, 1)*UE * Mouvement
        self.x = (self.x + xd)% self.dim[0]
        self.y = (self.y + yd)% self.dim[1]
        self.carte.coords(self.image, self.x-self.R, self.y-self.R, self.x+self.R, self.y+self.R)
        self.carte.tag_raise(self.image, getInstance((self.x, self.y), "herbe", self.dim[0]).image )


    def get_xd(self, entity, Mouvement):
        if (entity.x - self.x) >= 0:
            xd = min(Mouvement, entity.x - self.x)
        else:
            xd = max(-Mouvement, entity.x - self.x)
        Mouvement -= abs(xd)
        return (Mouvement, xd)

    def get_yd(self, entity, Mouvement):
        if (entity.y - self.y) >= 0:
            yd = min(Mouvement, entity.y - self.y)
        else:
            yd = max(-Mouvement, entity.y - self.y)
        Mouvement -= abs(yd)
        return (Mouvement, yd)

    @GPS
    def moveToward(self, entity):
        Mouvement = UE * faune.getValeur(self.vitesse)
        if (randint(0,1) == 0):
            (Mouvement, xd) = self.get_xd(entity, Mouvement)
            (Mouvement, yd) = self.get_yd(entity, Mouvement)
        else:
            (Mouvement, yd) = self.get_yd(entity, Mouvement)
            (Mouvement, xd) = self.get_xd(entity, Mouvement)

        # print(str(xd)+","+str(yd))
        self.x = (self.x + xd)% self.dim[0]
        self.y = (self.y + yd)% self.dim[1]
        self.carte.coords(self.image, self.x-self.R, self.y-self.R, self.x+self.R, self.y+self.R)
        self.carte.tag_raise(self.image, getInstance((self.x, self.y), "herbe", self.dim[0]).image)

    def reproduction(self, entity):
        if (entity.y == self.y) and (entity.x == self.x):
            for p in range(0, faune.getValeur(faune.nombre_moyen_petits[self.nom][1])):
                entity.hunger -= faune.nombre_moyen_petits[self.nom][0]
                self.hunger -= faune.nombre_moyen_petits[self.nom][0]
                petit = assigneEspece(self.nom, self.dim, self.carte, self.x, self.y) # create a child of the same class
                petit.hunger = 2*faune.nombre_moyen_petits[self.nom][0]
                global recensement
                recensement.append(petit)
                

##################################################
##    Classe :            class biche(faune):
##    Auteur :             Thibault Charmet
##    Docstring :            class qui simule une biche
##################################################

class biche(faune):
    """ classe qui simule une biche """
    def __init__(self, dim, carte, x, y):
        self.nom = "biche"
        self.R = 2
        self.carte = carte
        self.dim = dim
        self.hunger = self.total_hunger[self.nom]
        self.vitesse = self.agilite[self.nom]
        self.x = x # width
        self.y = y # height
        # print("Je suis une biche: ("+str(self.x)+","+str(self.y)+")")
        self.life = 100
        self.image = carte.create_oval(self.x-self.R,self.y-self.R, self.x+self.R,self.y+self.R, fill="Brown", outline="Green", width="0")
        localise(self, self.x, self.y, self.dim[0])

    def move(self):
        if (self.hunger >= 85) and (self.age >= self.age_reproduction[self.nom]):
            self.state = "breed"
            partenaire = self.getNearest("biche", "breed")
            if partenaire != None:
                self.moveToward(partenaire)
                self.reproduction(partenaire)
            else:
                self.moveRandom()
        else:
            self.state = "walk"
            self.moveRandom()
            # self.state = "eat"
            self.manger() # système de faim/danger
        # print(self.hunger)
        self.age += 1;
        self.hunger -= randint(self.actif[self.nom][0], self.actif[self.nom][1])
        if self.age >= self.vieillesse[self.nom][0]:
            trop_vieux = randint(0, self.vieillesse[self.nom][1] - self.vieillesse[self.nom][0])
            self.alive = (trop_vieux == 0)
        self.alive = self.alive and (self.hunger > 0)

    def manger(self):
        herbe = getInstance((self.x, self.y), "herbe", self.dim[0])
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

class loup(faune):
    """ classe qui simule un loup """
    def __init__(self, dim, carte, x, y):
        self.nom = "loup"
        self.R = 2
        self.carte = carte
        self.dim = dim
        self.hunger = self.total_hunger[self.nom]
        self.vitesse = self.agilite[self.nom]
        self.x = x # width
        self.y = y # height
        # #print("Je suis une loup: ("+str(self.x)+","+str(self.y)+")")
        self.life = 70
        self.image = carte.create_oval(self.x-self.R,self.y-self.R, self.x+self.R,self.y+self.R, fill="Grey", outline="Black", width="0")
        localise(self, self.x, self.y, self.dim[0])

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
                if (self.x == proie.x) and (self.y == proie.y):
                    self.manger(proie)
            else:
                self.moveRandom()
        # print(self.hunger)
        self.age += 1;
        self.hunger -= randint(self.actif[self.nom][0], self.actif[self.nom][1])
        if self.age >= self.vieillesse[self.nom][0]:
            trop_vieux = randint(0, self.vieillesse[self.nom][1] - self.vieillesse[self.nom][0])
            self.alive = (trop_vieux == 0)
        self.alive = self.alive and (self.hunger > 0)


    def manger(self, proie): # liste des proies
        kg = min([self.total_hunger[self.nom]-self.hunger, self.total_hunger[self.nom], proie.hunger]) # faire système de meute / partage ou une viande qui tombe au sol...
        self.hunger += kg
        print("Miam !"+str(self.hunger))
        proie.hunger -= kg
        proie.alive = False



def assigneEspece(nom, dim, carte, x, y):
    if nom == "loup":
        instance = loup(dim, carte, x, y)
    else:
        instance = biche(dim, carte, x, y)
    return instance
        

##    Prototype :            def (de)localise(instance, x, y, largeur):
##    Auteur :             Thibault Charmet
##    Objectif :            actualise localisation pour cette instance
##    Pré-conditions :    largeur*hauteur <= lenght(localisation) et x,y in [largeur, hauteur] et instance existante (non détruite)

def localise(instance, x, y, largeur):
    global localisation
    # print(str(instance)+" : "+str((largeur//UE)*(y-2)//UE+((x-2))//UE)+"("+str((x-2)//UE)+","+str((y-2)//UE)+")"+"("+str(x)+","+str(y)+")")
    localisation[((largeur//UE)*(y-2)//UE+((x-2))//UE)].append(instance)

def delocalise(instance, x, y, largeur):
    global localisation
    # print(((largeur//UE)*(y-2)//UE+((x-2))//UE))
    localisation[((largeur//UE)*(y-2)//UE+((x-2))//UE)].remove(instance)

def getInstance(coords, nomInstance, largeur):
    k, fin = 0, False
    population = list(localisation[((largeur//UE)*(coords[1]-2)//UE+((coords[0]-2))//UE)])
    while (k < len(population)) and not fin:
        fin = (population[k].nom == nomInstance)
        k += 1
    if fin:
        return population[k-1]
    else:
        raise Exception("Instance not found for (x,y)= ("+str(coords[1])+","+str(coords[0])+"). trouvé : "+str(localisation[(largeur-1) * (coords[1]//UE) + (coords[0]//UE)]))

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
    global localisation
    localisation = []
    print(L*H)
    for i in range(0, L*H // (UE*UE)):
        localisation.append([])
    herbe.ID = 0
    window.destroy()
    ecosysteme = simulation(animaux, L, H)
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


animaux = {"biche" : 0, "loup" : 0}
localisation = list()
recensement = list()
window = Tk()
window.title('Ecosystem simulator')
echelles = list()
for animal in animaux:
    echelle = Scale(window, orient="horizontal", from_=0, to=50, resolution=1,tickinterval=25, length=200, label="Nombre de " + animal + " : ")
    echelle.pack()
    echelles.append(echelle)

frame = Canvas(window, width=20, height=20, borderwidth="2", background="#000ddd555", confine="False", scrollregion=(0, 0, 0, 0), xscrollincrement=1)
echelle_largeur = Scale(window, orient="horizontal", from_=20, to=400, resolution=UE, tickinterval=50, length=400, label="Largeur de l'environement :", command=actualise)
echelle_hauteur = Scale(window, orient="horizontal", from_=20, to=400, resolution=UE, tickinterval=50, length=400, label="Hauteur de l'environement :", command=actualise)
echelle_largeur.pack()
echelle_hauteur.pack()
frame.pack()
frame.bind("<Button-1>",prendre)
frame.bind("<Motion>",bouger)

zone_options = Canvas(window, width=80, height=40)
zone_options.pack()
do_you_want_to_lag = StringVar()
check_for_lags = Checkbutton(zone_options, variable=do_you_want_to_lag, command=mode_lags, text='Activer le mode lag ', onvalue='oui', offvalue='non', anchor='sw')
check_for_lags.pack(side = LEFT)
check_for_lags.deselect()

truc = Checkbutton(zone_options, text='truc qui sert à rien', anchor='se')
truc.pack(side = RIGHT)
machin = Checkbutton(zone_options, text='machin qui sert à rien')
machin.pack(side = TOP)

bouton_run = Button(zone_options, text="Lancer", command=lancement, anchor='s')
bouton_run.pack(side = BOTTOM) # side = BOTTOM

message = Label(window, text="")
message.pack()

window.mainloop()

