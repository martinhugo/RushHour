# -*- coding: utf-8 -*-

from vehicule import *
import math
from listTools import *
""" Contient l'ensemble des classes et types nécessaire à la representation d'une configuration dans le jeu RushHour. """

class Configuration:

    def __init__(self, vehicules = [], nbCoupMax = 0):
        self.vehicules = list(vehicules)
        self.constructConfiguration()
        self.nbCoupMax = nbCoupMax

    def getConfiguration(self):
        """Retourne self.configuration """
        return self.configuration

    def setConfiguration(self, config):
        """ utilisé dans le cas de Dijkstra pour la création des noeuds"""
        self.configuration = config
        
    def setNbCoupMax(self, value):
        """ Modifie la valeur de self.nbCoupMax """
        self.nbCoupMax = value

    def getNbCoupMax(self):
        return self.nbCoupMax

    def setVehicules(self, vehicules):
        """ Modifie la valeur de self.vehicules """
        self.vehicules = list(vehicules)

    def getVehicules(self):
        """ Retourne self.vehicules """
        return self.vehicules 

    def getPositionsVehicles(self):
        """ retourne un dictionnaire associant la liste de toutes les cases occupées par un véhicule"""
        return self.positionsVehicules

    def constructConfiguration(self):
        """ Construit la configuration de base, initialise l'attribut configuration en fonction de l'attribut véhicule.
            Cette méthode permet de creer un tableau de taille 36 représentant la grille 
        """
        configuration = [0 for i in range(36)]
        for vehicule in self.vehicules:
            marqueur = vehicule.getMarqueur()
            orientation = vehicule.getOrientation()
            typeVehicule = vehicule.getTypeVehicule()
            for i in range(marqueur, marqueur+ (orientation*typeVehicule), orientation):
                configuration[i] = vehicule

        self.configuration = configuration

    @staticmethod
    def readFile(path):
        """ Lit le fichier passé en paramètre et créé la liste de véhicules présents dans le fichier de configuration
            Retourne un nouvel objet configuration avec les véhicules trouvés dans le fichier.
            params: path (str) -> le chemin du fichier de configuration 
        """
        with open(path, "r") as file:
            content = file.read()


        content = [word for line in content.split("\n") for word in line.split(" ") if len(word)>0]
        line, col = content[:2]
        content = content[2:]
        vehicules = Configuration.constructVehicules(content)
        return Configuration(vehicules)

    @staticmethod
    def constructVehicules(content):
        # Idée:
        # Crée une liste de 36 mots. Parcourir uniquement cette liste et deux dictionnaires vides voitures camions.
        #
        # Si on rencontre un mot de taille > 2, on vérifie son type et on l'ajoute à l'un des deux dictionnaires voitures camions à son indice numérotés
        # Si il est ajouté pour la première fois on ajoute son indice en tant que marqueur
        # Si il est rencontré pour une seconde fois on verifie si les deux marqueurs sont multiples de 6, si oui son orientation est bas sinon droite
        # on construit la liste finale en fusionnant les deux dictionnaires dans une liste et en faisant abstraction des clés.
        # Deux parcours, un pour creer le tableau, l'autre pour creer les dictionnaires. Peut être réduit en un parcourt, sera fait ultérieurement. (pour l'instant plus clair dans ma tête en un parcourt)
        #
        # Si on rencontre la lettre 'g', on créé une voiture selon la même méthode.
        # Première version: Peut comporter bugs et incohérences.

        voitures, camions  = {}, {}

        for i in range(len(content)):
            word = content[i]
            if len(word)>1 or word[0] == "g":
                
                goodDico = voitures
                typeVehicule = TypeVehicule.VOITURE

                if word[0] == "g":
                    key = word[0]
                else:
                    key = word[1]
                    if word[0] == "t":
                        goodDico = camions
                        typeVehicule = TypeVehicule.CAMION

                if key not in goodDico.keys():
                    goodDico[key] = Vehicule(word, i, typeVehicule, Orientation.DROITE)

                elif (abs(goodDico[key].getMarqueur() - i) == 6):
                        goodDico[key].setOrientation(Orientation.BAS)

        result = list(voitures.values())
        result.extend(list(camions.values()))
        return result

    def initPositionsVehicules(self):
        """ Pour chaque véhicule et pour chaque case retourne toutes les cases occupées

            Paramètres : 
                    - une configuration des voitures
        """
        self.positionsVehicules = {}

        for vehicle in self.getVehicules():
            currentList = []
            marqueur = vehicle.getMarqueur()
            # pour chaque positions de la grille
            indexMax = marqueur + vehicle.getOrientation() * (vehicle.getTypeVehicule()-1)
            # si le véhicule ne sort pas de la grille
            if (indexMax <36):
                self.positionsVehicules[vehicle.getIdVehicule()] = self.positions2Points[marqueur][indexMax]


