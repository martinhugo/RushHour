#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Module contenant les fenetres utilisées dans le projet Rush Hour
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QRadioButton, QGroupBox, QDialogButtonBox, QLineEdit, QProgressBar)
from PyQt5.QtCore import Qt
from controller import *


class SettingsDialog(QDialog):
    """ Classe permettant de paramètrer la résolution de la configuration courante. """

    def __init__(self, parent=None):
        """ Params: parent -> le parent de l'objet (géré automatiquement par PyQt)
            Return: self
            Initialisation de la fenetre Paramètre
        """
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        """ Met en forme la fenetre de dialogue, créé l'ensemble des boutons et labels permettant de paramètrer la résolution d'une grille. """


        settings_layout = QVBoxLayout();
        self.nbMoveMax = QLineEdit()

        buttons = QDialogButtonBox();
        #creating OK button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        
        #creating Cancel button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.reject)

        #adding created buttons to the layout
        groupType, groupProblem = self.getRadioButtonLayout()
        settings_layout.addWidget(groupType)
        settings_layout.addWidget(groupProblem)

        settings_layout.addWidget(QLabel("Nombre de mouvements maximum: "))
        settings_layout.addWidget(self.nbMoveMax)
        settings_layout.addWidget(buttons)

        #adding layout to dialog
        self.setLayout(settings_layout);
        self.sizeHint()


    def getRadioButtonLayout(self):
        """ Méthode permettant de  creer l'ensemble des radio buttons nécessaire à la fenetre.
            Return: groupType, groupProblem les GroupBox contenant les boutons radios permettant de choisir le type et le problème (RHC/RHM) de la résolution
        """
        #creating Radio buttons
        self.treeButton = QRadioButton(ResolutionType.TREE_RESOLUTION, self);
        self.linearProgrammingButton = QRadioButton(ResolutionType.LINEAR_PROGRAMMING, self);
        typeLayout = QVBoxLayout()
        typeLayout.addWidget(self.treeButton)
        typeLayout.addWidget(self.linearProgrammingButton)
        groupType = QGroupBox()
        groupType.setLayout(typeLayout)

        self.rhmButton = QRadioButton(ResolutionProblem.RHM, self);
        self.rhcButton = QRadioButton(ResolutionProblem.RHC, self);
        groupProblem = QGroupBox()
        problemLayout = QVBoxLayout()
        problemLayout.addWidget(self.rhmButton)
        problemLayout.addWidget(self.rhcButton)
        groupProblem = QGroupBox()
        groupProblem.setLayout(problemLayout)

        return groupType, groupProblem
       
    def exec_(self):
        """ Affiche la fenetre et lance la boucle evenementielle
            Les changements sont confirmées seulement si le bouton ok est pressée
        """ 
        # If changes was confirmed
        if(super().exec_()):
            
            if self.treeButton.isChecked():
                self.parent().controller.setResolutionType(ResolutionType.TREE_RESOLUTION)
            elif self.linearProgrammingButton.isChecked():
                self.parent().controller.setResolutionType(ResolutionType.LINEAR_PROGRAMMING)

            if self.rhmButton.isChecked():
                self.parent().controller.setResolutionProblem(ResolutionProblem.RHM)
            elif self.rhcButton.isChecked():
                self.parent().controller.setResolutionProblem(ResolutionProblem.RHC)

            try:
                nbMoveMax = self.nbMoveMax.text()
                self.parent().controller.setNbMoveMax(int(nbMoveMax))
            except ValueError:
                print(nbMoveMax + " ne peut être converti en entier.")




