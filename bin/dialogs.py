#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Module containing the Dialog boxes for the GooDoc Application.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QLineEdit)
from controller import *


class SettingsDialog(QDialog):
    """ Inherits: QDialog
        This class defines a dialog box.
        This dialog box is composed of two radio buttons, which let the user choose the order of methods and classes in the generated documentation.
    """

    def __init__(self, parent=None):
        """ Constructor
            Params: parent -> the object's parent
            Return: self
            The object is initialized with the super-constructror, the GUI with the initUI method.
        """
        super().__init__(parent)
        self.initUI()


    def initUI(self):
        """ Object method
            Params: None
            Return: None
            This method sets the dialog box's layout.
            The Dialog box conatains two radio buttons and OK/Cancel buttons.
            sizeHint() sets the box to an ideal size.
        """

        #creating layout
        settings_layout = QVBoxLayout();

        #creating Radio buttons
        self.treeButton = QRadioButton(ResolutionType.TREE_RESOLUTION, self);
        self.linearProgrammingButton = QRadioButton(ResolutionType.LINEAR_PROGRAMMING, self);

        self.nbMoveMax = QLineEdit()

        #creating the buttons
        buttons = QDialogButtonBox();

        #creating OK button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        
        #creating Cancel button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.reject)

        #adding created buttons to the layout
        settings_layout.addWidget(self.treeButton)
        settings_layout.addWidget(self.linearProgrammingButton)
        settings_layout.addWidget(QLabel("Nombre de mouvements maximum: "))
        settings_layout.addWidget(self.nbMoveMax)
        settings_layout.addWidget(buttons)

        #adding layout to dialog
        self.setLayout(settings_layout);
        self.sizeHint()



    def exec_(self):
        """ Object method.
            Params: None.
            Return: None.
            This method displays the window and launches its event loop. 
            Changes are commited when the OK button is pressed.
        """ 
        # If changes was confirmed
        if(super().exec_()):
            
            if self.treeButton.isChecked():
                self.parent().controller.setResolutionType(ResolutionType.TREE_RESOLUTION)
            elif self.linearProgrammingButton.isChecked():
                self.parent().controller.setResolutionType(ResolutionType.LINEAR_PROGRAMMING)

            try:
                nbMoveMax = self.nbMoveMax.text()
                self.parent().controller.setNbMoveMax(int(nbMoveMax))
            except ValueError:
                print(nbMoveMax + " ne peut être converti en entier.")

