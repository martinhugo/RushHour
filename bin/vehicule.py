# -*- coding: utf-8 -*-


""" Contient l'ensemble des classes et types nécessaire à la representation des véhicules dans le jeu RushHour. """

class Vehicule:

    def __init__(self, identifiant, marqueur, typeVehicule, orientation):
        """ Un véhicule est réprésenté par un marqueur sur la grille, un type de véhicule et son orientation """
        self.idVehicule = identifiant
        self.marqueur = marqueur
        self.typeVehicule = typeVehicule
        self.orientation = orientation

    def getIdVehicule(self):
        """ Retourne self.idVehicule """
        return self.idVehicule

    def getMarqueur(self):
        """ Retourne le marqueur du véhicule (position en haut à droite sur la grille [0, 36]) """
        return self.marqueur

    def setMarqueur(self, marqueur):
        """ utilisé pour la création d'un noeud dans le cas de Dijkstra"""
        self.marqueur = marqueur

    def getTypeVehicule(self):
        """ Retourne le type du véhicule (VOITURE: 2, CAMION: 3) """
        return self.typeVehicule

    def getOrientation(self):
        """ Retourne l'orientation du véhicule (DROITE: 1, BAS: 6) """
        return self.orientation

    def setOrientation(self, orientation):
        """ Modifie l'orientation du véhicule """
        self.orientation = orientation 

    def __repr__(self):
        return self.idVehicule
        
class TypeVehicule:
    """ Répresente le type du véhicule considéré """
    VOITURE = 2
    CAMION = 3

class Orientation:
    """ Répresente l'orientation du véhicule considéré """
    DROITE = 1
    BAS = 6


