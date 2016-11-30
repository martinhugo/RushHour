# -*- coding: utf-8 -*-

class ListTools:

    @staticmethod
    def union(a, b):
        """ Cette fonction fait l'union de deux tableaux
            Params : a -> tableau
                     b -> tableau
            Return : Union des deux tableaux
        """
        return list(set(a) | set(b))

    @staticmethod
    def intersection(a, b):
        """ Cette fonction réalise l'intersection de deux tableaux
            Params : a -> tableau 
                     b -> tableau
            Return : Intersection des deux tableaux
        """
        return list(set(a) & set(b))

    @staticmethod
    def unique(a):
        """ Cette fonction permet d'obtenir une liste d'éléments sans doublons
            Params : a -> tableau
            Return : Tableau d'éléments uniques
        """
        return list(set(a))

    @staticmethod
    def addToList(a, cte):
        """ Cette fonction permet d'ajouter une constante à un tableau de nombres
            Params : a -> tableau auquel on souhaite ajouter la constante
                     cte -> le nombre que l'on souhaite ajouter au tableau
            Return : Tableau auquel la constante a été ajoutée à chacun de ses éléments
        """
        return [value+cte for value in a]

    @staticmethod
    def difference(a, b):
        """ Cette fonction fait la différence de deux tableaux
            Params : a -> tableau
                     b -> tableau
            Return : La liste des éléments de a n'étant pas dans b
        """
        return list(set(a) - set(b))