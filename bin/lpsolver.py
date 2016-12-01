# -*- coding: utf-8 -*-
import time
from configuration import *
from configuration import *
from gurobipy import *


class LPSolver :
    """ Cette classe permet la résolution d'une grille de RushHour par programmation linéaire. """

    def __init__(self, config, resolutionProblem, nbCoupMax):
        """ 
            params : config -> configuration initiale de la grille
                     nbCoupMax -> nombre de coups max autorisés pour résoudre la grille
        """
        
        self.config = config 
        self.nbMove = nbCoupMax
        self.problem = resolutionProblem

        self.model = Model()

        self.moves = range(self.nbMove+1)
        self.marqueurs = range(36)

        self.initArrays()
        print(self.idVehiculesList)
        self.createDecisionsVariables()
        self.createObjective()
        self.createConstraints()


    def solve(self):
        """ Demande la résolution du modèle et écrit l'ensemble des variables valeurs de y[i][j][k][l] dans le fichier de chemin path """
        start_time = time.time()
        self.model.optimize()
        print(time.time() - start_time)
        return self.createConfigurations()

    def createConfigurations(self):
        """ cette fonction créé l'ensemble des configurations, de la configuration initiale à la configuration finale
            Params : None
            Return : la liste des configurations de la configuration initiale à la configuration finale 
            qui propose une solution optimale du problème
        """ 

        config = self.config
        listOfConfig = [config]

        for k in self.moves: # pour chaque mouvement k
            for idVehicule in self.idVehiculesList: # pour chaque véhicule idVehicule
                for j in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible j de idVehicule
                    for l in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible l différent de j
                        if j != l:
                            if self.y[idVehicule, j, l, k].X == 1:
                                ids = [config.getVehicules()[n].getIdVehicule() for n in range(0, len(config.getVehicules()))]
                                index = ids.index(idVehicule) # indice correspondant à la voiture concernée
                                config = Configuration.newConfig(config, config.getVehicules()[index], l)
                                listOfConfig.append(config)

        listOfConfig.reverse()
        return listOfConfig




####################################### Méthodes d'initialisations ####################################### 


    def initArrays(self):
        """ Initialise l'ensemble des tableaux et matrices nécessaires à l'établissement des variables, 
        contraintes et de la fonction objectif 
            Params : None
            Return : None
        """
        self.initIdVehiculesList()
        self.initPossiblesPositions() # créé x, y, z et les initialise selon la configuration passée en param
        self.initLongueurs() # correspond à v
        self.initPositions2Points() # correspond à p
        self.initPositionsVehicules() # correspond à m   
        


    def createDecisionsVariables(self):
        """ Créé l'ensemble des variables de décisions nécessaires à la résolution du problème.
            Les variables sont contenues dans des dictionnaires x, y, et z conformément aux notations de l'énoncé.
            Params : None
            Return : None
        """
        self.x, self.y, self.z = {}, {}, {}

        for vehicule in self.config.getVehicules(): # pour chaque véhicule
            idVehicule = vehicule.getIdVehicule()

            for k in self.moves: # pour chaque étape k 
                for j in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible j du véhicule

                    # variable de décision indiquant si le véhicule est en position j au terme de la k-eme étape
                    self.x[idVehicule, j, k] = self.model.addVar(0, 1, vtype=GRB.BINARY)

                    for l in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur différent de j
                        if j!=l:

                            # variable de décision indiquant si le véhicule est passé de la position j à la position l au terme de la k-eme étape
                            self.y[idVehicule, j, l, k] = self.model.addVar(0, 1, vtype=GRB.BINARY)

                for j in self.possiblesPositions[idVehicule]:

                    # variable de décision indiquant si le véhicule occupe la position j au terme de la k-eme étape
                    self.z[idVehicule, j, k] = self.model.addVar(0, 1, vtype=GRB.BINARY)
        
        self.model.update()

    def createObjective(self):
        """ Défini l'objectif du modèle en fonction du type d'objectif passé en paramètre.
            L'objectif est soit de type "RHM", minimisant le nombre de mouvement, soit de type "RHC", minimisant le nombre de case parcourue.
            Params : objectiveType (facultatif) -> le type de l'objectif, étant par défaut sur RHM
            Return : None
        """

        objective = LinExpr()
        
        for idVehicule in self.idVehiculesList: # pour chaque véhicule
            for k in self.moves: # pour chaque étape k
                for j in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible j du véhicule 
                    for l in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible du véhicule différent de j
                        if j != l:
                            # si l'objectif est RHM, le poids de chaque mouvement est de 1, sinon, du nombre de cases de déplacement
                            coeff = 1 if self.problem == "RHM" else (len(self.positions2Points[j][l]) - 1) # Ne pas compter les deux points courants. MODIFIER POSITIONS 2 POINTS?
                            objective.addTerms(coeff, self.y[idVehicule, j, l, k])

        # pour empêcher à la résolution de trouver que ne pas résoudre le problème est plus optimisé que de le résoudre
        coeff = self.nbMove if self.problem == "RHM" else 6*self.nbMove

        # minimisation de l'objectif
        self.model.setObjective(coeff*(1-self.x["g", 16, self.nbMove]) + objective, GRB.MINIMIZE)
        self.model.update()


    def createConstraints(self):
        """ Appelle l'ensemble des méthodes permettant la création de l'ensemble des contraintes nécéssaire à la résolution de la configuration RushHour 
            Params : None
            Return : None
        """

        self.addInitialisationConstraints() # contraintes d'initialisations
        self.addPositionConstraints() # contraintes de type 1, 2 et 3 (de l'énoncé)
        self.addMovementConstraints() # contraintes de type 4, 5, 6, 7 (de l'énoncé)
        self.model.update()




