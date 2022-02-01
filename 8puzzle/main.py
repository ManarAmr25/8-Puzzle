import time

import solver

# main
state = "432650781"
print("bfs : ")
start_time = time.time()
p1 = solver.bfs(state)
print("Time in millisecods : ",(time.time()-start_time) *1000)

print("dfs : ")
start_time = time.time()
p2 = solver.dfs(state)
print("Time in millisecods : ",(time.time()-start_time) *1000)

print("A* (heuristic : Manhattan) : ")
start_time = time.time()
p3 = solver.a_star(state,solver.h1)
print("Time in millisecods : ",(time.time()-start_time) *1000)

print("A* (heuristic : Euclidian) : ")
start_time = time.time()
p4 = solver.a_star(state,solver.h2)
print("Time in millisecods : ",(time.time()-start_time) *1000)