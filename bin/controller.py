#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""
import random
import copy
from PyQt5.QtCore import (QThread, QObject)


from configuration import *
from displayer import *
from lpsolver import *
from dijkstra import *

class ConfigController(QObject):
    """ Permet toutes intéractions avec la configuration.
        Cette classe reçoit les informations de l'application.
        En cas de demande de résolution, le controleur demande la résolution de la grille.
        Une fois le fichier de résolution produit, celui-ci créé l'ensemble des configurations à afficher et les envoi au modèle qui les affiche suivant les ordres de l'utilisateur.
    """

    def __init__(self, window, nbMoveMax = 50, colors={}):
        super().__init__()
        self.mainWindow = window
        self.resolutionType = ResolutionType.TREE_RESOLUTION
        self.resolutionProblem = ResolutionProblem.RHM
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
        """ Résoud la configuration selon le type de résolution demandée """

        if self.resolutionType == ResolutionType.LINEAR_PROGRAMMING:
            self.solver = Solver(LPSolver(self.configuration, self.resolutionProblem, self.nbMoveMax))
        else:
            self.solver = Solver(Dijkstra(self.configuration, self.resolutionProblem, self.nbMoveMax))

        # self.connect(self.get_thread, SIGNAL("finished()"), self.done)  -> à ajuster au code après
        #self.moveToThread(self.solver)
        self.solver.start()

        self.mainWindow.startTimer()


    def endSolving(self):
        """ Termine la résolution selon les instructions de la fenetre principale """
        self.solver.terminate()
        self.nextConfigs = self.solver.configs
        if (len(self.nextConfigs) == 0):
            self.mainWindow.statusBar().showMessage("Resolution Failed - Time out")
        

    


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
        


class Solver(QThread):

    def __init__(self, solver):
        QThread.__init__(self)
        self.solver = solver
        self.configs = []

    def run(self):
        print("début de la recherche de la solution")
        self.configs = self.solver.solve()
        print("fin de la recherche de la solution")
        self.terminate


    

class ResolutionType:
    LINEAR_PROGRAMMING = "Programmation linéaire"
    TREE_RESOLUTION = "Résolution arborescente"

class ResolutionProblem:
    RHC = "RHC"
    RHM = "RHM"