#######################################   Définition des tableaux d'attributs ####################################### 
    
    def initIdVehiculesList(self):
        """ Créé la liste des ids de véhicules 
            Params : None
            Return : None
        """ 
        self.idVehiculesList = [vehicule.getIdVehicule() for vehicule in self.config.getVehicules()]

    def initPossiblesPositions(self):
        """ Créé une liste des positions possibles que peut prendre chaque véhicule 
            Params : None
            Return : None
        """
        self.possiblesPositions = {}
        self.possiblesMarqueurs = {}

        for vehicule in self.config.getVehicules(): # pour chaque véhicule

            idVehicule = vehicule.getIdVehicule() # on stocke son identifiant
            orientation = vehicule.getOrientation() # on stocke son orientation (1 si horizontal, 6 si vertical)
            typeVehicule = vehicule.getTypeVehicule() # on stocke son type (camion ou voiture)

            # récupération du début de la ligne ou de la colonne dépendant de l'orientation de la voiture
            start = vehicule.getMarqueur()%6 if orientation == Orientation.BAS else vehicule.getMarqueur()//6 * Orientation.BAS 

            # définition de l'ensemble des positions possibles et de l'ensemble des marqueurs possibles de la voiture
            self.possiblesPositions[idVehicule] = list(range(start, start + 5*orientation + 1, orientation))
            self.possiblesMarqueurs[idVehicule] = list(range(start, start + (5 - (typeVehicule - 1))*orientation + 1, orientation))

    def initLongueurs(self):
        """ Défini la longueur de tous les véhicules de config
            Params : None
            Return : None
        """
        self.longueurs = {}
        for vehicule in self.config.getVehicules():
            self.longueurs[vehicule.getIdVehicule()] = vehicule.getTypeVehicule()

    def getLongueurs(self):
        """ Renvoie la longueur de tous les véhicules de config
            Params :None
            Return : le dictionnaire associant à chaque véhicule sa taille
        """
        return self.longueurs


    def initPositionsVehicules(self):
        """ défini toutes les cases occupées pour chaque véhicule et pour chaque case occupée par ce véhicule
            Params : None
            Return : None
        """
        self.positionsVehicules = {}
        for vehicle in self.config.getVehicules(): # pour chque véhicule

            currentList = {}
            idVehicule = vehicle.getIdVehicule() # on stocke l'identifiant du véhicule
            
            for j in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur j possible du véhicule
                positions = []
                indexMax = vehicle.getOrientation() * (vehicle.getTypeVehicule() -1) # on stocke l'indice maximum de la case occupée par le véhicule

                # si le véhicule ne sort pas de la grille
                if (j + indexMax < 36):
                    positions = self.positions2Points[j][j + indexMax] # on stocke l'ensemble des positions occupées par le véhicule en position j
                    
                currentList[j] = positions
            self.positionsVehicules[vehicle.getIdVehicule()] = currentList

    def getPositionsVehicules(self):
        """ Renvoie la liste de toutes les cases occupées pour un véhicule et une case donnée 
            Params : None
            Return : le dictionnaire associant l'ensemble des véhicules à l'ensemble des cases occupées par ce véhicule pour une case donnée"""
        return self.positionsVehicules

    def initPositions2Points(self):
        """ Défini la matrice p[][] qui contient pour tout i,j l'ensemble des positions entre ces deux marqueurs.
            Params : None
            Return : None
        """
        self.positions2Points = []
        for i in range(36): # pour chaque position i de la grille
            currentList = []
            for j in range(36): # pour chaque position j de la grille
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
            self.positions2Points.append(currentList)


    def getPositions2Points(self):
        """ retourne un tableau (i, j) qui est l'ensemble des positions comprises entre j et l.
            Params : None
            Return : un tableau 2D indiquant pour chaque (i, j) l'ensemble des positions entre ces deux points
        """
        return self.positions2Points




