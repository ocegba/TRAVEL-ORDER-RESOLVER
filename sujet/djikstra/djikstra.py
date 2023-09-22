import pandas as pd
import matplotlib.pyplot as plt
import csv

from string import ascii_uppercase

import itertools
from itertools import combinations

import networkx as nx
from collections import deque

class Djikstra:
    def __init__(self, trajets_file, view_graph):
        self.trajets_file = trajets_file
        self.view_graph = ""

    def graphe_trajets(self):
        graphe = {}
        
        with open(self.trajets_file, encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            next(reader)  # Sauter la première ligne
            
            for row in reader:
                trip_id, trajet, duree = row
                gares_split = trajet.split(' - ')
                
                if len(gares_split) == 2:
                    gare_origine, gare_destination = gares_split
                
                if gare_origine not in graphe:
                    graphe[gare_origine] = [] # créer la premiere valeur 
                    
                if gare_destination not in graphe:
                    graphe[gare_destination] = [] # ceux qui ne sont jamais pris en tant que départ

                graphe[gare_origine].append((trip_id, gare_destination, duree)) 
                graphe[gare_destination].append((trip_id, gare_origine, duree))
        
        return graphe
    
    def graphe_dirige_trajets(self):
        # Créez un nouveau graphe dirigé
        G = nx.DiGraph()

        graphe_gares = self.graphe_trajets()

        # Ajoutez les nœuds et les arêtes à partir de votre dictionnaire
        for node, edges in graphe_gares.items():
            for tripId, edge, weight in edges:
                G.add_edge(node, edge, weight=float(weight))

        if self.view_graph:
            print("\nPour vérification: Forme du graphe")
            print("------------------------------------")

            pos = nx.spring_layout(G)
            
            # Crée une nouvelle figure avec une taille personnalisée (largeur, hauteur) en pouces
            fig, ax = plt.subplots(figsize=(20, 6))

            nx.draw(G, with_labels=True, pos=pos, node_size=800, node_color='lightblue', \
                    font_size=10, font_color='black', font_weight='bold', \
                    font_family='sans-serif', style='dashed', linewidths=2 )

            plt.savefig("./djikstra_graph.png")


        return nx.to_dict_of_lists(G)

    def plus_court_chemin(self, source, destination):
        G = self.graphe_dirige_trajets()

        # dictionnaire des prédecesseurs
        predecesseurs = {source: None}
        # Créer une file
        f = deque()
        # Enfiler le sommet de départ
        f.appendleft(source)
        # Liste des sommets visités
        visites = [source]
        
        # TANT QUE la file est non vide
        while f:
            # On récupère le noeud
            s = f.pop()
            # POUR TOUT voisin t de s dans G
            for t in G[s]:
                if t == destination:
                    # Destination trouvée, on remonte le chemin
                    ville = s
                    chemin = [destination]
                    while ville:
                        chemin.append(ville)
                        ville = predecesseurs[ville]
                    # On remet dans l'ordre
                    chemin.reverse()
                    return chemin
                # SI t non marqué
                elif t not in visites:
                    # Enfiler t
                    f.appendleft(t)
                    # Marquer t
                    visites.append(t)
                    # Mise à jour du dictionnaire des prédecesseurs
                    predecesseurs[t] = s
        # Destination non trouvée
        return []
    
    def format_plus_court_chemin(self, source, destination):
        chemin = self.plus_court_chemin( source, destination)

        if len(chemin) > 0 :
            formatted_string = f'Departure {chemin[0]}'

            for i in range(1, len(chemin)-1):
                formatted_string += f' -> Step_{i} {chemin[i]}'

            formatted_string += f' -> Destination {chemin[-1]}'
        else :
            formatted_string = f"Pas de chemin trouvé entre {source} et {destination}"

        return formatted_string

if __name__ == "__main__":
    csv_trajet = "../datas/timetables.csv"

    graphe = Djikstra(csv_trajet, False)
    chemin = graphe.format_plus_court_chemin("Gare de Caen", "Gare de Marseille-St-Charles")
    with open("chemin_djikstra.txt", "w") as trajet:
        trajet.write(chemin)