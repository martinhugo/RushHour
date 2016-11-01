# -*- coding: utf-8 -*-

from vehicule import *
import math
""" Contient l'ensemble des classes et types nécessaire à la representation d'une configuration dans le jeu RushHour. """

class Configuration:

    def __init__(self, vehicules = [], nbCoupMax = 0):
        self.vehicules = list(vehicules)
        self.constructConfiguration()
        self.nbCoupMax = nbCoupMax

    def getConfiguration(self):
        """Retourne self.configuration """
        return self.configuration
        
    def setNbCoupMax(self, value):
        """ Modifie la valeur de self.nbCcoupMax """
        self.nbCoupMax = value

    def setVehicules(self, vehicules):
        """ Modifie la valeur de self.nbCoupMax """
        self.vehicules = list(vehicules)

    def getVehicules(self):
        """ Retourne self.vehicules """
        return self.vehicules 

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
        # Creer une liste de 36 mots. Parcourir uniquement cette liste et deux dictionnaires vides voitures camions.
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






if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
    print(conf)
    







