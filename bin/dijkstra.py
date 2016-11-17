# -*- coding: utf-8 -*-

import math
from copy import copy

from configuration import *

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


class Noeud:

	def __init__(self, config):
		self.config = config
		self.longueurChemin = math.inf
		self.historique = []

	def getConfig(self):
		""" Retourne l'identifiant du noeud """
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
		""" modifie complètement l'historique du noeud"""
		self.historique = historique

	def addHistorique(self, element):
		""" ajoute un élément à l'historique du noeud"""
		self.historique.append(element)


class Graphe:

	def __init__(self):
		self.noeuds = []
		self.aretes = []

	def getNoeuds(self):
		return self.noeuds

	def getAretes(self):
		return self.aretes

	def getNoeud(self, config):
		return [item for item in self.noeuds if item.getConfig() == config]

	def getArete(self, coupleNoeuds):
		for item in self.aretes:
			verif1 = Dijkstra.compareDeuxConfig(item.getCoupleNoeud()[0].getConfig(), coupleNoeuds[0].getConfig()) and Dijkstra.compareDeuxConfig(item.getCoupleNoeud()[1].getConfig(), coupleNoeuds[1].getConfig())
			verif2 = Dijkstra.compareDeuxConfig(item.getCoupleNoeud()[0].getConfig(), coupleNoeuds[1].getConfig()) and Dijkstra.compareDeuxConfig(item.getCoupleNoeud()[1].getConfig(), coupleNoeuds[0].getConfig())
			if (verif1 or verif2) :
				return item
		return []

	def getAretesFromNoeud(self, noeudsDefinitifs):
		aretesAAnalyser = []
		for item in self.aretes:
			if (item.getCoupleNoeud()[0] in noeudsDefinitifs and item.getCoupleNoeud()[1] not in noeudsDefinitifs) or (item.getCoupleNoeud()[1] in noeudsDefinitifs and item.getCoupleNoeud()[0] not in noeudsDefinitifs):
				aretesAAnalyser.append(item)
		return aretesAAnalyser

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

	@staticmethod
	def argminArete(listOfAretes):
		poidsMin = 0
		for item in listOfAretes:
			if poidsMin>item.getPoids():
				poidsMin = item.getPoids()
		return poidsMin

	@staticmethod
	def NoeudOppose(noeud, arete):
		if(arete.getCoupleNoeud()[0]==noeud):
			return arete.getCoupleNoeud()[0]
		else:
			return arete.getCoupleNoeud()[1]

	@staticmethod
	def coupleNoeud(arete):
		""" cette fonction retourne les noeuds dans l'ordre suivant : noeud définitif, noeud non définitif pour l'arête donnée"""
		return arete.getCoupleNoeud()[0], arete.getCoupleNoeud()[1]

