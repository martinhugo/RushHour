#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""

import sys
import os

from configuration import Configuration

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QDialog, QFileDialog, QToolBar, QVBoxLayout, QLabel, QHBoxLayout, QWidget)
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
MARGIN_WIDTH_MUR_PARKING = (WINDOW_WIDTH - IMAGE_SIZE_MUR_PARKING) / 2
MARGIN_HEIGHT_MUR_PARKING = (WINDOW_HEIGHT - IMAGE_SIZE_MUR_PARKING) / 2

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
        # self.show()

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
        """ initialize and display the images on the window.
            Params : None
            Return : None
        """

        # affiche les deux images : le mur du parking et le parking, en les plaçant au centre de la fenêtre
        self.newImage(MUR_PARKING, [IMAGE_SIZE_MUR_PARKING, IMAGE_SIZE_MUR_PARKING], [MARGIN_WIDTH_MUR_PARKING, MARGIN_HEIGHT_MUR_PARKING])
        self.newImage(PARKING, [IMAGE_SIZE_PARKING, IMAGE_SIZE_PARKING], [MARGIN_WIDTH_PARKING, MARGIN_HEIGHT_PARKING])

    
    def newImage(self, path, size = [], move = [], rotation = 0):
        """ Create a new image which is added to the window
            Params : 
                - path : path of the image
                - size : list of 2 elements [width, height]
                - move : list of 2 elements [moveX, moveY]
                - rotation : rotation of the image
            Return : None
        """

        image = QPixmap(path)

        label = QLabel(self)
        label.setPixmap(image)

        if(size != []):
            image = image.scaled(size[0], size[1])
            label.resize(image.width(), image.height())

        if(move != []):
            label.move(move[0], move[1])

        # if(rotation != 0):
            # TO DO

    def printVehicles(self, listVehicles):
        """ display the vehicles on the window.
            Params : 
                - listVehicles : list of vehicles to display
            Return : None
        """  
        path = ""   
        sizeCase = IMAGE_SIZE_PARKING/SIZE

        for vehicle in listVehicles:
            height = 0

            # camion ou voiture ( ne prend pas en compte le fait que la voiture soit celle à déplacer ou pas : TO DO)
            if(vehicle.getTypeVehicule() == 2):
                path = VOITURE
                height = 2
            else:
                path = CAMION
                height = 3

            position = vehicle.getMarqueur()
            positionX = position % SIZE
            positionY = int(position / SIZE)

            print(positionX, ", ", positionY)

            # rotation si le véhicule est orienté vers la droite: 
            if(vehicle.getOrientation() == 1):
                rotation = -90

            self.newImage(path, [sizeCase, sizeCase * height], [positionX * sizeCase, positionY * sizeCase], rotation)

    def updateWindow(self, newConfig):
        """ TO DO """
        pass
            


def main():
#if __name__ == "__main__":
    app = QApplication(sys.argv);
    rushhour = Window();
    config = Configuration.readFile("../puzzles/avancé/jam30.txt")
    print(config)
    rushhour.printVehicles(config.getVehicules())
    rushhour.show() # temporaire le temps de faire une méthode mettant à jour les éléments à afficher et ceux à cacher
    sys.exit(app.exec_());

main()
