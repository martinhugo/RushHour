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

	def launchDijkstra(self, config, nbMax):

		start_time = time.time()

		configPoidsMin = Noeud(config)
		configPoidsMin.setLongueurChemin(0)
		configPoidsMin.setHistorique([config])

		self.graphe.addNoeud(configPoidsMin) # ajout du noeud dans le graphe
		self.B.append(configPoidsMin) # ajout du premier noeud dans B (tant que pas dans la boucle, pas définitif)

		while(not self.verifCondition(configPoidsMin.getConfig())):
			
			self.A.append(configPoidsMin) # on ajoute le noeud définitif à A
			self.B.remove(configPoidsMin) # on retire le noeud définitif de B
			self.graphe.constructNoeuds(configPoidsMin, self.B)

			# initialisation
			poidsMin = math.inf
			noeudCheminMin = None

			for noeudNotA in self.B: # pour chaque noeud dans B
				for arete in noeudNotA.getAretes(): # pour chaque arete reliant B à A (aucune arete ne relie deux noeuds de B)
					noeudA = arete.getExtremite(noeudNotA) # on récupère le noeud dans A
					noeudNotA = self.majLongueurChemin(arete, noeudNotA, noeudA) # on met à jour la taille du chemin de noeud de B
					poidsMin, noeudCheminMin = self.majPoidsMin(poidsMin, arete, noeudNotA, noeudA, noeudCheminMin) # on met à jour poids min et noeud chemin min

			configPoidsMin = noeudCheminMin # on récupère le chemin le plus court et on itère
			print(configPoidsMin.getLongueurChemin())

		print("\nlongueur minimale trouvée : ", configPoidsMin.getLongueurChemin(), "\n")
		[print(configPoidsMin.getHistorique()[i]) for i in range(len(configPoidsMin.getHistorique()))]
		stop_time = time.time()
		print("temps total ---->", stop_time - start_time, " sec")
		

	@staticmethod
	def verifCondition(config):
		""" si le noeud sélectionné permet de conclure qu'on a fini, ie voiture "g" en position 16"""
		vehicules = config.getVehicules()
		for vehicule in vehicules:
			if(vehicule.getIdVehicule() == 'g'):
				if(vehicule.getMarqueur() == 16):
					return True
		return False

	def majLongueurChemin(self, arete, noeud, noeudDefinitif):
		""" retourne le noeud mis à jour si le chemin est plus court"""
		if((noeudDefinitif.getLongueurChemin() + arete.getPoids()) < noeud.getLongueurChemin()):
			noeud.setLongueurChemin(noeudDefinitif.getLongueurChemin() + arete.getPoids())
			noeud.setHistorique(noeudDefinitif.getHistorique() + [noeud.getConfig()])
		return noeud

	def majPoidsMin(self, poidsMin, arete, noeud, noeudDefinitif, noeudCheminMin):
		""" retourne poidsMin si le poidsMin est plus petit que celui fournit en paramètre"""
		if((noeudDefinitif.getLongueurChemin() + arete.getPoids()) < poidsMin):
			poidsMin = noeudDefinitif.getLongueurChemin() + arete.getPoids()
			noeudCheminMin = noeud
		return poidsMin, noeudCheminMin



def main():
# if __name__ == "__main__":

	dijkstra = Dijkstra()
	conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
	noeud = Noeud(conf)
	dijkstra.launchDijkstra(conf, 8)

main()






