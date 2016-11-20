# -*- coding: utf-8 -*-

import math
import time

from configuration import *
from graphe import *

class Dijkstra:
	""" première version de l'algo, peu optimisée, et n'enregistrant pas encore l'historique du chemin parcouru, affiche le poids min trouvé """

	def __init__(self):
		self.graphe = Graphe()
		self.A = [] # correspond aux noeud dont un chemin de longueur définitive a été trouvé
		self.B = []
		self.notA = []

	def launchDijkstra(self, config, nbMax):

		
		configPoidsMin = Noeud(config)
		configPoidsMin.setLongueurChemin(0)
		self.graphe.addNoeud(configPoidsMin)
		self.B.append(configPoidsMin)
		# i = 0
		# while(i<2):

		# 	i+=1
		while(not self.verifCondition(configPoidsMin.getConfig())):
			start_time = time.time()
			self.A.append(configPoidsMin)
			self.B.remove(configPoidsMin)
			# time3 = time.time()
			self.graphe.constructNoeuds(configPoidsMin, self.B) # occupe 1/6 du temps total
			# time4 = time.time()
			# print("construction du graphe---->", time4 - time3)

			# initialisation
			aretesAAnalyser = self.graphe.getAretesFromNoeud(self.B) # toutes les aretes entre A et non A
			poidsMin = math.inf
			noeudCheminMin = None

			# for arete in aretesAAnalyser:
			for noeudNotA in self.B:
				for arete in noeudNotA.getAretes():
					# on prend les extrémités de l'arete
					noeudA = arete.getExtremite(noeudNotA) # on récupère le noeud dans A
					
					# on met à jour la taille du chemin de noeud en dehors de A
					noeudNotA = self.majLongueurChemin(arete, noeudNotA, noeudA)

					# on met à jour poids min
					poidsMin, verif = self.majPoidsMin(poidsMin, arete, noeudNotA, noeudA)

					# si poids min mis à jour, on a rencontré un chemin plus court, que l'on stocke
					if(verif):
						noeudCheminMin = noeudNotA

			# on récupère le chemin le plus court et on itère
			configPoidsMin = noeudCheminMin
			stop_time = time.time()
			print("temps boucle --->", stop_time - start_time)

			print("poids chemin considéré : ", noeudCheminMin.getLongueurChemin())

		print("\nlongueur minimale trouvée : ", configPoidsMin.getLongueurChemin(), "\n")
		print(configPoidsMin.getConfig())
		
		

	@staticmethod
	def verifCondition(config):
		""" si le noeud sélectionné permet de conclure qu'on a fini, ie voiture "g" en position 16"""
		
		vehicules = config.getVehicules()
		vehiculeG = None
		for vehicule in vehicules:
			if(vehicule.getIdVehicule() == 'g'): # -------> A modifier par la suite
				vehiculeG = vehicule
		if(vehiculeG.getMarqueur() == 16):
			return True
		return False

	def majLongueurChemin(self, arete, noeud, noeudDefinitif):
		""" retourne le noeud mis à jour si le chemin est plus court"""
		if((noeudDefinitif.getLongueurChemin() + arete.getPoids()) < noeud.getLongueurChemin()):
			noeud.setLongueurChemin(noeudDefinitif.getLongueurChemin() + arete.getPoids())
			# noeud.setHistorique(noeudDefinitif.getConfig())
		return noeud

	def majPoidsMin(self, poidsMin, arete, noeud, noeudDefinitif):
		""" retourne poidsMin si le poidsMin est plus petit que celui fournit en paramètre"""
		if((noeudDefinitif.getLongueurChemin() + arete.getPoids()) < poidsMin):
			poidsMin = noeudDefinitif.getLongueurChemin() + arete.getPoids()
			return poidsMin, True
		return poidsMin, False



def main():

	dijkstra = Dijkstra()
	conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
	print(conf)

	noeud = Noeud(conf)
	dijkstra.launchDijkstra(conf, 8)

main()






