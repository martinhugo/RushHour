# -*- coding: utf-8 -*-

import math
from configuration import *
from copy import copy












class Arete:

	def __init__(self, coupleNoeud, poids):
		self.coupleNoeud = coupleNoeud
		self.poids = poids

	def getCoupleNoeud(self):
		""" retourne le couple de noeuds reliés par l'arête """
		return self.coupleNoeud

	def setCoupleNoeud(self, coupleNoeud):
		""" permet de modifier le couple de noeuds reliés par l'arête par ceux donnés en paramètre """
		self.coupleNoeud = coupleNoeud

	def getPoids(self):
		""" retourne le poids de l'arête """
		return self.poids

	def setPoids(self, poids):
		""" modifie le poids de l'arête par celui donné en paramètre """
		self.poids = poids

	def getExtremite(self, noeud):
		""" retourne le noeud à l'autre extrémité de l'arete"""
		if(self.coupleNoeud[0] == noeud):
			return self.coupleNoeud[1]
		return self.coupleNoeud[0]













class Noeud:

	def __init__(self, config):
		self.config = config
		self.longueurChemin = math.inf
		self.historique = []
		self.aretesReliees = []
		self.aretes = []

	def getConfig(self):
		""" Retourne la configuration correpondant au noeud """
		return self.config

	def setLongueurChemin(self, longueurChemin):
		""" modifie la longueur du chemin par celle donnée en paramètre """
		self.longueurChemin = longueurChemin

	def getLongueurChemin(self):
		""" retourne la longueur du chemin """
		return self.longueurChemin

	def getHistorique(self):
		""" retourne l'historique du noeud"""
		return self.historique

	def setHistorique(self, historique):
		""" modifie l'historique du noeud"""
		self.historique = historique

	def addAreteReliee(self, arete):
		self.aretesReliees.append(arete)

	def getNoeudsRelies(self):
		return self.noeudsRelies

	def addArete(self, arete):
		self.aretes.append(arete)

	def getAretes(self):
		return self.aretes













