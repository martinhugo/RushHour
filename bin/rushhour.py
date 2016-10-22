#/usr/bin/python3
# -*- coding:utf-8 -*-

""" Main Module of the GooDoc Application.
    The application is started by launching this module.
    It contains the Window class and the main procedure.
"""

import sys
import os

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QDialog, QFileDialog, QToolBar)
from PyQt5.QtGui import QIcon



# Images
ADD_FILES_ICON = "../img/addFiles.png"
START_ICON = "../img/start.png"
SETTINGS_ICON = "../img/settings.png"

# ToolTip
ADD_FILES_TIP = "Add files"
START_TIP = "Start generation"
SETTINGS_TIP = "Settings"


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


    def initScreen(self):
        """ This method sets up the documentation screen.
            A <INSERT NAME> is created and set as the central widget.
            Params: None
            Return: None
        """
        self.createToolBar()
        self.setWindowTitle("RUSH HOUR")
        self.setGeometry(100,100, 1200, 600)
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
        # settingsAction.setShortcut('Ctrl+L')
        
        self.addToolBar(self.toolbar);
        self.toolbar.addAction(addFileAction)
        self.toolbar.addAction(resolveAction)
        self.toolbar.addAction(settingsAction)


    def fileSelectDialog(self):
        """ Opens a file selection dialog and display on the grid the selected file.
            Params: none
            Return: none
        """
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_() :
            print(file_dialog.selectedFiles())
	        # self._files.addFiles(file_dialog.selectedFiles())



def main():
#if __name__ == "__main__":
    app = QApplication(sys.argv);
    rushhour = Window();
    sys.exit(app.exec_());

main()
