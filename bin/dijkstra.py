# -*- coding: utf-8 -*-

import math

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

	def __init__(self, identifiant):
		self.identifiant = identifiant
		self.longueurChemin = math.inf

	def getId(self):
		""" Retourne l'identifiant du noeud """
		return self.identifiant

	def setId(self, identifiant):
		""" Modifie l'identifiant du noeud par celui donné en paramètre """
		self.identifiant = identifiant

	def setLongueurChemin(self, longueurChemin):
		""" modifie la longueur du chemin par celle donnée en paramètre """
		self.longueurChemin = longueurChemin

	def getLongueurChemin(self):
		""" retourne la longueur du chemin """
		return self.longueurChemin


class Graphe:

	def __init__(self):
		self.noeuds = []
		self.aretes = []

	def getNoeuds(self):
		return self.noeuds

	def getAretes(self):
		return self.aretes

	def getNoeud(self, identifiant):
		return [item for item in self.noeuds if item.getId == identifiant]

	def getArete(self, coupleNoeuds):
		return [item for item in self.aretes if item.getCoupleNoeud == coupleNoeuds]

	def getAretesFromNoeud(self, noeudsDefinitifs, noeudsAAtteindre):
		aretesAAnalyser = []
		for item in self.aretes:
			if (item.getCoupleNoeud()[0] in noeudsDefinitifs and item.getCoupleNoeud()[1] in noeudsAAtteindre) or (item.getCoupleNoeud()[1] in noeudsDefinitifs and item.getCoupleNoeud()[0] in noeudsAAtteindre):
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
	def coupleNoeud(listOfNoeudDefinitifs, arete):
		if arete.getCoupleNoeud()[0] in listOfNoeudDefinitifs:
			return arete.getCoupleNoeud()[0], arete.getCoupleNoeud()[1]
		else:
			return arete.getCoupleNoeud()[1], arete.getCoupleNoeud()[0]


class Dijkstra:
	""" première version de l'algo, peu optimisée, et n'enregistrant pas encore l'historique du chemin parcouru, affiche le poids min trouvé """

	def __init__(self, graphe, noeudDepart, noeudObjectif):
		self.graphe = graphe
		self.noeudsVisitesDefinitifs = [noeudDepart]
		self.noeudsNonDefinitifs = self.graphe.noeuds
		self.noeudsNonDefinitifs.remove(noeudDepart)
		self.launchDijkstra(noeudDepart, noeudObjectif)

	def launchDijkstra(self, noeudDepart, noeudObjectif):
		
		# on fixe la longueur du chemin au noeud de départ à 1
		noeudDepart.setLongueurChemin(0)

		# tant qu'on a pas un chemin définitif vers le noeud objectif
		while(noeudObjectif not in self.noeudsVisitesDefinitifs):

			# liste des arêtes dont on cherche à déterminer le poids min
			listOfAretes = self.graphe.getAretesFromNoeud(self.noeudsVisitesDefinitifs, self.noeudsNonDefinitifs) 
			#initialisation des variables utilisées dans l'algo
			noeudCheminMin = None
			currentNoeudDefinitif = None
			currentNoeud = None

			poidsMin = math.inf

			for arete in listOfAretes:
				# on prend, pour l'arete courant, les deux noeuds reliés
				currentNoeudDefinitif, currentNoeud = self.graphe.coupleNoeud(self.noeudsVisitesDefinitifs, arete)

				# si le chemin en passant par cette arête est plus petit que ceux obtenus avant
				if((currentNoeudDefinitif.getLongueurChemin() + arete.getPoids()) < poidsMin):
					poidsMin = currentNoeudDefinitif.getLongueurChemin() + arete.getPoids()
					noeudCheminMin = currentNoeud

				# si le chemin jusqu'à ce noeud est plus petit que celui déjà enregistré
				if((currentNoeudDefinitif.getLongueurChemin() + arete.getPoids()) < currentNoeud.getLongueurChemin()):
					currentNoeud.setLongueurChemin(currentNoeudDefinitif.getLongueurChemin() + arete.getPoids())

			# on ajoute le noeud de chemin min à la liste définitive des chemins, et on l'enlève de la liste non définitive
			self.noeudsVisitesDefinitifs.append(noeudCheminMin)
			self.noeudsNonDefinitifs.remove(noeudCheminMin)
			print("chemin ajouté à la liste définitive : ", noeudCheminMin.getId(), "avec un chemin de longueur minimale : ", noeudCheminMin.getLongueurChemin())

		print("\nlongueur minimale trouvée : ", poidsMin, "\n")


def main():

	noeud1 = Noeud("Noeud1")
	noeud2 = Noeud("Noeud2")
	noeud3 = Noeud("Noeud3")
	noeud4 = Noeud("Noeud4")
	arete_noeud1_noeud2 = Arete([noeud1, noeud2], 3)
	arete_noeud1_noeud3 = Arete([noeud1, noeud3], 2)
	arete_noeud2_noeud4 = Arete([noeud2, noeud4], 10)
	arete_noeud3_noeud4 = Arete([noeud3, noeud4], 25)
	graphe = Graphe()
	graphe.addNoeuds([noeud1, noeud2, noeud3, noeud4])
	graphe.addAretes([arete_noeud1_noeud2, arete_noeud1_noeud3, arete_noeud3_noeud4, arete_noeud2_noeud4])

	Dijkstra(graphe, noeud1, noeud4)

main()






