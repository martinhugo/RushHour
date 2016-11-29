# -*- coding: utf-8 -*-

import math
import time

from configuration import *
from graphe import *

class Dijkstra:
    """ """

    def __init__(self, config, nbMax, flag = "RHM"):
        self.graphe = Graphe()
        self.config = config
        self.nbMax = nbMax
        self.nonDefinitiveEdges = [] # correspond aux noeuds de chemin non définitif
        self.solution = self.solve(flag)


    def getConfig(self):
        return self.config

    def getNbMax(self):
        return self.nbMax

    def getSolution(self):
        return self.solution

    def solve(self, flag = "RHM"):
        """ Retourne la liste des configurations permettant de résoudre la configuration.
            Cette configuration est retournée par l'algorithme de Dijkstra
            La résolution peut être faite selon RHM ou RHC selon la valeur du flag.
        """
        start_time = time.time()

        noeudsPoidsMin = Noeud(self.getConfig())
        noeudsPoidsMin.setHistorique([[self.getConfig(), 0]])
        self.graphe.addNoeud(noeudsPoidsMin) # ajout du noeud dans le graphe
        self.nonDefinitiveEdges.append(noeudsPoidsMin) # ajout du premier noeud dans B (tant que pas dans la boucle, pas définitif)

        i = 0
        while (not noeudsPoidsMin is None and not Configuration.verifCondition(noeudsPoidsMin.getConfig()) and self.getNbMax() > (len(noeudsPoidsMin.getHistorique())-1)):
            self.nonDefinitiveEdges.remove(noeudsPoidsMin) # on retire le noeud définitif de B
            self.graphe.constructNoeuds(noeudsPoidsMin, self.nonDefinitiveEdges, flag) # ajout des noeuds inexistants et maj de la taille du chemin

            # initialisation
            poidsMin = math.inf
            noeudCheminMin = None

            ###????? j'ai besoin d'une explication
            for noeud in self.nonDefinitiveEdges: # pour chaque noeud dans B
                if(noeud.getLongueurChemin() < poidsMin):
                    poidsMin = noeud.getLongueurChemin()
                    noeudCheminMin = noeud

            noeudsPoidsMin = noeudCheminMin # on récupère le chemin le plus court et on itère

        stop_time = time.time()
        print("temps total ---->", round(stop_time - start_time, 2), " sec", i)

        # si on a trouvé une solution
        if (noeudsPoidsMin is not None) and (self.getNbMax() >= len(noeudsPoidsMin.getHistorique())):
            listConfig = [noeudsPoidsMin.getHistorique()[i][0] for i in range(len(noeudsPoidsMin.getHistorique()))]
            listConfig.reverse()
            return listConfig   # si on a pas trouvé de solution en un nombre de pas < nbMax

        # si la solution ne peut être trouvé en nombre de pads
        else:
            return []


if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/débutant/jam2.txt")
    dijkstra = Dijkstra(conf, 52, flag = "RHM")
    print(len(dijkstra.getSolution()))
    # dijkstra.launchDijkstra(conf, 35, flag = "RHM")
    # print("nombre de configurations atteignables en 15 pas -->", Graphe.countConfig(conf, 15))






