import math

class Node:
    def __init__(self,name,location):
        self.name = name #name of node
        self.observation = 'E' #observation at node
        self.location = location #location of node
        self.time = 0
        self.energy = math.inf

    # just for printing nodes
    def __str__(self):
        return self.name

    def set_observation(self,obs):
        self.observation = obs

    def set_energy(self,enr):
        self.energy = enr

    def set_time(self,time):
        self.time = time

