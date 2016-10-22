#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""

from configuration import *

class ConfigController:
    """ Permet toutes intéractions avec la configuration.
        Cette classe reçoit les informations de l'application.
        En cas de demande de résolution, le controleur demande la résolution de la grille.
        Une fois le fichier de résolution produit, celui-ci créé l'ensemble des configurations à afficher et les envoi au modèle qui les affiche suivant les ordres de l'utilisateur.
    """

    def __init__(self, window):
        self.mainWindow = window
        self.resolutionType = "RAPTOR JESUS THE ONE WHO LOVES EVERYTHING"

    def createInitialConfiguration(self, path):
        self.configuration = Configuration.readFile(path)
        self.mainWindow.displayConfiguration(self.configuration)

    def solve(self, solvingType):
        pass

    def createConfigurations(self, path="temp.cfg"):
        pass

    def setResolutionType(self, resolutionType):
        self.resolutionType = resolutionType
        print(self.resolutionType)