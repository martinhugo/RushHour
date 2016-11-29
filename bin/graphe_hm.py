# -*- coding: utf-8 -*-

import math
import time
from configuration import *









class Noeud:

	def __init__(self, config):
		self.config = config
		self.id = str(config)
		self.historique = []

	def getId(self):
		return self.id


	def getConfig(self):
		""" Retourne la configuration correpondant au noeud """
		return self.config


	def getLongueurChemin(self):
		""" retourne la longueur du chemin """
		return self.historique[-1][1]


	def setLongueurChemin(self, longueurChemin):
		self.historique[-1][1] = longueurChemin


	def getHistorique(self):
		""" retourne l'historique du noeud"""
		return self.historique


	def setHistorique(self, historique):
		""" modifie l'historique du noeud"""
		self.historique = historique

	def __eq__(self, noeud2):
		""" cette fonction retourne vrai si les 2 noeuds donnés en paramètres ont la meme config"""
		return self.getId() == noeud2.getId()



	@staticmethod
	def compare2Noeuds(noeud1, noeud2):
		""" cette fonction retourne vrai si les 2 noeuds donnés en paramètres ont la meme config"""
		return noeud1.getId() == noeud2.getId()













class Graphe:

	def __init__(self):
		self.noeuds = []


	def getNoeuds(self):
		""" retourne la liste des noeuds du graphe"""
		return self.noeuds


	def addNoeud(self, noeud):
		self.noeuds.append(noeud)
			

	def constructNoeuds(self, noeud, nonDefinitveEdges, flag = "RHM"):
		""" construit des noeuds en fonction d'un dictionnaire passé en paramètre"""
		start_time = time.time()
		movements = noeud.getConfig().getPossibleMovements()
		poids = 1
		# pour chaque véhicule, pour chaque position possible du véhicule
		for vehicle in movements.keys():

			listVehicules = noeud.getConfig().getVehicules()
			marqueurVehicle = listVehicules[listVehicules.index(vehicle)].getMarqueur()
			orientationVehicle = listVehicules[listVehicules.index(vehicle)].getOrientation()

			for marqueur in movements[vehicle]:

				if(flag != "RHM"):
					poids = abs(marqueurVehicle - marqueur)/orientationVehicle

				currentEdge = self.verifNoeudInGraphe(Noeud(Configuration.newConfig(noeud.getConfig(), vehicle, marqueur)))

				if(len(currentEdge.getHistorique()) == 0): # si le noeud n'a jamais été crée
					self.constructNoeud(noeud, currentEdge, nonDefinitveEdges, poids)

				elif(currentEdge.getLongueurChemin() > noeud.getLongueurChemin() + poids): # si noeud déjà créé et chemin plus petit possible
					currentEdge.setLongueurChemin(noeud.getLongueurChemin() + poids)
				


	def constructNoeud(self, noeudDefinitif, noeudToAdd, nonDefinitveEdges, poids):
		""" ajoute le noeud et l'arête correspondant dans le graphe si le noeud et l'arete ne sont pas déjà dans le graphe"""
		noeudToAdd.setHistorique(noeudDefinitif.getHistorique() + [[noeudToAdd.getConfig(), noeudDefinitif.getLongueurChemin() + poids]])
		self.addNoeud(noeudToAdd)
		nonDefinitveEdges.append(noeudToAdd)


	def verifNoeudInGraphe(self, noeud):
		""" Retourne une référence sur un noeud existant si ce noeud existe déja dans le graphe, 
			renvoi la nouvelle référence sinon. 
		"""
		for n in self.getNoeuds():
			if(Noeud.compare2Noeuds(n, noeud)):
				return n
		return noeud



	### METHODE INUTILE ??
	@staticmethod
	def countConfig(conf, i):
		""" compte le nombre de configuration atteignables en i pas depuis conf"""

		graphe = Graphe()
		flag = "RHM"
		config = Noeud(conf)
		config.setHistorique([[conf, 0]])
		A = [config]

		while(not config == None and i > (len(config.getHistorique())-1)):
			A.remove(config) # on retire le noeud définitif de A
			graphe.constructNoeuds(config, A, flag) # ajout des noeuds inexistants et maj de la taille du chemin
			config = A[0]
		return len(graphe.getNoeuds())-1