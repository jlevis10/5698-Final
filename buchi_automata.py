from PySimpleAutomata import DFA, automata_IO
import json
import random

class BuchiAutomata :
    def __init__(self,filename):
        self.name = filename[:filename.index(".")]
        self.graph = self.generate(filename)
        self.nodes = list(self.graph.keys())
        self.initial = self.nodes[0]
        self.final = self.nodes[-1]
        self.transitions = self.graph.values()
        self.alphabet = self.nodes[-1]
        self.obs = ['r1','r2','r3','o1','o2']

    def get_accepting_word(self):
        current_state = self.initial
        word = []
        while current_state[:6] != "accept":
            options = self.graph[current_state]
            nodes = list(options.keys())
            node = nodes[random.randint(0, len(nodes)-1)]
            word.append(options[node])
            current_state = node
        word.append("(" + current_state + ")^w")
        return "".join(word)


    def get_path(self):
        current = self.initial
        path = str(current)
        while (current != self.final):
            operations = self.graph[current]
            move = self.obs[random.randint(0,4)]
            for key in operations:
                while ("!" + move in operations[key].split()):
                    move = self.obs[random.randint(0, 4)]
                if move in operations[key].split():
                    current = key
            path += ", " + str(move)
            path += " -> " + (current)
        return path

    def get_alphabet(self):
        alpha = set()
        for item in self.transitions:
            alpha.add(self.transitions[item])
        return list(alpha)

    def get_final(self):
        accepting = []
        for node in self.nodes:
            if "accept" in str(node):
                accepting.append(node)

    def generate(self,filename):
        graph = dict()
        with open (filename,'r') as f:
            lines = f.readlines()
        eqn = lines[0].split()
        self.formula = " ".join(eqn[eqn.index("/*")+1:eqn.index("*/")])
        i = 1
        while i < len(lines)-1:
            key = lines[i].split()[0]
            value = dict()
            i += 2
            while ("fi;" not in lines[i]):
                val = lines[i][lines[i].index("(")+1:lines[i].index(")")]
                temp = lines[i].split()
                value[temp[-1]] = val
                i += 1
            i+=1
            graph[key] = value

        return graph

    def visualize(self):
        dfa = dict()
        transitions = []
        print (self.graph)
        for s1 in self.graph:
            for s2 in self.graph[s1]:
                transitions.append([s1,self.graph[s1][s2],s2])
        dfa["states"] = self.nodes
        dfa["initial_state"] = self.initial
        dfa["accepting_states"] = self.nodes[-1]
        dfa["transitions"] = transitions
        dfa["alphabet"]= self.alphabet
        dfa_dump = json.dumps(dfa, indent=4)
        with open (self.name+'.json','w' ) as f:
            f.write(dfa_dump)

        new_dfa = automata_IO.dfa_json_importer(self.name+'.json')
        automata_IO.dfa_to_dot(new_dfa, self.name, 'outputs/')

    def extract_path(self,finite,inf=False):
        path = [node[node.index("|")+1:] for node in finite]
        fin_path=[]
        for i in range (len(finite)-1):
            options = self.graph[path[i]]
            fin_path.append(options[path[i+1]])
        if inf:
            return "("+ "  ".join(fin_path) + ")^w"
        return "  ".join(fin_path)
