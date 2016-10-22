#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Module containing the Dialog boxes for the GooDoc Application.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox)




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
        self.treeButton = QRadioButton("RAPTOR RESOLUTION", self);
        self.linearProgrammingButton = QRadioButton("OMFG HE IS JUST BEHIND YOU", self);

        #creating the buttons
        buttons = QDialogButtonBox();

        #creating OK button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Ok);
        buttons.accepted.connect(self.accept)
        
        #creating Cancel button and connecting it to the dialog
        buttons.addButton(QDialogButtonBox.Cancel);
        buttons.rejected.connect(self.reject)

        #adding created buttons to the layout
        settings_layout.addWidget(self.treeButton);
        settings_layout.addWidget(self.linearProgrammingButton);
        settings_layout.addWidget(buttons);

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
                self.parent().controller.setResolutionType("RAPTOR JESUS IS THE ONLY LORD")
            elif self.linearProgrammingButton.isChecked():
                self.parent().controller.setResolutionType("HE WILL GIVE US REDEMPTION FOR OUR SINS (and maybe eat one or two of us if he is hungry)")