#/usr/bin/python3
# -*- coding:utf-8 -*-


""" Première version de ConfigViewer """

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QApplication)
from PyQt5.QtCore import QObjectCleanupHandler
from vehicule import *
from configuration import *

class ConfigDisplayer(QWidget): 

    def __init__(self, configuration, colors):
        super().__init__()
        grid = QGridLayout()
        # for marqueur, vehicule in enumerate(configuration.getConfiguration()):
        #     i, j = marqueur//6, marqueur%6
        #     label = QLabel(str(vehicule))
        #     label.setStyleSheet("background-color:rgb" + str(colors[str(vehicule)]) + ";qproperty-alignment: AlignCenter;border: 1px solid;");
        #     grid.addWidget(label, i, j)
        # self.setLayout(grid)

        print(configuration)
        posEmpty = list(range(36))
        for vehicule in configuration.getVehicules():
            marqueur = vehicule.getMarqueur()
            size = vehicule.getTypeVehicule()
            orientation = vehicule.getOrientation()

            posEmpty = [pos for pos in posEmpty if pos not in [occupatePos for occupatePos in range(marqueur, marqueur + size*orientation, orientation)]]
            i, j = marqueur//6, marqueur%6
            label = QLabel(str(vehicule))
            label.setStyleSheet("background-color:rgb" + str(colors[str(vehicule)]) + ";qproperty-alignment: AlignCenter;border: 1px solid;")
            if orientation == Orientation.BAS:
                grid.addWidget(label, i, j, size, 1)
            else:
                grid.addWidget(label, i, j, 1, size)

        for marqueur in posEmpty:
            i, j = marqueur//6, marqueur%6
            label = QLabel()
            label.setStyleSheet("background-color:rgb" + str(colors["0"]) + ";qproperty-alignment: AlignCenter;border: 1px solid;")
            grid.addWidget(label, i, j)

        self.setLayout(grid)


        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = ConfigDisplayer(Configuration.readFile("../puzzles/avancé/jam30.txt"))
    widget.show()
    sys.exit(app.exec_())