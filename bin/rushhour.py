#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""

import sys
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QDialog, QFileDialog, QToolBar, QVBoxLayout, QLabel, QHBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap

import controller
from dialogs import *

# Images
ADD_FILES_ICON = "../img/addFiles.png"
START_ICON = "../img/start.png"
SETTINGS_ICON = "../img/settings.png"

MUR_PARKING = "../img/MurParking.png"
PARKING = "../img/parkingBase.png"
VOITURE = "../img/voiture.png"
VOITURE_A_SORTIR = "../img/voitureASortir.png"
CAMION = "../img/camion.png"

# width and height
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

IMAGE_SIZE_MUR_PARKING = 500
MARGIN_HEIGHT_MUR_PARKING = (WINDOW_HEIGHT - IMAGE_SIZE_MUR_PARKING) / 2
MARGIN_WIDTH_MUR_PARKING = (WINDOW_WIDTH - IMAGE_SIZE_MUR_PARKING) / 2

IMAGE_SIZE_PARKING = 464
MARGIN_HEIGHT_PARKING = (WINDOW_HEIGHT - IMAGE_SIZE_PARKING) / 2
MARGIN_WIDTH_PARKING = (WINDOW_WIDTH - IMAGE_SIZE_PARKING) / 2

SIZE = 6

# ToolTip
ADD_FILES_TIP = "Add files"
START_TIP = "Start generation"
SETTINGS_TIP = "Settings"

WINDOW_TITLE = "RUSH HOUR"

class Window (QMainWindow):
    """ This class is the main class of the application.
        Inherits: QMainWindow
    """

    def __init__(self):
        """ This method initialize the grid and set the toolbar
            Params: None
            Return: None
        """
        super().__init__()
        self.initScreen()
        self.controller = controller.ConfigController(self)


    def displayConfiguration(self, configuration):
        print(configuration)

    def initScreen(self):
        """ This method sets up the documentation screen.
            A <INSERT NAME> is created and set as the central widget.
            Params: None
            Return: None
        """
        self.createToolBar()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100,100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.initImages()
        self.show()


    def createToolBar(self):
        """ Creates a ToolBar with 3 buttons: a file selector, a settings button and a start button. 
            Params: None
            Return: None
        """
        self.toolbar = QToolBar(self);
        
        addFileAction = QAction(QIcon(ADD_FILES_ICON), ADD_FILES_TIP, self)
        addFileAction.setShortcut('Ctrl+O')
        addFileAction.triggered.connect(self.fileSelectDialog)

        resolveAction=QAction(QIcon(START_ICON), START_TIP, self)
        # resolveAction.setShortcut('Ctrl+K')

        settingsAction=QAction(QIcon(SETTINGS_ICON), SETTINGS_TIP, self)
        settingsAction.triggered.connect(self.settings)
        # settingsAction.setShortcut('Ctrl+L')
        
        self.addToolBar(self.toolbar);
        self.toolbar.addAction(addFileAction)
        self.toolbar.addAction(resolveAction)
        self.toolbar.addAction(settingsAction)


    def settings(self):
        """ Object method
            Params: none
            Return: none
            Opens a settings dialog.
        """
        settingsDialog = SettingsDialog(self)
        settingsDialog.exec_()


    def fileSelectDialog(self):
        """ Opens a file selection dialog and display on the grid the selected file.
            Params: none
            Return: none
        """
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_() :
            print(file_dialog.selectedFiles())
            self.controller.createInitialConfiguration(file_dialog.selectedFiles()[0])
    
    def initImages(self):
        """ TO DO """

        hbox = QHBoxLayout(self)

        murParking = QPixmap(MUR_PARKING)
        murParking = murParking.scaled(IMAGE_SIZE_MUR_PARKING, IMAGE_SIZE_MUR_PARKING)

        labelMurParking = QLabel(self)
        labelMurParking.setPixmap(murParking)        
        labelMurParking.resize(murParking.width(),murParking.height())
        labelMurParking.move(MARGIN_WIDTH_MUR_PARKING, MARGIN_HEIGHT_MUR_PARKING)

        parking = QPixmap(PARKING)
        parking = parking.scaled(IMAGE_SIZE_PARKING, IMAGE_SIZE_PARKING)

        labelParking = QLabel(self)
        labelParking.setPixmap(parking)        
        labelParking.resize(parking.width(),parking.height())
        labelParking.move(MARGIN_WIDTH_PARKING, MARGIN_HEIGHT_PARKING)

        hbox.addWidget(labelMurParking)
        hbox.addWidget(labelParking)
        self.setLayout(hbox)


    def printVehicles(self, listVehicles):
        """ Version 1 ne fonctionnant pas encore """
        
        hbox = QHBoxLayout(self)

        listLabel = []
        for vehicle in range(len(listVehicles)):
            label = QLabel(self)
            pixmap = None
            height = 0

            # camion ou voiture
            if(listVehicles[vehicle].getTypeVehicule == 2):
                pixmap = QPixmap(VOITURE)
                height = 2
            else:
                pixmap = QPixmap(CAMION)
                height = 3

            # image adaptée à la taille du reste
            label.resize(IMAGE_SIZE_PARKING / SIZE, IMAGE_SIZE_PARKING * height/ SIZE)

            # orientation
            if(listVehicles[vehicle].getOrientation() == 1):
                pixmap.rotate(-90)

            # position sur la fenêtre
            label.move(MARGIN_WIDTH_PARKING + ((listVehicles[vehicle].getMarqueur() - 1) % SIZE), MARGIN_HEIGHT_PARKING + round((listVehicles[vehicle].getMarqueur() - 1) / SIZE))
            listLabel.append(label)

        # ajout des images à la fenêtre
        [hbox.addWidget(label) for label in listLabel]
        # self.setLayout(hbox)


def main():
#if __name__ == "__main__":
    app = QApplication(sys.argv);
    rushhour = Window();
    sys.exit(app.exec_());

main()
