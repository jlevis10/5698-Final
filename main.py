from environment import Environment
import statistics
from path_planner import PathPlanner
import time
from copy import deepcopy

def visualize(path,path_type='Finite Path',animate=False):
    filename = 'visualization_' + path_type.split()[0] + ".txt"
    if not animate:
        with open(filename,'w') as f:
            f.write(path_type+"\n")
            for node in path:
                print(node)
                f.write(node+"\n")
                location = int(node[4:])
                xx = (location-1)//4
                yy = (location-1) %4
                for i in range(4):
                    for j in range(4):
                        if 3-i == xx and j == yy:
                            print('x  ',end="")
                            f.write('x  ')
                        else:
                            print('.  ',end="")
                            f.write('.  ')
                    print()
                    f.write("\n")
                print()
                f.write("\n")
    else:
        for node in path:
            print("\n\n")
            print(node)
            location = int(node[4:])
            xx = (location - 1) // 4
            yy = (location - 1) % 4
            for i in range(4):
                for j in range(4):
                    if 3 - i == xx and j == yy:
                        print('x  ', end="")
                    else:
                        print('.  ', end="")
                print()
            time.sleep(.5)

def get_next_destinations(ages):
    age_list = [(k, v) for k, v in ages.items()]
    dest1 = age_list[0][0]
    dest2 = age_list[1][0]
    dest1_age = max(age_list[0][1],age_list[1][1])
    dest2_age = min(age_list[0][1], age_list[1][1])
    for pair in age_list:
        if pair[1] > dest1_age:
            dest2 = dest1
            dest2_age = dest1_age
            dest1 = pair[0]
            dest1_age = pair[1]
        elif pair[1] > dest2_age:
            dest2 = pair[0]
            dest2_age = pair[1]

    return dest1, dest2

def reward_found(path1, path2, prize):
    prize_node = "Node" + str(prize[0]) + str(prize[1])
    time = -1
    agent = "agent1"
    for i in range(len(path1)):
        if path1[i] == prize_node:
            time = i

    for i in range(len(path2)):
        if path2[i] == prize_node:
            if time == -1 or i < 1:
                time = i
                agent = "agent2"


    return time>=0 , agent

def update_node_ages(node_ages, path1, path2):
    # first update from path1:
    time_step1 = len(path1)
    time_step2 = len(path2)
    p1r = deepcopy(path1)
    p1r.reverse()
    p2r = deepcopy(path2)
    p2r.reverse()

    for node in node_ages.keys():
        if node in path1:
            node_ages[node] = p1r.index(node)
        elif node in path2:
            node_ages[node] = min(node_ages[node],p2r.index(node))
        else:
            node_ages[node] = node_ages[node] + max(time_step1,time_step2)

    return node_ages

def start_simulation(size=(7,7),battery_life=15):

    rounds_required = 1

    # initialization
    env = Environment(size)
    env.add_desired("Node33","B")
    node_ages = dict()
    dest1 = "Node43"
    dest2 = "Node23"
    start1 = "Node00"
    start2 = "Node66"
    for node in env.nodes:
        node_ages[node.name] = 0

    # loop
    prize = env.generate_random_reward()

    print("Beginning simulation. First reward is at: ",prize)
    print("Agent 1 starting position: ",start1, " Agent 1 target node: ",dest1)
    print("Agent 2 starting position: ", start2, " Agent 2 target node: ", dest2)

    env.remove_desired_nodes()
    env.add_desired(dest1,"T1")
    env.add_desired(dest2,"T2")
    planner1 = PathPlanner(env,start1,'spec1.txt')
    path1 = planner1.generate_path()

    path1, inf1 = env.extract_word(path1)

    for node in set(path1):
        if node != "Node33":
            env.avoid(node)

    planner2 = PathPlanner(env,start2,'spec2.txt')
    path2, inf2 = env.extract_word(planner2.generate_path())

    print(path1)
    print(path2)

    found, agent = reward_found(path1,path2,prize)
    if found:
        print("Reward was discovered by ", agent)

    else:
        print("Reward still not discovered. ")

    times = list()
    while not found:
        time_start = time.time()
        rounds_required += 1
        node_ages = update_node_ages(node_ages,path1,path2)

        destinations = sorted(node_ages.items(), key=lambda x: x[1], reverse=True)
        dest1 = destinations[0][0]
        dest2 = destinations[1][0]

        start1 = "Node32"
        start2 = "Node34"

        print("Agent 1 starting position: ", start1, " Agent 1 target node: ", dest1)
        print("Agent 2 starting position: ", start2, " Agent 2 target node: ", dest2)

        env = Environment(size)
        env.add_desired(dest1, "T1")
        env.add_desired(dest2, "T2")
        env.add_desired("Node33","B")

        planner1 = PathPlanner(env, start1, 'spec1.txt')
        path1 = planner1.generate_path()

        path1, inf1 = env.extract_word(path1)

        for node in set(path1):
            if node != "Node33":
                env.avoid(node)

        planner2 = PathPlanner(env, start2, 'spec2.txt')
        path2, inf2 = env.extract_word(planner2.generate_path())

        time_end = time.time()
        print("Time spend on motion planning: ", time_end - time_start)
        times.append(time_end - time_start)

        print(path1)
        print(path2)

        found, agent = reward_found(path1, path2, prize)
        if found:
            print("Reward was discovered by ", agent)
        else:
            print("Reward still not discovered. ")




    return rounds_required, agent, sum(times)/len(times)


for i in range(20):
    rounds, agent, avg_time = start_simulation((8,8))


"""num_simulations = 1000
round_count = list()
agent_tracker = {"agent1":0,"agent2":0}

for i in range(num_simulations):
    rounds, agent = start_simulation()
    round_count.append(rounds)
    agent_tracker[agent] += 1

print("Agent 1 found the reward",agent_tracker["agent1"],"times.")
print("Agent 2 found the reward",agent_tracker["agent2"],"times.")
print("The mean amount of rounds needed was: ",sum(round_count)/len(round_count))
print("The standard deviation of rounds needed was: ",statistics.pstdev(round_count))
"""







