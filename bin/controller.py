#/usr/bin/python3
# -*- coding:utf-8 -*-

import random
import copy
from PyQt5.QtCore import (QThread)

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

    def __init__(self, window, nbMoveMax = 50, colors={}):
        """ Initialise l'ensemble des paramètres nécessaires aux interactions entre l'IHM et les solveurs
            Params: window -> fenêtre principale de l'application
                    nbMoveMax -> nombre de mouvement maximum autorisé pour l'application
                    colors -> couleur d'affichage de chaque élément des configurations
        """
        self.mainWindow = window
        self.resolutionType = ResolutionType.TREE_RESOLUTION
        self.resolutionProblem = ResolutionProblem.RHM
        self.nbMoveMax = nbMoveMax
        self.colors = colors

        self.nextConfigs = []
        self.predConfigs = []


    def setConfiguration(self, path, initColors = True):
        """ Modifie la configuration du controller et son affichage
            Les couleurs d'affichage des différents véhicules peuvent ou non être modifié.
            params : path -> chemin ou se trouve la nouvelle configuration a afficher
        """
        self.configuration = Configuration.readFile(path)

        if initColors == True:
            self.initColors()

        self.mainWindow.setCentralWidget(ConfigDisplayer(self.configuration, self.colors))

    def setResolutionType(self, resolutionType):
        """ Modifie la valeur de self.resolutionType a resolutionType """
        self.resolutionType = resolutionType

    def setResolutionProblem(self, resolutionProblem):
        """ Modifie la valeur de self.resolutionProblem a resolutionProblem"""
        self.resolutionProblem = resolutionProblem

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
        """ Résoud la configuration selon le type de résolution et le problème (RHM/RHC) demandé.
            Un QThread est créé permettant de ne pas bloquer l'application, le timer est lancé dans l'application principale.
        """
        if self.resolutionType == ResolutionType.LINEAR_PROGRAMMING:
            self.solver = Solver(LPSolver(self.configuration, self.resolutionProblem, self.nbMoveMax))
        else:
            self.solver = Solver(Dijkstra(self.configuration, self.resolutionProblem, self.nbMoveMax))

        self.solver.start()
        self.mainWindow.startTimer()


    def endSolving(self):
        """ Termine la résolution selon les instructions de la fenetre principale à la suite de l'arrêt du timer
            La terminaison du Thread est demandé.
        """
        self.solver.terminate()
        self.nextConfigs = self.solver.configs
        if (len(self.nextConfigs) == 0):
            self.mainWindow.statusBar().showMessage("Resolution Failed - Time out")
        

    


    def displayNextConfig(self):
        """ Demande l'affichage par l'application de la configuration suivante dans l'ensemble des configurations solutions """
        print(len(self.nextConfigs), self.nextConfigs)
        if(len(self.nextConfigs) != 0):
            config = self.nextConfigs.pop()
            self.predConfigs.append(config)
            self.mainWindow.setCentralWidget(ConfigDisplayer(config, self.colors))


    def displayPredConfig(self):
        """ Demande l'affichage par l'application de la configuration précédente dans l'ensemble des configurations solutions"""
        if(len(self.predConfigs) != 0):
            config = self.predConfigs.pop()
            self.nextConfigs.append(config)
            self.mainWindow.setCentralWidget(ConfigDisplayer(config, self.colors))
        


class Solver(QThread):
    """ Thread effectuant la résolution de la configuration.
        Recoit un objet solveur et demande a ce solveur de s'executer
    """
    def __init__(self, solver):
        QThread.__init__(self)
        self.solver = solver
        self.configs = []

    def run(self):
        """ Execution de la résolution """
        print("début de la recherche de la solution")
        self.configs = self.solver.solve()
        print("fin de la recherche de la solution")
        self.terminate


    

class ResolutionType:
    """ Enumération contenant les informations sur les types de résolutions """
    LINEAR_PROGRAMMING = "Programmation linéaire"
    TREE_RESOLUTION = "Résolution arborescente"

class ResolutionProblem:
    """ Enumération contenant les informations sur les type de problème à résoudre """
    RHC = "RHC"
    RHM = "RHM"