class Graphe:

	def __init__(self):
		self.noeuds = []
		self.aretes = []


	############################### GETTERS ET SETTERS #########################################

	def getNoeuds(self):
		""" retourne la liste des noeuds du graphe"""
		return self.noeuds

	def getAretes(self):
		""" retourne la liste des aretes du graphe"""
		return self.aretes

	def getNoeud(self, config):
		""" retourne les noeuds selon la config donnée en paramètre"""
		return [item for item in self.noeuds if self.compare2Config(item.getConfig(), config)]

	def getArete(self, coupleNoeuds):
		""" retourne l'arete correspondant au couple de noeuds fournit en argument"""
		arete = Arete(coupleNoeuds)
		for item in self.aretes:
			if (Graphe.compare2Arete(item, arete)):
				return item
		return []

	def getAretesFromNoeud(self, noeuds):
		aretesAAnalyser = []
		for noeud in noeuds:
			aretesAAnalyser + noeud.getAretes()
		return aretesAAnalyser

	######################################## AUTRES METHODES ###################################

	def addNoeud(self, noeud):
		self.noeuds.append(noeud)

	def addNoeuds(self, noeuds):
		for noeud in noeuds:
			self.addNoeud(noeud)

	def removeNoeud(self, noeud):
		self.noeuds.remove(noeud)

	def addArete(self, arete):
		self.aretes.append(arete)

	def addAretes(self, aretes):
		for arete in aretes:
			self.addArete(arete)

	def constructNoeuds(self, noeud, B):
		""" construit des noeuds en fonction d'un dictionnaire passé en paramètre"""
		dico = noeud.getConfig().getPossiblePosition()

		listNoeuds = []

		for objet in dico.keys(): # pour chaque véhicule
			for marqueur in dico[objet]: # pour chaque position possible du véhicule
				noeudToAdd = Noeud(self.newConfig(noeud.getConfig(), objet, marqueur)) # définition du noeud
				self.constructNoeud(noeud, noeudToAdd, B)
					
	def constructNoeud(self, noeudDefinitif, noeudToAdd, B):
		""" ajoute le noeud et l'arête correspondant dans le graphe si le noeud et l'arete ne sont pas déjà dans le graphe"""

		areteToAdd = Arete([noeudDefinitif, noeudToAdd], 1)
		if(not self.verifAreteInGraphe(areteToAdd)): # si arete inexistante
			self.addArete(areteToAdd)
			noeudToAdd.addArete(areteToAdd) # le noeud a une réference sur les aretes

		if(not self.verifNoeudInGraphe(noeudToAdd)): # si noeud inexistant
			noeudToAdd.setLongueurChemin(math.inf)
			self.addNoeud(noeudToAdd)
			B.append(noeudToAdd)

		


	def verifNoeudInGraphe(self, noeud):
		""" retourne vrai si le noeud est dans le graphe"""

		for n in self.getNoeuds():
			if(self.compare2Config(n.getConfig(), noeud.getConfig())):
				return True
		return False

	def verifAreteInGraphe(self, arete):
		""" retourne vrai si l'arete est dans le graphe"""
		noeud1, noeud2 = arete.getCoupleNoeud()
		for a in self.getAretes():
			if(self.compare2Aretes(a, arete)):
				return True
		return False

	####################################### METHODES STATIQUES #########################################

	@staticmethod
	def compare2Config(config1, config2):
		""" cette méthode retourne vrai si les 2 configurations données en paramètre sont identiques"""
		list1 = []
		list2 = []
		for vehicule in range(len(config1.getVehicules())):
			list1.append(config1.getVehicules()[vehicule].getMarqueur())
		for vehicule in range(len(config2.getVehicules())):
			list2.append(config2.getVehicules()[vehicule].getMarqueur())
		return (len(ListTools.intersection(list1, list2)) == len(config1.getVehicules()))

	@staticmethod
	def compare2Noeuds(noeud1, noeud2):
		""" cette fonction retourne vrai si les 2 noeuds donnés en paramètres ont la meme config"""
		return Graphe.compare2Config(noeud1.getConfig(), noeud2.getConfig())

	@staticmethod
	def compare2Aretes(arete1, arete2):
		""" cette fonction retourne vrai si les aretes données en paramètre sont identiques"""
		noeud11, noeud12 = arete1.getCoupleNoeud()
		noeud21, noeud22 = arete2.getCoupleNoeud()
		if(Graphe.compare2Noeuds(noeud11, noeud21) and Graphe.compare2Noeuds(noeud12, noeud22)):
			return True
		if(Graphe.compare2Noeuds(noeud12, noeud21) and Graphe.compare2Noeuds(noeud11, noeud22)):
			return True
		return False

	@staticmethod
	def isInList(noeud, listNoeud):
		""" retourne vrai si le noeud est dans la liste de noeud donnée en paramètre"""
		return True in [Graphe.compare2Noeuds(noeud, i) for i in listNoeud]

	@staticmethod
	def coupleNoeud(arete, noeudDefinitifs):
		""" cette fonction retourne les noeuds dans l'ordre suivant : noeud définitif, noeud non définitif pour l'arête donnée"""
		if(Graphe.isInList(arete.getCoupleNoeud()[0], noeudDefinitifs)):
			return arete.getCoupleNoeud()[0], arete.getCoupleNoeud()[1]
		return arete.getCoupleNoeud()[1], arete.getCoupleNoeud()[0]

	@staticmethod
	def getConfigCoupleNoeud(arete):
		""" retourne les configs des noeuds reliés par l'arete"""
		return arete.getCoupleNoeud()[0].getConfig(), arete.getCoupleNoeud()[1].getConfig()

	@staticmethod
	def newConfig(configInit, vehicle, newPosition):
		""" crée une nouvelle config à partir d'un véhicule et d'une nouvelle position, retourne la nouvelle config"""

		newConfig = copy(configInit)
		newVehicle = copy(vehicle)
		newVehicle.setMarqueur(newPosition)

		listVehicles = copy(configInit.getVehicules())

		listVehicles.remove(vehicle)
		listVehicles.append(newVehicle)

		newConfig.setVehicules(listVehicles)
		newConfig.constructConfiguration()

		return newConfig
