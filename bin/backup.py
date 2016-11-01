
# MUR_PARKING = "../img/MurParking.png"
# PARKING = "../img/parkingBase.png"
# VOITURE = "../img/voiture.png"
# VOITURE_A_SORTIR = "../img/voitureASortir.png"
# CAMION = "../img/camion.png"

# # width and height
# WINDOW_WIDTH = 1000
# WINDOW_HEIGHT = 600

# IMAGE_SIZE_MUR_PARKING = 500
# MARGIN_WIDTH_MUR_PARKING = (WINDOW_WIDTH - IMAGE_SIZE_MUR_PARKING) / 2
# MARGIN_HEIGHT_MUR_PARKING = (WINDOW_HEIGHT - IMAGE_SIZE_MUR_PARKING) / 2

# IMAGE_SIZE_PARKING = 464
# MARGIN_HEIGHT_PARKING = (WINDOW_HEIGHT - IMAGE_SIZE_PARKING) / 2
# MARGIN_WIDTH_PARKING = (WINDOW_WIDTH - IMAGE_SIZE_PARKING) / 2

# SIZE = 6



# def initImages(self):
    #     """ initialize and display the images on the window.
    #         Params : None
    #         Return : None
    #     """

    #     # affiche les deux images : le mur du parking et le parking, en les plaçant au centre de la fenêtre
    #     self.newImage(MUR_PARKING, [IMAGE_SIZE_MUR_PARKING, IMAGE_SIZE_MUR_PARKING], [MARGIN_WIDTH_MUR_PARKING, MARGIN_HEIGHT_MUR_PARKING])
    #     self.newImage(PARKING, [IMAGE_SIZE_PARKING, IMAGE_SIZE_PARKING], [MARGIN_WIDTH_PARKING, MARGIN_HEIGHT_PARKING])

    
    # def newImage(self, path, size = [], move = [], rotation = 0):
    #     """ Create a new image which is added to the window
    #         Params : 
    #             - path : path of the image
    #             - size : list of 2 elements [width, height]
    #             - move : list of 2 elements [moveX, moveY]
    #             - rotation : rotation of the image
    #         Return : None
    #     """

    #     image = QPixmap(path)

    #     label = QLabel(self)
    #     label.setPixmap(image)

    #     if(size != []):
    #         image = image.scaled(size[0], size[1])
    #         label.resize(image.width(), image.height())

    #     if(move != []):
    #         label.move(move[0], move[1])

    #     # if(rotation != 0):
    #         # TO DO

    # def printVehicles(self, listVehicles):
    #     """ display the vehicles on the window.
    #         Params : 
    #             - listVehicles : list of vehicles to display
    #         Return : None
    #     """  
    #     path = ""   
    #     sizeCase = IMAGE_SIZE_PARKING/SIZE

    #     for vehicle in listVehicles:
    #         height = 0

    #         # camion ou voiture ( ne prend pas en compte le fait que la voiture soit celle à déplacer ou pas : TO DO)
    #         if(vehicle.getTypeVehicule() == 2):
    #             path = VOITURE
    #             height = 2
    #         else:
    #             path = CAMION
    #             height = 3

    #         position = vehicle.getMarqueur()
    #         positionX = position % SIZE
    #         positionY = int(position / SIZE)

    #         print(positionX, ", ", positionY)

    #         # rotation si le véhicule est orienté vers la droite: 
    #         if(vehicle.getOrientation() == 1):
    #             rotation = -90

    #         self.newImage(path, [sizeCase, sizeCase * height], [positionX * sizeCase, positionY * sizeCase], rotation)
