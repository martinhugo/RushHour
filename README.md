# RushHour

## Description 

This project is an universty project developed during the first semester of our Master 1 in Artificial Intelligence at Pierre et Marie Curie University.

Rush Hour is a puzzle game where the player tries to order multiple cars in a garage in order to clear the way for his car. 

The goal of this project is to implement a solver for this game and a graphical interface to visualize the proposed solutions. 

## Chosen Approach

The solver use two approaches:
  * Linear Programming Solver: the solver uses linear programming methods and the gurobi solver to solve the grids.
  * Graph Solver: The solver initializes the current state of the game as a node of a graph. Then, a Dijkstra is launched on the graph until a solution is found.

A complete graphical interface is provided, you can visualize each step of the solution once it is calculated. The solving process is threaded and doesn't block the graphical interface.
