import csv
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Dijkstra:
    def __init__(self, filename):
        self.connections = {}
        self.load_data(filename)

    def load_data(self, filename):
        trip_ids = []
        trajets = []
        durees = []

        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter='\t')
            next(csv_reader)

            for row in csv_reader:
                trip_id, trajet, duree = row
                trip_ids.append(trip_id)
                trajets.append(trajet)
                durees.append(int(duree))

        for i in range(len(trip_ids)):
            parts = trajets[i].split(" - ")
            departure, destination = parts[0], parts[1]
            duree = durees[i]
            if departure not in self.connections:
                self.connections[departure] = []
            self.connections[departure].append((destination, duree))
            if destination not in self.connections:
                self.connections[destination] = []
            self.connections[destination].append((departure, duree))

    def find_shortest_path(self, departure, destination):
        visited = set()
        distances = {city: float('inf') for city in self.connections}
        previous_city = {city: None for city in self.connections}
        distances[departure] = 0
        queue = [(0, departure)]

        while queue:
            current_distance, current_city = heapq.heappop(queue)
            if current_city in visited:
                continue
            visited.add(current_city)
            for neighbor, weight in self.connections[current_city]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_city[neighbor] = current_city
                    heapq.heappush(queue, (distance, neighbor))

        route = []
        current = destination
        while current:
            route.insert(0, current)
            current = previous_city[current]

        cumulative_distance = distances[destination]

        formatted_string = f'Departure {route[0]}'
        for i in range(1, len(route)-1):
            formatted_string += f' -> Step_{i} {route[i]}'
        formatted_string += f' -> Destination {route[-1]}\nTemps passé: {cumulative_distance/60} h'
        
        with open("chemin_djikstra.txt", "w") as trajet:
            trajet.write(formatted_string)

        return route, cumulative_distance, formatted_string

    def draw_graph(self):
        G = nx.Graph()
        
        for city, connections in self.connections.items():
            for neighbor, weight in connections:
                G.add_edge(city, neighbor, weight=weight)
        
        pos = nx.spring_layout(G)  # Layout du graphique
        
        edge_labels = {(city, neighbor): f"{data['weight']} km" for city, neighbor, data in G.edges(data=True)}
        
        nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        
        plt.title("Graphique des connexions entre les villes")
        plt.savefig("./djikstra_graph.png")


if __name__ == "__main__":
    dijkstra = Dijkstra('../datas/timetables.csv')
    dijkstra.draw_graph()
    departure ="Gare de Caen"
    destination = "Gare de Marseille-St-Charles"
    route, cumulative_distance, formatted_string = dijkstra.find_shortest_path(departure, destination)