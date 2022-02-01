import random
import math
from queue import PriorityQueue


def generate_next(state_rep):  # state_rep : string
    children = []
    # search for '0' (empty space)
    index = state_rep.find('0')
    # calculate empty space coordaniates >> r : row , c : column
    (r, c) = (index // 3, index % 3)
    # move empty space up, down, right, or left
    x = [1, -1, 0, 0]
    y = [0, 0, 1, -1]
    for (i, j) in zip(x, y):
        # add possible moves to children list
        if r + i > -1 and r + i < 3 and c + j > -1 and c + j < 3:  # validate next move : check for boundaries
            new_index = 3 * (r + i) + (c + j)
            # swap elements of index and new_index
            new_state = state_rep[:index] + state_rep[new_index] + state_rep[index + 1:]
            new_state = new_state[:new_index] + '0' + new_state[new_index + 1:]

            children.append(new_state)

    # shuffle possible states to change their order
    random.shuffle(children)
    return children


def bfs(state_rep):  # state_rep: string
    goal_state = "012345678"
    frontier = [(state_rep, 1)]  # queue
    frontier_dic = {}
    frontier_dic[state_rep] = True
    path = {}
    path[state_rep] = state_rep
    max_depth = 0;
    while len(frontier):
        state, level = frontier.pop(0)
        max_depth = max(max_depth, level)
        frontier_dic[state] = False

        if state == goal_state:
            print(f'success, {len(path)} states explored. max depth explored : {max_depth}')
            return get_path(path)
        children = generate_next(state)  # get possible next moves/states
        for child in children:
            # add new state to frontier list if it isn't explored or in the frontier list
            if not ((child in frontier_dic) or (child in path)):
                # enqueue child
                frontier.append((child, level + 1))
                frontier_dic[state] = True
                # add parent of the state
                path[child] = state
    # no possible solution
    print(f'failure, {len(path)} states explored. max depth explored : {max_depth}')
    return []


def dfs(state_rep):  # state_rep: string
    goal_state = "012345678"
    frontier = [(state_rep, 1)]  # stack
    frontier_dic = {}
    frontier_dic[state_rep] = True
    path = {}
    path[state_rep] = state_rep
    max_depth = 0
    while len(frontier):
        state, level = frontier.pop()
        max_depth = max(max_depth, level)
        frontier_dic[state] = True
        if state == goal_state:  # check if current state is the goal state
            print(f'success, {len(path)} states explored. max depth explored : {max_depth}')
            return get_path(path)
        children = generate_next(state)  # get possible next moves/states
        for child in children:
            # add new state to frontier list if it isn't explored or in the frontier list
            if not ((child in frontier_dic) or (child in path)):
                frontier.append((child, level + 1))
                frontier_dic[child] = True
                # add parent of the state
                path[child] = state
    # no possible solution
    print(f'failure, {len(path)} states explored. max depth explored : {max_depth}')
    return []


def h1(state):  # sum of manhattan distances
    sum = 0
    for i in range(9):
        x1, y1 = i // 3, i % 3
        x2, y2 = int(state[i]) // 3, int(state[i]) % 3
        sum += abs(x1 - x2) + abs(y1 - y2)
    return sum


def h2(state):  # sum of euclidian distances
    sum = 0
    for i in range(9):
        x1, y1 = i // 3, i % 3
        x2, y2 = int(state[i]) // 3, int(state[i]) % 3
        sum += math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return sum


def a_star(state_rep, heuristic_fn):
    goal_state = "012345678"
    frontier = PriorityQueue()  # priority queue
    # calculate h + g
    h = heuristic_fn(state_rep)  # calculate h
    # enqueue initial state tuple (g(s)+h(s), g ,state)
    frontier.put((h, 0, state_rep, 1))
    path = {}
    path[state_rep] = state_rep
    max_depth = 0

    while not frontier.empty():
        f, gs, state, level = frontier.get()
        max_depth = max(max_depth, level)
        if state == goal_state:
            print(f'success, {len(path)} states explored. max depth explored : {max_depth}')
            return get_path(path)
        children = generate_next(state)  # get possible next moves/states > list of list of states
        for child in children:
            # add new state to frontier list if it isn't explored or in the frontier list
            if not child in path:
                h_child = heuristic_fn(child)  # recalculate any way
                # cost to reach current node
                g_child = 1 + gs
                # enqueue child
                frontier.put((h_child + g_child, g_child, child, level + 1))
                # add parent of the state
                path[child] = state
    # no possible solution
    print(f'failure, {len(path)} states explored. max depth explored : {max_depth}')
    return []


def get_path(parent):
    # start back tracing from goal state
    current = "012345678"
    # list of the steps
    path = []
    # back track until we reach initial state
    while current != parent[current]:
        path.insert(0, current)
        current = parent[current]
    path.insert(0, current)
    print("Path to solution : ", path)
    return path
