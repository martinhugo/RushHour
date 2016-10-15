# -*- coding: utf-8 -*-

from vehicule import *
""" Contient l'ensemble des classes et types nécessaire à la representation d'une configuration dans le jeu RushHour. """

class Configuration:

    def __init__(self, vehicules = [], nbCoupMax = 0):
        self.vehicules = list(vehicules)
        self.nbCoupMax = nbCoupMax

    def setNbCoupMax(self, value):
        """ Modifie la valeur de self.nbCcoupMax """
        self.nbCoupMax = value

    def setVehicules(self, vehicules):
        """ Modifie la valeur de self.nbCoupMax """
        self.vehicules = list(vehicules)

    def getVehicules(self):
        """ Retourne self.vehicules """
        return self.vehicules 

    @staticmethod
    def lireFichier(path):
        with open(path, "r") as file:
            content = file.read()

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

        content = [word for line in content.split("\n") for word in line.split(" ") if len(word)>0]
        print(content)
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
                    goodDico[key] = Vehicule(i, typeVehicule, Orientation.DROITE)

                elif (goodDico[key].getMarqueur() / i) == 6:
                    goodDico[key].setOrientation(Orientation.BAS)


        result = list(voitures.values())
        result.extend(list(camions.values()))
        
        return Configuration(result)


if __name__ == "__main__":
    conf = Configuration.lireFichier("../puzzles/débutant/jam1.txt")
    for vehicule in conf.getVehicules():
        print(vehicule)
    print("Nb Vehicules: ", len(conf.getVehicules()))








