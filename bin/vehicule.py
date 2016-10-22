# -*- coding: utf-8 -*-


""" Contient l'ensemble des classes et types nécessaire à la representation des véhicules dans le jeu RushHour. """

class Vehicule:

    def __init__(self, marqueur, typeVehicule, orientation):
        """ Un véhicule est réprésenté par un marqueur sur la grille, un type de véhicule et son orientation """
        self.marqueur = marqueur
        self.typeVehicule = typeVehicule
        self.orientation = orientation

    def getMarqueur(self):
        """ Retourne le marqueur du véhicule (position en haut à droite sur la grille [0, 36]) """
        return self.marqueur

    def getTypeVehicule(self):
        """ Retourne le type du véhicule (VOITURE: 2, CAMION: 3) """
        return self.typeVehicule

    def getOrientation(self):
        """ Retourne l'orientation du véhicule (DROITE: 1, BAS: 6) """
        return self.orientation

    def setOrientation(self, orientation):
        """ Modifie l'orientation du véhicule """
        self.orientation = orientation 

    def __str__(self):
        return str((self.marqueur, self.typeVehicule, self.orientation))

    def __repr__(self):
        return str(self)
        
class TypeVehicule:
    """ Répresente le type du véhicule considéré """
    VOITURE = 2
    CAMION = 3

class Orientation:
    """ Répresente l'orientation du véhicule considéré """
    DROITE = 1
    BAS = 6