class Dijkstra:
	""" première version de l'algo, peu optimisée, et n'enregistrant pas encore l'historique du chemin parcouru, affiche le poids min trouvé """

	def __init__(self):
		self.graphe = Graphe()
		self.A = [] # correspond aux noeud dont un chemin de longueur définitive a été trouvé

	def launchDijkstra(self, config, nbMax):

		dernierNoeudVisite = Noeud(config) 
		self.A.append(dernierNoeudVisite)
		self.graphe.addNoeud(dernierNoeudVisite)
		
		# on fixe la longueur du chemin au noeud de départ à 0
		dernierNoeudVisite.setLongueurChemin(0)

		# tant qu'on a pas un chemin définitif vers l'objectif ou dépassé le nb de coup max
		while(not Dijkstra.verifCondition(dernierNoeudVisite)):

			# dictionnaire stockant pour chaque véhicule, la liste de ses mvts possibles
			dicoNoeudsPotentiels = dernierNoeudVisite.getConfig().getPossiblePosition() 

			# complétion de l'arbre à partir du dernier noeud ajouté (le reste n'a pas besoin d'être modifié, et reste fixe)
			if(dernierNoeudVisite.getLongueurChemin()<nbMax):
				self.constructNoeuds(dernierNoeudVisite, dicoNoeudsPotentiels)

			# liste des arêtes dont on cherche à déterminer le poids min
			listOfAretes = self.graphe.getAretesFromNoeud(self.A)

			#initialisation des variables utilisées dans l'algo
			currentNoeudA = None # noeud de liste A considéré
			currentNoeudnotA = None # noeud considéré pas dans A
			currentNoeudMin = None # noeud de poids min considéré

			poidsMin = math.inf # poids du chemin minimum

			for arete in listOfAretes:

				currentNoeudMin = currentNoeudnotA # initialisation si aucune amélioration de longueur

				# on prend, pour l'arete courant, les deux noeuds reliés
				currentNoeudA, currentNoeudnotA = self.graphe.coupleNoeud(arete)

				# si le chemin en passant par cette arête est plus petit que ceux obtenus avant

				if((currentNoeudA.getLongueurChemin() + arete.getPoids()) < poidsMin):
					poidsMin = currentNoeudA.getLongueurChemin() + arete.getPoids()
					currentNoeudMin = currentNoeudnotA

				# si le chemin jusqu'à ce noeud est plus petit que celui déjà enregistré
				if((currentNoeudA.getLongueurChemin() + arete.getPoids()) < currentNoeudnotA.getLongueurChemin()):
					
					currentNoeudnotA.setLongueurChemin(currentNoeudA.getLongueurChemin() + arete.getPoids())
					# ici pour modifier historique ---> prochaine itération

			dernierNoeudVisite = currentNoeudMin

			# on ajoute le noeud de chemin min à la liste définitive des chemins
			self.A.append(dernierNoeudVisite)
			# print("poids chemin considéré : ", dernierNoeudVisite.getLongueurChemin())
			# print(dernierNoeudVisite.getConfig().getConfiguration())

		print("\nlongueur minimale trouvée : ", dernierNoeudVisite.getLongueurChemin(), "\n")

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

	@staticmethod
	def verifCondition(noeud):
		""" si le noeud sélectionné permet de conclure qu'on a fini, ie voiture "g" en position 17"""
		config = noeud.getConfig()
		vehicules = config.getVehicules()
		vehiculeG = None
		for vehicule in vehicules:
			if(vehicule.getIdVehicule() == 'g'): # -------> A modifier par la suite
				vehiculeG = vehicule
		if(vehiculeG.getMarqueur() == 17):
			return True
		return False

	def constructNoeuds(self, noeud, dico):
		listNoeuds = []
		
		for vehicule in dico.keys(): # pour chaque véhicule

			if(dico[vehicule] != None): # si mouvements possibles pour le véhicule

				for marqueurPossible in dico[vehicule]: # pour chaque position possible du véhicule
					noeudToAdd = Noeud(Dijkstra.newConfig(noeud.getConfig(), vehicule, marqueurPossible)) # définition du noeud

					if(not Dijkstra.compareDeuxConfig(noeudToAdd.getConfig(), noeud.getConfig())): # si noeud inexistant
						noeudToAdd.setLongueurChemin(math.inf) # chemin fixé au max
						self.graphe.addNoeud(noeudToAdd) # chemin ajouté au graphe
					else:
						print("test")

					if(self.graphe.getArete([noeudToAdd, noeud]) == []): # si arete inexistante
						self.graphe.addArete(Arete([noeud, noeudToAdd], 1)) # arete ajoutée au graphe avec aret1 dans A, l'autre non



	@staticmethod
	def compareDeuxConfig(config1, config2):
		list1 = []
		list2 = []
		for vehicule in range(len(config1.getVehicules())):
			list1.append(config1.getVehicules()[vehicule].getMarqueur())
		for vehicule in range(len(config2.getVehicules())):
			list2.append(config2.getVehicules()[vehicule].getMarqueur())
		return (len(ListTools.intersection(list1, list2)) == len(config1.getVehicules()))


def main():

	dijkstra = Dijkstra()
	conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
	print(conf)

	noeud = Noeud(conf)
	dijkstra.launchDijkstra(conf, 8)


main()