#######################################   Définition des contraintes ####################################### 


    def addPositionConstraints(self):
        """ Trois types de contraintes sont ajoutées dans cette méthode : 
                Un seul véhicule dans chaque case a chaque tour. # 2
                Seule vi cases sont occupées par le véhicule i dans sa rangée. #3
                zi,m,k = 1 pour toutes m cases occupées par un véhicule i.
            Params : None
            Return : None

        """
        for k in range(1, self.nbMove+1): # pour chaque étape à partir de la première étape
            for idVehicule in self.idVehiculesList: # pour chaque véhicule

                # pour chaque tour et chaque véhicule, la somme de ces variables z a 1 est égal a la longueur du véhicule.
                self.model.addConstr(quicksum((self.z[idVehicule, j, k] for j in self.possiblesPositions[idVehicule])), GRB.EQUAL, self.longueurs[idVehicule]) #3

                for j in self.possiblesMarqueurs[idVehicule]:
                    # pour vehicule, tour et positions  possibles du vehicule, les z correspondant aux positions du véhicule sont a 1
                    self.model.addConstr(self.longueurs[idVehicule]*self.x[idVehicule, j, k] - quicksum(self.z[idVehicule, l, k] for l in self.positionsVehicules[idVehicule][j]), GRB.LESS_EQUAL, 0)

            for j in self.marqueurs:
                # pour chaque tour et chaque marqueur, il y a au plus un seul véhicule dans la case
                self.model.addConstr(quicksum((self.z[idVehicule, j, k] for idVehicule in self.idVehiculesList if j in self.possiblesPositions[idVehicule])), GRB.LESS_EQUAL, 1)

    def addMovementConstraints(self):
        """ Quatre types de contraintes sont ajoutées dans cette méthode:
                un véhicule ne peut se déplacer que si l'espace entre les deux cases est vide (4)
                au plus un véhicule est déplacé par tour (5)
                le dernier mouvement est celui ou le véhicule "g" est au marqueur 16 (6)
                lors d'un mouvement, le marqueur du véhicule est bien mis à jour (7)
            Params : None
            Return : None
        """

        for k in range(0, self.nbMove+1): # pour chaque étape k
            # le nombre de véhicule déplacé au tour k
            nbVehiculeMoved = LinExpr()

            for idVehicule in self.idVehiculesList:

                # le nombre de position du marqueur du véhicule
                nbVehiculePosition = LinExpr()

                # Le nombre de mouvement du véhicule
                nbVehiculeMovement = LinExpr()
                
                for j in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible
                    nbVehiculePosition.addTerms(1, self.x[idVehicule, j, k])
                    
                    # Ces contraintes ne sont pas valable au tour d'initialisation
                    if k != 0:
                        nbMovementFromJ = LinExpr()
                        nbMovementToJ = LinExpr()
                        for l in self.possiblesMarqueurs[idVehicule]: # pour chaque marqueur possible différent de j
                            if j != l:
                                    nbVehiculeMovement.addTerms(1, self.y[idVehicule, j, l, k])
                                    nbVehiculeMoved.addTerms(1, self.y[idVehicule, j, l, k])
                                    nbMovementFromJ.addTerms(1, self.y[idVehicule, j, l, k])
                                    nbMovementToJ.addTerms(1, self.y[idVehicule, l, j, k])                         

                                    # idVehicule peut se déplacer de j à l uniquement si cet espace est vide au tour précédent
                                    for p in self.positions2Points[j][l]:
                                        nbVehiculeBetween = LinExpr()
                                        for otherVehicule in self.idVehiculesList:
                                            if otherVehicule != idVehicule and p in self.possiblesPositions[otherVehicule]:
                                                nbVehiculeBetween.addTerms(1, self.z[otherVehicule, p, k-1])

                                        self.model.addConstr(self.y[idVehicule, j, l, k], GRB.LESS_EQUAL, (1-nbVehiculeBetween)) # UTILE(4)

                        ## Les mouvements doivent partir d'une position valide
                        self.model.addConstr(nbMovementFromJ - self.x[idVehicule, j, k-1], GRB.LESS_EQUAL, 0) # mouvement doivent partir d'une position valide
                        ## Les marqueurs sont mis à jour lorsqu'un mouvement arrive dans une position
                        self.model.addConstr(nbMovementToJ - self.x[idVehicule, j, k], GRB.LESS_EQUAL, 0) # mouvement arrive et mise à jour, nécessaire
                    
                ## Un véhicule a son marqueur en une position à chaque tour
                self.model.addConstr(nbVehiculePosition, GRB.EQUAL, 1)
                
                if k!=0:
                    for j in self.possiblesMarqueurs[idVehicule]:
                        ## si il n'y a pas de mouvement, pas de changement dans le marqueur d'un véhicule
                        self.model.addConstr(nbVehiculeMovement, GRB.GREATER_EQUAL, self.x[idVehicule, j, k] - self.x[idVehicule, j, k-1]) 
                        #self.model.addConstr(nbVehiculeMovement, GRB.GREATER_EQUAL, self.x[idVehicule, j, k-1] - self.x[idVehicule, j, k]) Inutile dans notre conception

            # si g n'est pas en 16, il y a un mouvement à ce tour
            if k!=0:
                self.model.addConstr(nbVehiculeMoved - (1-self.x["g", 16, k-1]), GRB.EQUAL, 0) #(6)
            else:
                self.model.addConstr(nbVehiculeMoved, GRB.EQUAL, 0)



    def addInitialisationConstraints(self):
        """ Ajoute les contraintes d'initialisation représentant la configuration courante 
            Les marqueurs et positions des véhicules sont mis a 1 en fonction de la configuration courante.
            Params : None
            Return : None
        """
        for vehicule in self.config.getVehicules(): # pour chaque véhicule
            idVehicule = vehicule.getIdVehicule()
            self.model.addConstr(self.x[idVehicule, vehicule.getMarqueur(), 0], GRB.EQUAL, 1)
            for pos in self.positionsVehicules[idVehicule][vehicule.getMarqueur()]: #une contrainte les met à 1 automatiquement, pas nécessaire.
                self.model.addConstr(self.z[idVehicule, pos, 0], GRB.EQUAL, 1)


                            

if __name__ == "__main__":
    conf = Configuration.readFile("../puzzles/avancé/jam26.txt")

    lp = LPSolver(conf, "RHC", 31)
    #print(len(lp.positions2Points[13][16])-1, len(lp.positions2Points[13][14])-1)

    lp.solve()
