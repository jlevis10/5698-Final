import math
from copy import deepcopy


class TS:

    def __init__(self,environment):
        self.env = environment
        self.X = self.env.nodes # all possible states
        self.O = ['o1','o2','o3','o4','E'] # all possible observations (not currently used)
        self.sigma = ['left','right','up','down'] # all possible transitions (not currently used)
        self.currentNode = self.env.currentNode

    # transition function, input a direction and it will move the current node
    # this is here for potential future use; (not currently used)
    def delta(self,sigma):
        self.env.move(sigma)
        self.currentNode = self.env.currentNode

    #get the observation at a given node
    def o(self,node_name):
        return self.env.get_node_obs(node_name)

    # set the observation for a given node name
    def set_observation(self,node,new_output):
        """
        :param node: string name of node to set
        :param new_output: string name of new observation
        :return:
        """
        self.env.set_node_obs(node,new_output)

    def Dijkstra(self,source,destination):
        """
        :param source: string for first node
        :param destination: string for last node
        :return: tuple containing list of nodes travelled and list of output words
        """
        #this code was modified from:
        #https://algodaily.com/lessons/an-illustrated-guide-to-dijkstras-algorithm/python
        unvisited = deepcopy(self.env.graph)
        shortest_distances = {}
        route = []
        observation_route = []
        path_nodes = {}
        for nodes in unvisited:
            shortest_distances[nodes] = math.inf
        shortest_distances[source] = 0
        while unvisited:
            min_node = None
            for current_node in unvisited:
                if min_node is None:
                    min_node = current_node
                elif shortest_distances[min_node] \
                        > shortest_distances[current_node]:
                    min_node = current_node
            for (node, value) in unvisited[min_node].items():
                if value + shortest_distances[min_node] \
                        < shortest_distances[node]:
                    shortest_distances[node] = value \
                                               + shortest_distances[min_node]
                    path_nodes[node] = min_node
            unvisited.pop(min_node)
        node = destination

        while node != source:
            try:
                route.insert(0, node)
                observation_route.insert(0,self.o(node))
                node = path_nodes[node]
            except Exception:
                print('Path not reachable')
                break
        route.insert(0, source)
        observation_route.insert(0, self.o(source))

        if shortest_distances[destination] != math.inf:
            print('Shortest distance is ' + str(shortest_distances[destination]))
            print('Path is ' + str(route))
            print('The output word of this path is: ' + str(observation_route))
            return (str(route), str(observation_route))

        return None
