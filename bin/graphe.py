# -*- coding: utf-8 -*-

import math
import time
from configuration import *









class Noeud:
	""" Cette classe permet la création d'un noeud, avec un historique, un identifiant unique et une configuration"""

	def __init__(self, config):
		""" Params : config -> correspond à la configuration du noeud"""
		self.config = config
		self.id = str(config)
		self.historique = [None, None, None] # se présente sous la forme [pere, taille du chemin, profondeur]

	def getId(self):
		""" Permet de récupérer l'identifiant du noeud
			Params : None
			Return : l'identifiant du noeud
		"""
		return self.id


	def getConfig(self):
		""" Permet de récupérer la configuration du noeud
			Params : None
			Return : la configuration du noeud
		"""
		return self.config


	def getHistorique(self):
		""" Permet d'obtenir l'historique du noeud
			Params : None
			Return : la liste correspondant à l'historique du noeud
		"""
		return self.historique


	def setHistorique(self, historique):
		""" Modifie l'historique du noeud avec l'historique donnée en paramètre
			Params : historique
			Return : None
		"""
		self.historique = historique


	def getParent(self):
		""" Récupère la référence du père du noeud
			Params : None
			Return : Noeud pere
		"""
		return self.historique[0]


	def setParent(self, pere):
		""" Permet de modifier le père du noeud
			Params : pere du noeud
			Return : None
		"""
		self.historique[0] = pere


	def getLongueurChemin(self):
		""" Permet d'obtenir la longueur du chemin 
			Params : None
			Return : longueur du chemin pour atteindre le noeud
		"""
		return self.historique[1]


	def setLongueurChemin(self, longueurChemin):
		""" Permet de modifier l'historique du noeud
			Params : longueurChemin
			Return : None
		"""
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
	""" Cette classe permet la création d'un graphe contenant une liste de noeuds"""

	def __init__(self):
		""" Params : None"""
		self.noeuds = []


	def getNoeuds(self):
		""" retourne la liste des noeuds du graphe"""
		return self.noeuds


	def addNoeud(self, noeud):
		""" Cette fonction ajoute un noeud au graphe
			Params : Le noeud à ajouter
			Return : None
		"""
		self.noeuds.append(noeud)
			

	def constructNoeuds(self, noeud, nonDefinitveEdges, flag = "RHM"):
		""" construit des noeuds à partir du noeud passé en paramètre
			Params: noeud -> noeud à partir duquel on souhaite construire les autres noeuds
					nonDefinitiveEdges -> liste des noeuds non définitifs
					flag (facultatif) -> objetcif de résolution du problème, par défaut RHM
			Return : None
		"""

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
		""" ajoute le noeud et l'arête correspondant dans le graphe
			Params : noeudDefinitif auquel relier le noeud à créer
					 noeudToAdd : le noeud à ajouter au graphe
					 nonDefinitifEdges : liste de noeuds dont le chemin min n'est pas encore définitif
					 poids : poids du chemin du noeud définitif au noeud à ajouter
			Return : None
		"""

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
		""" compte le nombre de configuration atteignables en i pas depuis conf
			Params : Nombre de pas souhaités
			Return : nombre de configurations accessibles
		"""

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