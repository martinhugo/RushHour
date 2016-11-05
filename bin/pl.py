# -*- coding: utf-8 -*-

from configuration import *

class PL :
	""" 
		va définir les variables de contrainte nécessaires pour la résolution par PL. 

		Longueurs : v[i] : longueur du véhicule i
		PositionsVehicules : m[i][j] : tableau de positions représentant l'ensemble des positions occupées par le véhicule i quand le pointeur est en position j.
		Positions2Points : p[j][l] : ensemble des positions comprises entre j et l. -> TODO
		
	"""

	def __init__(self, config):

		self.nbMove = config.getNbCoupMax() # nombre de mouvements max autorisés

		self.longueurs = [0]*len(config.getVehicules())
		self.setLongueurs(config)

		self.positionsVehicules = []
		self.setPositionsVehicules(config)

		self.matricePresence = PL.initTab3D(len(config.getVehicules()), 36, self.nbMove + 1)
		self.setMatricePresence(config, 0)

		self.matriceOccupe = PL.initTab3D(len(config.getVehicules()), 36, self.nbMove + 1)
		self.setMatriceOccupe(config, 0)

		self.matriceMouvement = []
		[self.matriceMouvement.append(PL.initTab3D(36, 36, self.nbMove)) for i in range(len(config.getVehicules()))]

		
		

	def setMatricePresence(self, config, step):
		""" 
			Modifie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
			Si une voiture i a son marqueur sur une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon

			Paramètres : 
				- une configuration des voitures
				- une étape "step"

		"""

		for i in range(0, len(config.getVehicules())):
			self.matricePresence[i][ config.getVehicules()[i].getMarqueur() ][step] = 1

	def getMatricePresence(self):
		""" 
			Renvoie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
			Si une voiture i a son marqueur sur une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon
		"""
		return self.matricePresence


	def setMatriceOccupe(self, config, step):
		"""
			Modifie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
			Si une voiture i occupe une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon

			Paramètres : 
				- une configuration des voitures
				- une étape "step"
		"""

		for i in range(0, len(config.getVehicules())):
			vehicle = config.getVehicules()[i]
			for positions in self.positionsVehicules[i][vehicle.getMarqueur()]:
				self.matricePresence[i][ positions ][step] = 1

	def getMatriceOccupe(self):
		""" 
			Renvoie une matrice de la forme : [pour chaque voiture "i" ][pour chaque case "j" ][pour chaque étape "step"]
			Si une voiture i occupe une case j à une étape donnée "step", la case de la matrice correspondante indiquera 1, 0 sinon
		"""
		return self.matriceOccupe

	def setMatriceMouvement(self, config, step):
		""" 
			modifie une matrice de la forme [Pour chaque voiture i][pour chaque case j][Pour chaque case l][pour chaque étape]
			Va modifier si il y a eu un mouvement de k vers l entre l'étape k-1 et l'étape k
			S'il y a eu un mouvement, indique 1, sinon 0

			Paramètres : 
				- une configuration des voitures
				- une étape "step"
		"""
		# non vérifié


		if step>0:
			for i in range(0, len(config.getVehicules())):
				previousPointer = -1
				currentPointer = -1

				# ne sont modifiés que s'il y a eu un changement de la position du pointeur au cours du k-eme mouvement
				for j in range(36):
					
					# ne sera vérifié que si on avait un marqueur à une étape en j qui n'y est plus
					if(self.matricePresence[i][j][step - 1] < self.matricePresence[i][j][step]):
						previousPointer = j

					# ne sera vérifié que si on a un pointeur qui n'était pas présent à une étape en j et qui y est maintenant
					elif(self.matricePresence[i][j][step - 1] > self.matricePresence[i][j][step]):
						currentPointer = j

				if( previousPointer != -1 and currentPointer != -1):
					self.matriceMouvement[i][previousPointer][currentPointer][step] = 1


	def getMatriceMouvement(self):
		""" 
			renvoie une matrice de la forme [Pour chaque voiture i][pour chaque case j][Pour chaque case l][pour chaque étape]
			Va modifier si il y a eu un mouvement de k vers l entre l'étape k-1 et l'étape k
			S'il y a eu un mouvement, indique 1, sinon 0
		"""
		return self.matriceMouvement

	def setLongueurs(self, config):
		""" Défini la longueur de tous les véhicules de config

		Paramètres : 
				- une configuration des voitures
		"""

		for i in range(0, len(config.getVehicules())):
			self.longueurs[i] = config.getVehicules()[i].getTypeVehicule()

	def getLongueurs(self, config):
		""" Renvoie la longueur de tous les véhicules de config"""
		return self.longueurs

	def setPositionsVehicules(self, config):
		""" Pour chaque véhicule et pour chaque case, défini toutes les cases occupées

		Paramètres : 
				- une configuration des voitures


		TODO -> 1ere itération : considère que les véhicules peuvent aller dans toutes les cases de la grille, 
		à modifier pour ne permettre que des déplacement en fonction de leur ligne ou colonne de départ

		"""
		for i in range(0, len(config.getVehicules())):

			vehicle = config.getVehicules()[i] 
			self.positionsVehicules.append([])

			# pour chaque positions -> à modifier par la suite
			for j in range(36):

				listToAdd = []

				# si le véhicule est tourné vers la droite
				if(vehicle.getOrientation() == 1):
					if (vehicle.getMarqueur() + vehicle.getTypeVehicule()) <36: # vérifie que le véhicule ne peut pas sortir de la grille
						for length in range(vehicle.getTypeVehicule()):
							listToAdd.append(vehicle.getMarqueur() + length) # ajoute les positions occupées pour la position j

				# si le véhicule est tourné vers le bas
				else:
					if (vehicle.getMarqueur() + (vehicle.getTypeVehicule() * 6)) <36: # vérifie que le véhicule ne peut pas sortir de la grille
						for length in range(vehicle.getTypeVehicule()):
							listToAdd.append(vehicle.getMarqueur() + length * 6) # ajoute les positions occupées pour la position j

				self.positionsVehicules[i].append(listToAdd)

		def getPositionsVehicules(self):
			""" Renvoie la liste de toutes les cases occupées pour un véhicule et une case donnée """
			return self.positionsVehicules

		def setPosition2Points(self):
			# TODO
			pass

		def getPositions2Points(self):
			# TODO
			pass


	@staticmethod
	def initTab3D(x, y, z):
		""" créé et initialise un tableau à 3 dimensions aux tailles données en paramètre """

		tab = []
		for i in range(x):
			tab.append([])
			for j in range(y):
				tab[i].append([0] * z)
		return tab

def main(): # pour corriger version buggée python (à ne pas oublier de retirer)
# if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
    pl = PL(conf)
    [print(pl.getMatricePresence()[i]) for i in range(len(pl.getMatricePresence()))]
    [print(pl.getMatriceOccupe()[i]) for i in range(len(pl.getMatriceOccupe()))]

main()