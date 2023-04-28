from node import Node
import random
class Environment:
    def __init__(self,size=(7,7)): #default size is 8x10, user will specify sub region in constructor
        self.size = size
        self.nodes = self.create_nodes(size) #create a list of nodes as large as size of grid
        self.graph = self.create_graph() #graph with edge costs and string nodes (used for dijkstra and move)
        self.currentNode = self.nodes[0] #current node which will be an iterator
        self.desired_list = list()

    # creates labelled nodes based on size of the grid
    def create_nodes(self,size):
        self.obstacle_list = []
        self.avoid_list = []
        nodes = []
        for i in range(size[0]):
            for j in range(size[1]):
                nodes.append(Node(("Node"+str(i)+str(j)),(i,j)))
        return nodes

    def print_nodes(self):
        for node in self.nodes:
            print(node.name, node.location, node.observation)

    # creates edges between nodes and assigns default weight to 1.
    # corresponds to the creat_graph method
    def assign_default_edges(self,node):
        assignment = 1
        if node.name in self.avoid_list:
            assignment = 5

        edges = dict()
        x = node.location[0]
        y = node.location[1]
        for n in self.nodes:
            if n.observation != 'o1': # make sure that the node is not blocked by object
                if n.name == ("Node" + str(x+1) + str(y)):
                    edges[str(n)] = assignment
                if n.name == (("Node" + str(x-1) + str(y))):
                    edges[str(n)] = assignment
                if n.name == (("Node" + str(x) + str(y+1))) and y != self.size[0]-1:
                    edges[str(n)] = assignment
                if n.name == (("Node" + str(x) + str(y-1))) and y != 0:
                    edges[str(n)] = assignment
                if n.name == (("Node" + str(x) + str(y))):
                    edges[str(n)] = assignment
        return edges


    # creates graph with key = string node name, value = weight of edge.
    def create_graph(self):
        graph = dict()
        for n in self.nodes:
            graph[n.name] = self.assign_default_edges(n)
        return graph

    def add_obstacle(self,node_name):
        self.obstacle_list.append(node_name)
        self.set_node_obs(node_name,"o1")
        # now update all information
        self.graph = self.create_graph()

    def avoid(self,node_name):
        self.avoid_list.append(node_name)
        self.set_node_obs(node_name,"a")
        self.graph = self.create_graph()

    def add_desired(self,node_name,name='T1'):
        self.set_node_obs(node_name,name)
        if name != "B":
            self.desired_list.append(node_name)

    def remove_desired_nodes(self):
        for node in self.desired_list:
            self.set_node_obs(node,"E")

    # input string of node name, output node's obs
    def get_node_obs(self,node_name):
        for node in self.nodes:
            if node.name == node_name:
                return node.observation

    # input string of node name, set the obs
    def set_node_obs(self,node_name,new_output):
        for node in self.nodes:
            if node.name == node_name:
                node.set_observation(new_output)

    def extract_word(self,pa_path): # get only first part of nodes in PA
        path = [node[:node.index("|")] for node in pa_path]
        return path , [self.get_node_obs(node) for node in path]


    def near_obstacle(self,node):
        # checks if node is next to obstacle, if so, all edges to that node will have added weight
        index = int(node[4:])
        for obs in self.obstacle_list:
            location = int(obs[4:])
            if index-4 == location or index + 4 == location or index -1 == location or index + 1 == location\
                    or index + 5 == location or index - 5 == location or index + 3 == location or index-3==location:
                return True
        return False


    def generate_random_reward(self):
        x_coord = random.randint(0,self.size[0]-1)
        y_coord = random.randint(0,self.size[1]-1)
        if (x_coord == 3 and y_coord == 3):
            x_coord = 4
            y_coord = random.randint(0,6)
        return (x_coord,y_coord)

    def remove_avoidances(self):
        for node_name in self.avoid_list:
            self.set_node_obs(node_name, "a")
        self.graph = self.create_graph()