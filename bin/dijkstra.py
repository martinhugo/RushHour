# -*- coding: utf-8 -*-

import math
import time

from configuration import *
from graphe import *



class Dijkstra:
    """ Cette classe permet la résolution d'une grille de RushHour par l'algorithme de Dijkstra"""
    
    def __init__(self, config, flag, nbMax):
        """ Initialise l'ensemble des paramètres nécessaire à l'algorithme de Dijkstra 
            Params : 
                config -> la configuration initiale
                nbMax -> le nombre maximum de déplacements autorisés
                flag (facultatif) -> objectif de résolution, par défaut sur RHM
        """
        self.graphe = Graphe()
        self.config = config
        self.problem = flag
        self.nbMax = nbMax
        self.nonDefinitiveEdges = [] # correspond aux noeuds de chemin non définitif


    def getConfig(self):
        """ Retourne la configuration """
        return self.config

    def getNbMax(self):
        """ Retourne le nombre de mouvement maximum """
        return self.nbMax

    def getSolution(self):
        """ Retourne la solution trouvée par l'algorithme """
        return self.solution

    def solve(self):
        """ Cette méthode permet la résolution de la grille de RushHour par Dijkstra
            La résolution peut être faite selon RHM ou RHC selon la valeur de l'attribut self.problem
            Return : liste des configurations permettant de résoudre la grille de RushHour
        """
        start_time = time.time()

        noeudsPoidsMin = Noeud(self.getConfig()) # correspond au noeud initial
        noeudsPoidsMin.setHistorique([None, 0, 0]) # historique de ce noeud, sans parent, avec un chemin de 0 et une profondeur de 0
        self.graphe.addNoeud(noeudsPoidsMin) # ajout du noeud dans le graphe
        self.nonDefinitiveEdges.append(noeudsPoidsMin) # ajout du premier noeud dans nonDefinitiveEdges (tant que pas dans la boucle, pas définitif)

        while(not noeudsPoidsMin == None and not Configuration.verifCondition(noeudsPoidsMin.getConfig()) and self.getNbMax() > noeudsPoidsMin.getProfondeur()):

            self.nonDefinitiveEdges.remove(noeudsPoidsMin) # on retire le noeud définitif de nonDefinitiveEdges
            self.graphe.constructNoeuds(noeudsPoidsMin, self.nonDefinitiveEdges, self.problem) # ajout des noeuds inexistants et maj de la taille du chemin

            # initialisation
            poidsMin = math.inf
            noeudCheminMin = None

            for noeud in self.nonDefinitiveEdges: # pour chaque noeud dans nonDefinitiveEdges
                if(noeud.getLongueurChemin() < poidsMin):
                    poidsMin = noeud.getLongueurChemin() # on garde le poids min
                    noeudCheminMin = noeud # on garde le noeud non définitif de poids min

            noeudsPoidsMin = noeudCheminMin # on récupère le chemin le plus court et on itère

        stop_time = time.time()
        print("temps total ---->", round(stop_time - start_time, 2), " sec")

        # si on a trouvé une solution
        if (noeudsPoidsMin is not None) and (self.getNbMax() >= noeudsPoidsMin.getProfondeur()):

            listConfig = [noeudsPoidsMin.getConfig()]
            while(noeudsPoidsMin.getParent() != None):
                noeudsPoidsMin = noeudsPoidsMin.getParent()
                listConfig.append(noeudsPoidsMin.getConfig())
            return listConfig

        # si la solution ne peut être trouvé en nombre de pas
        else:
            return []



if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/contre_exemple_RHM_RHC.txt")
    dijkstra = Dijkstra(conf, "RHC", 52)
    print(len(dijkstra.getSolution()))
    # dijkstra.launchDijkstra(conf, 35, flag = "RHM")
    # print("nombre de configurations atteignables en 1 pas -->", Graphe.countConfig(conf, 1))
