# Generated from: Assignment1_Fall2026_SG.ipynb
# Converted at: 2026-10-02T03:03:37.954Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from collections import deque
import heapq


# replicating the map of romania

romania_map = {
    "Arad": {
        "Zerind": 75,
        "Timisoara": 118,
        "Sibiu": 140
    },
    "Zerind": {
        "Arad": 75,
        "Oradea": 71
    },

    "Oradea": {
        "Zerind": 71,
        "Sibiu": 151
    },

    "Timisoara": {
        "Arad": 118,
        "Lugoj": 111
    },

    "Lugoj": {
        "Timisoara": 111,
        "Mehadia": 70
    },

    "Mehadia": {
        "Lugoj": 70,
        "Dobreta": 75
    },

    "Dobreta": {
        "Mehadia": 75,
        "Craiova": 120
    },

    "Craiova": {
        "Dobreta": 120,
        "Rimnicu Vilcea": 146,
        "Pitesti": 138
    },

    "Sibiu": {
        "Arad": 140,
        "Oradea": 151,
        "Fagaras": 99,
        "Rimnicu Vilcea": 80
    },

    "Rimnicu Vilcea": {
        "Sibiu": 80,
        "Craiova": 146,
        "Pitesti": 97
    },

    "Fagaras": {
        "Sibiu": 99,
        "Bucharest": 211
    },

    "Pitesti": {
        "Rimnicu Vilcea": 97,
        "Craiova": 138,
        "Bucharest": 101
    },

    "Bucharest": {
        "Fagaras": 211,
        "Pitesti": 101,
        "Giurgiu": 90,
        "Urziceni": 85
    },

    "Giurgiu": {
        "Bucharest": 90
    },

    "Urziceni": {
        "Bucharest": 85,
        "Hirsova": 98,
        "Vaslui": 142
    },

    "Hirsova": {
        "Urziceni": 98,
        "Eforie": 86
    },

    "Eforie": {
        "Hirsova": 86
    },

    "Vaslui": {
        "Urziceni": 142,
        "Iasi": 92
    },

    "Iasi": {
        "Vaslui": 92,
        "Neamt": 87
    },

    "Neamt": {
        "Iasi": 87
    }
}


# straight-line distances to bucharest
heuristic = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Dobreta": 242,
    "Eforie": 161,
    "Fagaras": 178,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 98,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}


# function to calculate the total distance of each path

def calculate_cost(path):
    cost = 0

    for i in range(len(path) - 1): # loop through each consecutive pair of cities, add distance between the two cities and add it to the total cost so far
        current = path[i]
        next_node = path[i + 1]
        cost += romania_map[current][next_node]

    return cost # return total distance so far

# bfs

def bfs(start, goal): # starting from arad, keep track of the path taken so far to avoid traveling to the same city over and over again
    queue = deque([[start]])
    visited = set([start])
    while queue: # remove first path from the queue; explore paths in the order they were written
        path = queue.popleft()
        current = path[-1]
        if current == goal:
            return path
        for neighbor in romania_map[current]:
            if neighbor not in visited: # if neighboring city hasn't been visited yet, then mark it as visited, and add it to the existing path
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append(new_path)
    return None

# dfs

def dfs(start, goal):
    stack = [[start]] # start stack with Arad, and keep track of the cities we've already been to
    visited = set()
    while stack:
        path = stack.pop() # remove the very last path of the stack, so that dfs operates by traveling all the way down a single path
        current = path[-1]
        if current == goal: # if current city = bucharest, return the path taken to get there
            return path
        if current in visited:# mark cities we haven't visited already as visited
            continue
        visited.add(current) # turn neighboring cities into a list
        neighbors = list(romania_map[current].keys())
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                new_path = path + [neighbor]
                stack.append(new_path)
    return None
    
# a* search

def a_star(start, goal): # a* operates on a formula: f(n) = g(n) + h(n), where g(n) = actual distance from arad to n, and h(n) = estimated distance (heuristic) from n to bucharest

    initial_f = heuristic[start]
    priority_queue = [
        (initial_f, 0, [start])
    ]
    # keep track of the lowest known distance to each city
    best_g = {
        start: 0
    }
    while priority_queue: # if there are cities to explore, continue searching
        f, g, path = heapq.heappop(priority_queue)
        current = path[-1]
        # if goal is reached
        if current == goal:
            return path
        for neighbor, edge_cost in romania_map[current].items():
            new_g = g + edge_cost
            # only consider this route if it is better than the route we've found so far (in terms of f(n))
            if neighbor not in best_g or new_g < best_g[neighbor]:
                best_g[neighbor] = new_g
                h = heuristic[neighbor]
                new_f = new_g + h
                new_path = path + [neighbor]
                heapq.heappush(
                    priority_queue,
                    (new_f, new_g, new_path)
                )
    return None


# run all three algorithms

start = "Arad"
goal = "Bucharest"


# display path when searching with bfs + its total path cost
bfs_path = bfs(start, goal)

print("BFS")
print("Path:", " → ".join(bfs_path))
print("Path cost:", calculate_cost(bfs_path))
print()


# display path when searching with dfs + its total path cost
dfs_path = dfs(start, goal)

print("DFS")
print("Path:", " → ".join(dfs_path))
print("Path cost:", calculate_cost(dfs_path))
print()


# display path when searching with a* search + its total path cost
astar_path = a_star(start, goal)

print("A* Search")
print("Path:", " → ".join(astar_path))
print("Path cost:", calculate_cost(astar_path))