# -*- coding: utf-8 -*-

from vehicule import *
""" Contient l'ensemble des classes et types nécessaire à la representation d'une configuration dans le jeu RushHour. """

class Configuration:

    def __init__(self, vehicules = [], nbCoupMax = 0):
        self.vehicules = list(vehicules)
        self.nbCoupMax = nbCoupMax

    def setNbCoupMax(value):
        """ Modifie la valeur de self.nbCcoupMax """
        self.nbCoupMax = value

    def setVehicules(vehicules):
        """ Modifie la valeur de self.nbCoupMax """
        self.vehicules = list(vehicules)

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
        content = [word for word in content.split([" ", "\n"])]
        voitures, camions  = {}, {}

        for i, word in range(len(content)), content:
            if len(word)>2 or word[0] == "g":
                
                key = word[1]
                goodDico = voitures
                typeVehicule = TypeVehicule.VOITURE

                if word[0] == "t": 
                    goodDico = camions
                    typeVehicule = TypeVehicule.CAMION
                elif word[0] == "g":
                    key = word[0]


                if key not in goodDico.keys():
                    goodDico[key] = Vehicule(i, typeVehicule, Orientation.DROITE)

                else if (goodDico[key].getMarqueur() / i) == 6:
                    goodDico[key].setOrientation(Orientation.BAS)

        result = list(voitures.values())
        result.extend(list(camions.values()))
        
        self.vehicules = result











