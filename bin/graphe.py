# -*- coding: utf-8 -*-

import math
from configuration import *
from copy import copy









class Noeud:

	def __init__(self, config):
		self.config = config
		self.id = Configuration.getStrConfig(config)
		self.longueurChemin = math.inf
		self.historique = []

	def getId(self):
		return self.id

	def getConfig(self):
		""" Retourne la configuration correpondant au noeud """
		return self.config

	def getLongueurChemin(self):
		""" retourne la longueur du chemin """
		return self.historique[-1][1]

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

	@staticmethod
	def compare2Noeuds(noeud1, noeud2):
		""" cette fonction retourne vrai si les 2 noeuds donnés en paramètres ont la meme config"""
		return noeud1.getId() == noeud2.getId()









class Graphe:

	def __init__(self):
		self.noeuds = []
		self.aretes = []

	############################### GETTERS ET SETTERS #########################################

	def getNoeuds(self):
		""" retourne la liste des noeuds du graphe"""
		return self.noeuds

	def getNoeud(self, config):
		""" retourne les noeuds selon la config donnée en paramètre"""
		return [item for item in self.noeuds if self.compare2Config(item.getConfig(), config)]

	######################################## AUTRES METHODES ###################################

	def addNoeud(self, noeud):
		self.noeuds.append(noeud)

	def addNoeuds(self, noeuds):
		[self.addNoeud(noeud) for noeud in noeuds]
			
	def removeNoeud(self, noeud):
		self.noeuds.remove(noeud)
			
	def constructNoeuds(self, noeud, B):
		""" construit des noeuds en fonction d'un dictionnaire passé en paramètre"""
		dico = noeud.getConfig().getPossiblePosition()
		# pour chaque véhicule, pour chaque position possible du véhicule
		[[self.constructNoeud(noeud, Noeud(self.newConfig(noeud.getConfig(), objet, marqueur)) , B) for marqueur in dico[objet]] for objet in dico.keys()]
						
	def constructNoeud(self, noeudDefinitif, noeudToAdd, B):
		""" ajoute le noeud et l'arête correspondant dans le graphe si le noeud et l'arete ne sont pas déjà dans le graphe"""
		if(not self.verifNoeudInGraphe(noeudToAdd)): # si noeud inexistant

			noeudToAdd.setHistorique([noeudDefinitif.getHistorique()] + [(noeudToAdd.getConfig(), noeudDefinitif.getLongueurChemin() + 1)])
			self.addNoeud(noeudToAdd)
			B.append(noeudToAdd)

	def verifNoeudInGraphe(self, noeud):
		""" retourne vrai si le noeud est dans le graphe"""
		for n in self.getNoeuds():
			if(Noeud.compare2Noeuds(n, noeud)):
				return True
		return False

	####################################### METHODES STATIQUES #########################################

	

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