##########################################################################################################################################
#                                                                                                                                        #
#                                                       POUR POSITIONS POSSIBLES                                                         #
#                                                                                                                                        #
##########################################################################################################################################

    def allPossiblePositionsForAVehicle(self, vehicle):
        """ retourne la liste, pour un véhicule, de toutes les cases que ce véhicule peut occuper, sans tenir compte des autres véhicules"""

        marqueur = vehicle.getMarqueur()
        orientation = vehicle.getOrientation()
        length = vehicle.getTypeVehicule()

        debut = 0
        if(orientation == 6):
            debut = marqueur%6
        else:
            debut = marqueur-marqueur%6
        fin = debut + orientation*(6-length)

        return [i for i in range(debut, fin+1, orientation)]


    def allPossiblePositionsForAllVehicles(self):
        """ retourne un dictionnaire associant à un véhicule la liste de toutes les cases que ce véhicule peut occuper, sans tenir compte des autres véhicules"""

        vehicles = self.getVehicules()
        possibleMoves = {}
        for vehicle in vehicles:
            possibleMoves[vehicle.getIdVehicule()] = self.allPossiblePositionsForAVehicle(vehicle)
        return possibleMoves


    def possiblePositionForAVehicle(self, vehicle):
        """ Retourne la liste de toutes les positions effectivement possibles d'un véhicule """

        listPositionVehicle = self.removeCasesEnCommum(vehicle)
        listPositionVehicle.remove(vehicle.getMarqueur()) # enlever position occupée par curseur
        listPositionVehicle = self.removeCasesImpossibles(vehicle, listPositionVehicle)
        if(len(listPositionVehicle) == 0):
            listPositionVehicle = []
        return listPositionVehicle

    def removeCasesEnCommum(self, vehicle, listPositionVehicle = None):
        """ retire toutes les cases en commun entre un véhicule et tous les autres, retourne la liste des mouvements possibles sans ces cases"""

        orientation = vehicle.getOrientation()
        length = vehicle.getTypeVehicule()

        if(listPositionVehicle == None):
            listPositionVehicle = self.allPossiblePositionsForAVehicle(vehicle)

        listPositionOtherVehicles = self.unionCasesOtherVehicles(vehicle) 
        
        for value in range(length): # pour chaque case occupée par le vehicule
            listToRemove = listPositionOtherVehicles
            listToRemove = ListTools.intersection(ListTools.addToList(listPositionVehicle, value * orientation), listToRemove)
            for element in listToRemove:
                listPositionVehicle.remove(element - value * orientation) # on enleve tous les éléments en commun
        return listPositionVehicle

    def unionCasesOtherVehicles(self, vehicle):
        """ retourne la liste de toutes les cases occupées par les véhicules autres que le véhicule passé en paramètre """

        listPositionOtherVehicles = []
        for otherVehicle in self.getVehicules(): # pour tous les autres véhicules
            if otherVehicle != vehicle:
                # liste de toutes les cases occupées par tous les autres véhicules
                listPositionOtherVehicles = ListTools.union( listPositionOtherVehicles, self.getPositionsVehicles()[otherVehicle.getIdVehicule()])
        return listPositionOtherVehicles


    def removeCasesImpossibles(self, vehicle, listPositionVehicle = None):
        """ retire toutes les cases qui nécessitent de sauter par dessus un véhicule """

        marqueur = vehicle.getMarqueur()
        orientation = vehicle.getOrientation()

        if(listPositionVehicle == None):
            listPositionVehicle = self.allPossiblePositionsForAVehicle(vehicle)

        listToRemove = []
        listPositionOtherVehicles = self.unionCasesOtherVehicles(vehicle) 

        for element in listPositionVehicle:
            for value in listPositionOtherVehicles:
                if( (orientation == 1 and element//6 == value //6) or (orientation == 6 and element%6 == value%6) ): # si les cases sont alignées
                    if( (marqueur > value and element < value) or (marqueur < value and element > value) ): # si la case a nécessité un saut par dessus un véhicule
                        listToRemove.append(element)
        listToRemove = ListTools.unique(listToRemove)

        for element in listToRemove:
            listPositionVehicle.remove(element) # on enleve tous les éléments en commun
        return listPositionVehicle

    def possiblePositionForAllVehicle(self):
        """ retourne un dictionnaire associant la liste de tous les déplacements effectivement possibles pour un véhicule"""

        dicoPositions = {}
        for vehicle in self.getVehicules():
            positionsPossibles = self.possiblePositionForAVehicle(vehicle)
            if positionsPossibles != []:
                dicoPositions[vehicle] = positionsPossibles
        return dicoPositions

    def getPossiblePosition(self):
        """ retourne l'ensemble des positions possibles pour tous les véhicules"""
        self.initPositions2Points()
        self.initPositionsVehicules()
        return self.possiblePositionForAllVehicle()

    def initPositions2Points(self):
        """ Défini la matrice p[][] qui contient pour tout i,j l'ensemble des positions entre ces deux marqueurs.
            Si les cases ne sont pas alignées verticalement ou horizontalement, le tableau renverra une liste vide pour la case correspondante
        """
        self.positions2Points = []
        for i in range(36):
            currentList = []
            for j in range(36):
                positions = []
                step = 0
                # si les 2 points sont alignés horizontalement
                if(i//6 == j//6):
                    step = 1

                # si les deux points sont alignés verticalement
                elif(i%6 == j%6):
                    step = 6

                # pour parcourir dans l'autre sens si j est avant i
                coef = 1 if i<=j else -1

                # si les deux points sont alignés verticalement ou horizontalement
                if(step !=0):
                    for k in range(i, j + (1 * coef), step * coef):
                        positions.append(k) # on ajoute chaque point compris entre i et j

                currentList.append(positions)
            self.positions2Points.append(currentList)

##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################

    def __str__(self):
        """ Retourne la chaine de caractère associé à la configuration.
            Permet l'affichage de la grille.
            Cette méthode sert surtout au débug
        """
        i = 1
        content = ""
        for el in self.configuration:
            content += str(el) + "\t"
            if(i%6 == 0): 
                content += "\n"
            i += 1

        return content

    def __repr__(self):
        """ Cf __str__ """
        return str(self)


#if __name__ == "__main__":
conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
print(conf)
print(conf.getPossiblePosition())
    







