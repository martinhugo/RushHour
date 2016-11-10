
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

# def setMatricePresence(self, config, step):
#         """ 
#             Modifie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
#             Si une voiture i a son marqueur sur une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon

#             Paramètres : 
#                 - une configuration des voitures
#                 - une étape "step"

#         """

#         for i in range(0, len(config.getVehicules())):
#             self.matricePresence[i][ config.getVehicules()[i].getMarqueur() ][step] = 1

#     def getMatricePresence(self):
#         """ 
#             Renvoie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
#             Si une voiture i a son marqueur sur une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon
#         """
#         return self.matricePresence








#     def setMatriceOccupe(self, config, step):
#         """ Modifie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
#             Si une voiture i occupe une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon

#             Paramètres : 
#                 - une configuration des voitures
#                 - une étape "step"
#         """

#         for i in range(0, len(config.getVehicules())):
#             vehicle = config.getVehicules()[i]
#             for positions in self.positionsVehicules[i][vehicle.getMarqueur()]:
#                 self.matricePresence[i][ positions ][step] = 1

#     def getMatriceOccupe(self):
#         """ Renvoie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
#             Si une voiture i occupe une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon
#         """
#         return self.matriceOccupe












#     def setMatriceMouvement(self, config, step):
#         """ 
#             modifie une matrice de la forme [Pour chaque voiture i][pour chaque case j][Pour chaque case l][pour chaque étape]
#             Va modifier si il y a eu un mouvement de k vers l entre l'étape k-1 et l'étape k
#             S'il y a eu un mouvement, indique 1, sinon 0

#             Paramètres : 
#                 - une configuration des voitures
#                 - une étape "step"
#         """

#         if step>0:
#             for i in range(0, len(config.getVehicules())):
#                 previousPointer = -1
#                 currentPointer = -1

#                 # ne sont modifiés que s'il y a eu un changement de la position du pointeur au cours du k-eme mouvement
#                 for j in range(36):
                    
#                     # ne sera vérifié que si on avait un marqueur à une étape en j qui n'y est plus
#                     if(self.matricePresence[i][j][step - 1] < self.matricePresence[i][j][step]):
#                         previousPointer = j

#                     # ne sera vérifié que si on a un pointeur qui n'était pas présent à une étape en j et qui y est maintenant
#                     elif(self.matricePresence[i][j][step - 1] > self.matricePresence[i][j][step]):
#                         currentPointer = j

#                 if( previousPointer != -1 and currentPointer != -1):
#                     self.matriceMouvement[i][previousPointer][currentPointer][step] = 1


#     def getMatriceMouvement(self):
#         """ 
#             renvoie une matrice de la forme [Pour chaque voiture i][pour chaque case j][Pour chaque case l][pour chaque étape]
#             Va modifier si il y a eu un mouvement de k vers l entre l'étape k-1 et l'étape k
#             S'il y a eu un mouvement, indique 1, sinon 0
#         """
#         return self.matriceMouvement

    


# Initialisation des variables de décision associé au véhicule
# Définir des contraintes pour initialiser l'instance ?
# print(idVehicule, vehicule.getMarqueur())
# self.x[idVehicule][vehicule.getMarqueur()][0].setAttr("X", 1)
# for pos in self.positionsVehicules[idVehicule]:
#     self.z[idVehicule][position][0].setAttr("X", 1)