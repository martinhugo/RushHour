#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""
import random
import copy


from configuration import *
from displayer import *
from lpsolver import *
from dijkstra import *

class ConfigController:
    """ Permet toutes intéractions avec la configuration.
        Cette classe reçoit les informations de l'application.
        En cas de demande de résolution, le controleur demande la résolution de la grille.
        Une fois le fichier de résolution produit, celui-ci créé l'ensemble des configurations à afficher et les envoi au modèle qui les affiche suivant les ordres de l'utilisateur.
    """

    def __init__(self, window, nbMoveMax = 0, colors={}):
        self.mainWindow = window
        self.resolutionType = ResolutionType.LINEAR_PROGRAMMING
        self.nbMoveMax = nbMoveMax
        self.colors = colors

        self.nextConfigs = []
        self.predConfigs = []


    def setConfiguration(self, path, initColors = True):
        """ Modifie la configuration du controller.
            Un nouveau widget d'affichage est alors créé pour remplacer le précédent (temporaire, le mieux serait de le mettre simplement à jour).
            Les couleurs d'affichage des différents véhicules peuvent ou non être modifié.
        """
        self.configuration = Configuration.readFile(path)

        if initColors == True:
            self.initColors()

        self.mainWindow.setCentralWidget(ConfigDisplayer(self.configuration, self.colors))

    def setResolutionType(self, resolutionType):
        """ Modifie la valeur de self.resolutionType a resolutionType """
        self.resolutionType = resolutionType

    def setNbMoveMax(self, nbMoveMax):
        """ Modifie la valeur de nbMoveMax a nbMoveMax """
        self.nbMoveMax = nbMoveMax

    def initColors(self):
        """ Modifie l'attribut self.colors.
            Affecte aléatoirement une couleur à tous les véhicules. Le véhicule "g" est mis à rouge. L'absence de véhicule est en noir.
        """
        self.colors = {}

        for vehicule in self.configuration.getVehicules():
            self.colors[str(vehicule)] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.colors["g"] = (random.randint(200, 255), random.randint(0, 50), random.randint(0,50))
        self.colors["0"] = (255, 255, 255)

    def solve(self):
        """ Résoud la configuration selon le type de résolution demandée """
        if self.resolutionType == ResolutionType.LINEAR_PROGRAMMING:
            solver = LPSolver(self.configuration, self.nbMoveMax)
        else:
            solver = Dijkstra(self.configuration, self.nbMoveMax)

        self.nextConfigs = solver.solve()
        print(len(self.nextConfigs))
    


    def displayNextConfig(self):
        """ Demande l'affichage par l'application de la configuration suivante """
        print(len(self.nextConfigs), self.nextConfigs)
        if(len(self.nextConfigs) != 0):
            config = self.nextConfigs.pop()
            self.predConfigs.append(config)
            self.mainWindow.setCentralWidget(ConfigDisplayer(config, self.colors))


    def displayPredConfig(self):
        """ Demande l'affichage par l'application de la configuration précédente """
        if(len(self.predConfigs) != 0):
            config = self.predConfigs.pop()
            self.nextConfigs.append(config)
            self.mainWindow.setCentralWidget(ConfigDisplayer(config, self.colors))
        





    

class ResolutionType:
    LINEAR_PROGRAMMING = "Programmation linéaire"
    TREE_RESOLUTION = "Résolution arborescente"