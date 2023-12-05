import random
import time


def addEdge(adj, x, y):
    adj[x].append(y)
    adj[y].append(x)
    
def addEdgeParse(adj, x, y):
    adj[x].append(y)
    # adj[y].append(x)
 
 
def dfs(adj, dp, src, par):
    for child in adj[src]:
        if child != par:
            dfs(adj, dp, child, src)
 
    for child in adj[src]:
        if child != par:
            # not including source in the vertex cover
            dp[src][0] = dp[child][1] + dp[src][0]
 
            # including source in the vertex cover
            dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])
 
 
def minSizeVertexCover(adj, N):
    dp = [[0 for j in range(2)] for i in range(N+1)]
    for i in range(1, N+1):
        # 0 denotes not included in vertex cover
        dp[i][0] = 0
 
        # 1 denotes included in vertex cover
        dp[i][1] = 1
 
    dfs(adj, dp, 1, -1)
 
    # printing minimum size vertex cover
    print(min(dp[1][0], dp[1][1]))
    
            
def parse(datafile):
    with open(datafile) as f:
        num_vertices = int(f.readline())
        adj_list = [[] for _ in range(num_vertices + 1)]

        for i in range(1,num_vertices+1):
            line = list(map(int, f.readline().split()))
            size = len(line)
            for j in range(size):
                addEdgeParse(adj_list, i, line[j])

    return adj_list
 
 
adj = parse("data_besar.txt")

N = len(adj) -1

start_time = time.time()
minSizeVertexCover(adj, N)
end_time = time.time()

print(f"Running time : {end_time-start_time}")

# Sumber : https://www.geeksforgeeks.org/vertex-cover-problem-dynamic-programming-solution-for-tree/


