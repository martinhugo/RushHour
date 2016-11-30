# -*- coding: utf-8 -*-

class ListTools:

    @staticmethod
    def union(a, b):
        return list(set(a) | set(b))

    @staticmethod
    def intersection(a, b):
        return list(set(a) & set(b))

    @staticmethod
    def unique(a):
        return list(set(a))

    @staticmethod
    def addToList(a, cte):
        return [value+cte for value in a]

    @staticmethod
    def difference(a, b):
        return list(set(a) - set(b))