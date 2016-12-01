#/usr/bin/python3
# -*- coding:utf-8 -*-



import sys

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel)

from vehicule import *
from configuration import *

class ConfigDisplayer(QWidget): 
    """ QWidget permettant d'afficher une configuration du jeu Rush Hour """
    
    def __init__(self, configuration, colors):
        """ Initialise le widget d'affichage de configuration 
                Params: configuration: la configuration a afficher
                colors: la couleur à affecter à chaque élément de la configuration
        """
        super().__init__()
        self.grid = QGridLayout()
        self.displayConfiguration(configuration, colors)

    def displayConfiguration(self, configuration, colors):
        """ Affiche la configuration avec les colors passées en paramètres 
            Params: configuration: la configuration a afficher
                    colors: la couleur à affecter à chaque élément de la configuration
        """
        posEmpty = list(range(36))
        # pour chaque véhicule
        for vehicule in configuration.getVehicules():
            marqueur = vehicule.getMarqueur()
            size = vehicule.getTypeVehicule()
            orientation = vehicule.getOrientation()
            # calcul des positions vides
            posEmpty = [pos for pos in posEmpty if pos not in [occupatePos for occupatePos in range(marqueur, marqueur + size*orientation, orientation)]]
            i, j = marqueur//6, marqueur%6

            # affichage des véhicules
            label = QLabel(str(vehicule))
            label.setStyleSheet("background-color:rgb" + str(colors[str(vehicule)]) + ";qproperty-alignment: AlignCenter;border: 1px solid;")
            if orientation == Orientation.BAS:
                self.grid.addWidget(label, i, j, size, 1)
            else:
                self.grid.addWidget(label, i, j, 1, size)

        # affichage des positions vides
        for marqueur in posEmpty:
            i, j = marqueur//6, marqueur%6
            label = QLabel()
            label.setStyleSheet("background-color:rgb" + str(colors["0"]) + ";qproperty-alignment: AlignCenter;border: 1px solid;")
            self.grid.addWidget(label, i, j)

        self.setLayout(self.grid)

