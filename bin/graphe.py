# -*- coding: utf-8 -*-

import math
import time
from configuration import *









class Noeud:

	def __init__(self, config):
		self.config = config
		self.id = str(config)
		self.historique = [None, None, None] # se présente sous la forme [pere, taille du chemin, profondeur]

	def getId(self):
		return self.id


	def getConfig(self):
		""" Retourne la configuration correpondant au noeud """
		return self.config


	def getHistorique(self):
		""" retourne l'historique du noeud"""
		return self.historique


	def setHistorique(self, historique):
		""" modifie l'historique du noeud"""
		self.historique = historique


	def getParent(self):
		return self.historique[0]


	def setParent(self, pere):
		self.historique[0] = pere


	def getLongueurChemin(self):
		""" retourne la longueur du chemin """
		return self.historique[1]


	def setLongueurChemin(self, longueurChemin):
		self.historique[1] = longueurChemin


	def getProfondeur(self):
		return self.historique[2]


	def setProfondeur(self, longueurChemin):
		self.historique[2] = longueurChemin


	def __eq__(self, noeud2):
		""" cette fonction retourne vrai si les 2 noeuds donnés en paramètres ont la meme config"""
		return self.getId() == noeud2.getId() if noeud2 != None else None


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

				if(currentEdge.getProfondeur() == None): # si le noeud n'a jamais été crée
					self.constructNoeud(noeud, currentEdge, nonDefinitveEdges, poids)

				elif(currentEdge.getLongueurChemin() > noeud.getLongueurChemin() + poids): # si noeud déjà créé et chemin plus petit possible
					currentEdge.setLongueurChemin(noeud.getLongueurChemin() + poids)
					currentEdge.setParent(noeud)
				


	def constructNoeud(self, noeudDefinitif, noeudToAdd, nonDefinitveEdges, poids):
		""" ajoute le noeud et l'arête correspondant dans le graphe si le noeud et l'arete ne sont pas déjà dans le graphe"""
		noeudToAdd.setHistorique([noeudDefinitif, noeudDefinitif.getLongueurChemin() + poids, noeudDefinitif.getProfondeur() + 1])
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



	@staticmethod
	def countConfig(conf, nbPas):
		""" compte le nombre de configuration atteignables en nbPas pas depuis conf"""

		graphe = Graphe()
		config = Noeud(conf)
		config.setHistorique([conf, 0, 0])
		A = [config]

		while(config != None and nbPas > config.getProfondeur()):
			print(config.getProfondeur())
			A.remove(config) # on retire le noeud définitif de A
			graphe.constructNoeuds(config, A) # ajout des noeuds inexistants et maj de la taille du chemin
			if len(A) > 0: # si on est pas au dernier élément
				config = A[0]
			else:
				config = None
		return len(graphe.getNoeuds())