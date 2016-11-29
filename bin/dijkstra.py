# -*- coding: utf-8 -*-

import math
import time

from configuration import *
from graphe import *

class Dijkstra:
	""" """

	def __init__(self, config, nbMax, flag = "RHM"):
		self.graphe = Graphe()
		self.config = config
		self.nbMax = nbMax
		self.B = [] # correspond aux noeuds de chemin non définitif
		self.solution = self.solve(flag)


	def getConfig(self):
		return self.config

	def getNbMax(self):
		return self.nbMax

	def getSolution(self):
		return self.solution






	def solve(self, flag = "RHM"):

		start_time = time.time()

		configPoidsMin = Noeud(self.getConfig())
		configPoidsMin.setHistorique([[self.getConfig(), 0]])

		self.graphe.addNoeud(configPoidsMin) # ajout du noeud dans le graphe
		self.B.append(configPoidsMin) # ajout du premier noeud dans B (tant que pas dans la boucle, pas définitif)

		print(time.time() - start_time)
		while(not configPoidsMin == None and not Configuration.verifCondition(configPoidsMin.getConfig()) and self.getNbMax() > (len(configPoidsMin.getHistorique())-1)):

			self.B.remove(configPoidsMin) # on retire le noeud définitif de B
			self.graphe.constructNoeuds(configPoidsMin, self.B, flag) # ajout des noeuds inexistants et maj de la taille du chemin

			# initialisation
			poidsMin = math.inf
			noeudCheminMin = None

			for noeudNotA in self.B: # pour chaque noeud dans B
				poidsMin, noeudCheminMin = Dijkstra.majPoidsMin(poidsMin, noeudNotA, noeudCheminMin) # on met à jour poids min et noeud chemin min

			configPoidsMin = noeudCheminMin # on récupère le chemin le plus court et on itère

		stop_time = time.time()
		print("temps total ---->", round(stop_time - start_time, 2), " sec")

		# si tout le graphe a été parcouru sans qu'une solution ne soit trouvée
		if(configPoidsMin == None):
			#print("Il n'existe pas de solution réalisable pour cette grille")
			return []

		# si on a trouvé une solution
		elif self.getNbMax() > len(configPoidsMin.getHistorique()):
			# [print(configPoidsMin.getHistorique()[i][0]) for i in range(len(configPoidsMin.getHistorique()))]
			# print("\nlongueur minimale trouvée : ", configPoidsMin.getLongueurChemin(), "\n")
			listConfig = [configPoidsMin.getHistorique()[i][0] for i in range(len(configPoidsMin.getHistorique()))]
			listConfig.reverse()
			return listConfig	# si on a pas trouvé de solution en un nombre de pas < nbMax

		else:
			# print("pas de solution trouvée en moins de", nbMax, "pas.\n")
			return []

		

	@staticmethod
	def majPoidsMin(poidsMin, noeud, noeudCheminMin):
		""" retourne poidsMin si le poidsMin est plus petit que celui fournit en paramètre """
		if(noeud.getLongueurChemin() < poidsMin):
			poidsMin = noeud.getLongueurChemin()
			noeudCheminMin = noeud
		return poidsMin, noeudCheminMin



if __name__ == "__main__":

	conf = Configuration.readFile("../puzzles/débutant/jam1.txt")
	dijkstra = Dijkstra(conf, 35, flag = "RHM")
	print(len(dijkstra.getSolution()))
	# dijkstra.launchDijkstra(conf, 35, flag = "RHM")
	# print("nombre de configurations atteignables en 15 pas -->", Graphe.countConfig(conf, 15))






