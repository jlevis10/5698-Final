from product_automaton import ProductAutomaton
from buchi_automata import BuchiAutomata
from ts import TS
from environment import Environment

class PathPlanner:
    def __init__(self,env,start_pt = "Node43",spec="spec1.txt"):
        self.start = start_pt + "|T0_init"
        self.BA = BuchiAutomata(spec)
        self.PA = ProductAutomaton(TS(env),self.BA)

    def update(self,env):
        self.env = env

    def generate_path(self):
        path, length, possible = self.PA.Dijkstra(self.start,'Node43|accept_all')
        return path[:-1]

    def generate_path2(self,path1):
        path2 = self.generate_path()
        for i in range(min(len(path1), len(path2)) - 1):
            if path1[i + 1] == path2[i + 1] and path1[i + 1] != "Node42|T1_S2":
                path2.insert(i, path2[i])
        return path2