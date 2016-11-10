# -*- coding: utf-8 -*-

from configuration import *
from gurobipy import *


class LPSolver :
    """ 
        va définir les variables de contrainte nécessaires pour la résolution par PL. 
        Positions2Points : p[j][l] : ensemble des positions comprises entre j et l. -> TODO
        
    """

    def __init__(self, config):

        self.config = config
        self.nbMove = config.getNbCoupMax() # nombre de mouvements max autorisés
        
        self.model = Model()
        self.marqueurs = range(36)
        self.moves = range(self.nbMove+1)

        # correspond à v
        self.initLongueurs()
        # correspond à p
        self.initPosition2Points()
        # correspond à m
        self.initPositionsVehicules()
        # créé x, y, z et les initialise selon la configuration passée en param
        self.createDecisionsVariables()
        # défini la fonction objectif
        self.createObjective()


    def definePossiblesPositions(self):
        """ Créé une liste des positions possibles que peut prendre chaque véhicule """
            self.possiblesPositions = {}
            for vehicule in self.config.getVehicules():
                idVehicule = vehicule.getIdVehicule()
                orientation = vehicule.getOrientation()

                start = vehicule.getMarqueur()%6 if orientation == Orientation.BAS else vehicule.getMarqueur()//6 # peut être l'inverse, à verifier.
                self.possiblesPositions[idVehicule] = list(range(start, start + 5*orientation))

    def createDecisionsVariables(self):
        """ Créé l'ensemble des variables de décisions nécessaires à la résolution du problème. """
        self.x, self.y, self.z = {}, {}, {}

        for vehicule in self.config.getVehicules():
            # Création de toutes les variables de décision associé au véhicule 
            idVehicule = vehicule.getIdVehicule()
            self.x[idVehicule] = [[self.model.addVar(vtype=GRB.BINARY) for k in self.moves] for j in self.possiblesPositions[idVehicule]]
            self.z[idVehicule] = [[self.model.addVar(vtype=GRB.BINARY) for k in self.moves] for j in self.possiblesPositions[idVehicule]]
            self.y[idVehicule] = [[[self.model.addVar(vtype=GRB.BINARY) for k in self.moves] for i in self.possiblesPositions[idVehicule] if i != j] for j in self.possiblePositions[idVehicule]]
            self.model.update()

    def createObjective(self, objectiveType="RHM"):
        """ Défini l'objectif du modèle en fonction du type d'objectif passé en paramètre.
            L'objectif est soit de type "RHM", minimisant le nombre de mouvement, soit de type "RHC", minimisant le nombre de case parcourue.
        """
        objective = LinExpr()
        # A OPTIMISER, Développer rapidement parceque flemme et envie de jouer (présaison open omg too op ggwp rito)
        for vehiculeList in self.y.values():
            for j,marqueurList in enumerate(vehiculeList):
                for l,deplList in enumerate(marqueurList):
                    for movementVariable in deplList:
                        coeff = 1 if objectiveType == "RHM" else len(self.positionEntre2Points(j,l))
                        objective.addTerms(coeff, movementVariable)

        self.model.setObjective(objective, GRB.MINIMIZE)


    def createConstraints(self):
        """ Créé l'ensemble des contraintes nécéssaire à la résolution de la configuration RushHour """
        self.addPositonVehiculeConstraints() # contraintes de type 3
        self.addFreeSpaceMovementConstraints() # contrainte de type 4






    def initLongueurs(self):
        """ Défini la longueur de tous les véhicules de config

            Paramètres : 
                - une configuration des voitures
        """
        self.longueurs = {}
        for vehicule in self.config.getVehicules():
            self.longueurs[vehicule.getIdVehicule()] = vehicule.getTypeVehicule()

    def getLongueurs(self):
        """ Renvoie la longueur de tous les véhicules de config"""
        return self.longueurs


    def initPositionsVehicules(self):
        """ Pour chaque véhicule et pour chaque case, défini toutes les cases occupées

            Paramètres : 
                    - une configuration des voitures
        """
        self.positionsVehicules = {}
        for vehicle in self.config.getVehicules():
            currentList = []
            # pour chaque positions de la grille
            for j in range(36):
                positions = []
                indexMax = vehicle.getOrientation() * vehicle.getTypeVehicule()
                # si le véhicule ne sort pas de la grille
                if (j + indexMax <36):
                    positions = self.position2Points[j][j + indexMax]
                currentList.append(positions)

            self.positionsVehicules[vehicle.getIdVehicule()] = positions

    def getPositionsVehicules(self):
        """ Renvoie la liste de toutes les cases occupées pour un véhicule et une case donnée """
        return self.positionsVehicules

    def initPosition2Points(self):
        """ Défini la matrice p[][] qui contient pour tout i,j l'ensemble des positions entre ces deux marqueurs.
            Si les cases ne sont pas alignées verticalement ou horizontalement, le tableau renverra une liste vide pour la case correspondante
        """
        self.position2Points = []
        for i in range(36):
            currentList = []
            for j in range(36):
                positions = []
                step = 0
                # si les 2 points sont alignés horizontalement
                if(i//6 == j//6):
                    step = 1

                # si les deux points sont alignés verticalement
                elif(i%6 == j%6):
                    step = 6

                # pour parcourir dans l'autre sens si j est avant i
                coef = 1 if i<=j else -1

                # si les deux points sont alignés verticalement ou horizontalement
                if(step !=0):
                    for k in range(i, j + (1 * coef), step * coef):
                        positions.append(k) # on ajoute chaque point compris entre i et j

                currentList.append(positions)
            self.position2Points.append(currentList)


    def getPositions2Points(self):
        """ retourne un tableau [pour toutes les cases j][pour toutes les cases l] qui est l'ensemble des positions comprises entre j et l."""
        return self.positions2Points


    def addPositonVehiculeConstraints(self):
        """ Ajoute l'ensemble des contraintes forçant le fait que pour chaque véhicule i et à chaque tour k, il y a longueur du véhicule i variables de décisions z[i][j][k] à 1. """
        for vehicule in self.config.getVehicules():
            for move in self.moves:
                self.model.addConstr(quicksum((self.z[vehicule.getIdVehicule()][j][move] for j in self.marqueurs)), GRB.EQUAL, self.longueurs(idVehicule))

    def addFreeSpaceMovementConstraints(self):
        """ Ajoute l'ensemble des contraintes exprimant le fait que chaque véhicule i qui se déplace de j à l au tour k ne peut le faire que s'il n'existe aucune gène entre j et l """
        
        # TROUVER UN MOYEN D'OPTIMISER LES BOUCLES IMBRIQUEES
        for currentVehicule in self.y.keys():
            for j in possiblePositions[idVehicule]:
                for l in (l in possiblePossitions[idvehicule] if l!=j):
                    for k in moves:
                        for p in self.Positions2Points(j,l):
                            self.model.addConstr(self.y[currentVehicule][j][l][k], GRB.LESS_EQUAL, 1 - quicksum([self.z[idVehicule][p][k-1] for idVehicule in self.y.keys() if idVehicule != currentVehicule]))

def main():
# if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/avancé/jam30.txt")
    conf.setNbCoupMax(10)
    lp = LPSolver(conf)
    # [print(pl.getMatricePresence()[i]) for i in range(len(pl.getMatricePresence()))]
    # [print(pl.getMatriceOccupe()[i]) for i in range(len(pl.getMatriceOccupe()))]
    # print(pl.getPositions2Points())
    # [print(pl.getPositionsVehicules()[i]) for i in range(len(pl.getPositionsVehicules()))]

main()