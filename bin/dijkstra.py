# -*- coding: utf-8 -*-

import math
import time

from configuration import *
from graphe import *

class Dijkstra:
	""" première version de l'algo, peu optimisée, et n'enregistrant pas encore l'historique du chemin parcouru, affiche le poids min trouvé """

	def __init__(self):
		self.graphe = Graphe()
		self.A = [] # correspond aux noeud de chemin définitif
		self.B = [] # correspond aux noeuds de chemin non définitif

	def launchDijkstra(self, config, nbMax, flag = "RHM"):

		start_time = time.time()

		configPoidsMin = Noeud(config)
		configPoidsMin.setHistorique([[config, 0]])

		self.graphe.addNoeud(configPoidsMin) # ajout du noeud dans le graphe
		self.B.append(configPoidsMin) # ajout du premier noeud dans B (tant que pas dans la boucle, pas définitif)

		while(not Configuration.verifCondition(configPoidsMin.getConfig())):

			self.A.append(configPoidsMin) # on ajoute le noeud définitif à A
			self.B.remove(configPoidsMin) # on retire le noeud définitif de B
			self.graphe.constructNoeuds(configPoidsMin, self.B, flag) # ajout des noeuds inexistants et maj de la taille du chemin

			# initialisation
			poidsMin = math.inf
			noeudCheminMin = None

			for noeudNotA in self.B: # pour chaque noeud dans B
				poidsMin, noeudCheminMin = Dijkstra.majPoidsMin(poidsMin, noeudNotA, noeudCheminMin) # on met à jour poids min et noeud chemin min

			configPoidsMin = noeudCheminMin # on récupère le chemin le plus court et on itère

		print("\nlongueur minimale trouvée : ", configPoidsMin.getLongueurChemin(), "\n")
		[print(configPoidsMin.getHistorique()[i][0]) for i in range(len(configPoidsMin.getHistorique()))]
		stop_time = time.time()
		print("temps total ---->", stop_time - start_time, " sec")
		

	@staticmethod
	def majPoidsMin(poidsMin, noeud, noeudCheminMin):
		""" retourne poidsMin si le poidsMin est plus petit que celui fournit en paramètre """
		if(noeud.getLongueurChemin() < poidsMin):
			poidsMin = noeud.getLongueurChemin()
			noeudCheminMin = noeud
		return poidsMin, noeudCheminMin



def main():
# if __name__ == "__main__":

	dijkstra = Dijkstra()
	conf = Configuration.readFile("../puzzles/débutant/jam1.txt")
	noeud = Noeud(conf)
	dijkstra.launchDijkstra(conf, 8, flag = "RHC")

main()






