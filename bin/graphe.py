# -*- coding: utf-8 -*-

import math
from configuration import *









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

	def setLongueurChemin(self, longueurChemin):
		self.historique[-1][1] = longueurChemin

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


	def getNoeuds(self):
		""" retourne la liste des noeuds du graphe"""
		return self.noeuds


	def addNoeud(self, noeud):
		self.noeuds.append(noeud)
			

	def constructNoeuds(self, noeud, B, flag = "RHM"):
		""" construit des noeuds en fonction d'un dictionnaire passé en paramètre"""

		dico = noeud.getConfig().getPossiblePosition()
		poids = 1

		# pour chaque véhicule, pour chaque position possible du véhicule
		for objet in dico.keys():

			listVehicules = noeud.getConfig().getVehicules()
			marqueurObjet = listVehicules[listVehicules.index(objet)].getMarqueur()
			orientationObjet = listVehicules[listVehicules.index(objet)].getOrientation()

			for marqueur in dico[objet]:

				if(flag != "RHM"):
					poids = abs(marqueurObjet - marqueur)/orientationObjet

				n = self.verifNoeudInGraphe(Noeud(Configuration.newConfig(noeud.getConfig(), objet, marqueur)))

				if(len(n.getHistorique()) == 0): # si le noeud n'a jamais été crée
					self.constructNoeud(noeud, n, B, poids)

				elif(n.getLongueurChemin() > noeud.getLongueurChemin() + poids): # si noeud déjà créé et chemin plus petit possible
					n.setLongueurChemin(noeud.getLongueurChemin() + poids)
				

	def constructNoeud(self, noeudDefinitif, noeudToAdd, B, poids):
		""" ajoute le noeud et l'arête correspondant dans le graphe si le noeud et l'arete ne sont pas déjà dans le graphe"""
		noeudToAdd.setHistorique(noeudDefinitif.getHistorique() + [[noeudToAdd.getConfig(), noeudDefinitif.getLongueurChemin() + poids]])
		self.addNoeud(noeudToAdd)
		B.append(noeudToAdd)


	def verifNoeudInGraphe(self, noeud):
		""" retourne vrai si le noeud est dans le graphe"""# revoir commentaire
		for n in self.getNoeuds():
			if(Noeud.compare2Noeuds(n, noeud)):
				return n
		return noeud