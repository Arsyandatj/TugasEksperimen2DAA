
import argparse
import networkx as nx
import operator
import time
import os
import matplotlib.pyplot as plt


def addEdgeParse(adj, x, y):
    adj[x].append(y)

# FUNCTION FOR PARSING INPUT FILES
def parse(datafile):
    with open(datafile) as f:
        if datafile == "data_kecil.txt":
            num_vertices = 100
        elif datafile == "data_sedang.txt":
            num_vertices = 300
        else:
            num_vertices = 900
        # num_vertices = int(f.readline())
        adj_list = [[] for _ in range(num_vertices + 1)]

        for i in range(1,num_vertices+1):
            line = list(map(int, f.readline().split()))
            size = len(line)
            for j in range(size):
                addEdgeParse(adj_list, i, line[j])

    return adj_list

# USE THE ADJACENCY LIST TO CREATE A GRAPH
def create_graph(adj_list):
	G = nx.Graph()
	for i in range(1,len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i , j)
	return G


def visualize_tree(tree):
    pos = nx.spring_layout(tree)  # Set layout for better visualization (spring layout)
    nx.draw(tree, pos, with_labels=True, font_weight='bold')
    plt.show()

def BnB(G):
	#RECORD START TIME
	start_time=time.time()
	end_time=start_time
	delta_time=end_time-start_time
	times=[]    #list of times when solution is found, tuple=(VC size,delta_time)

	# INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
	OptVC = []
	CurVC = []
	Frontier = []
	neighbor = []

	# ESTABLISH INITIAL UPPER BOUND
	UpperBound = G.number_of_nodes()
	print('Initial UpperBound:', UpperBound)

	CurG = G.copy()  # make a copy of G
	# sort dictionary of degree of nodes to find node with highest degree
	v = find_maxdeg(CurG)
	#v=(1,0)

	# APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
	Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
	Frontier.append((v[0], 1, (-1, -1)))
	# print(Frontier)

	while Frontier!=[]:
		(vi,state,parent)=Frontier.pop() #set current node to last element in Frontier
		
		#print('New Iteration(vi,state,parent):', vi, state, parent)
		backtrack = False

		#print(parent[0])
		# print('Neigh',vi,neighbor)
		# print('Remaining no of edges',CurG.number_of_edges())

		
		if state == 0:  # if vi is not selected, state of all neighbors=1
			neighbor = CurG.neighbors(vi)  # store all neighbors of vi
			for node in list(neighbor):
				CurVC.append((node, 1))
				CurG.remove_node(node)  # node is in VC, remove neighbors from CurG
		elif state == 1:  # if vi is selected, state of all neighbors=0
			# print('curg',CurG.nodes())
			CurG.remove_node(vi)  # vi is in VC,remove node from G
			#print('new curG',CurG.edges())
		else:
			pass

		CurVC.append((vi, state))
		CurVC_size = VC_Size(CurVC)
		#print('CurVC Size', CurVC_size)
		# print(CurG.number_of_edges())
		# print(CurG.edges())

		# print('no of edges',CurG.number_of_edges())
		if CurG.number_of_edges() == 0:  # end of exploring, solution found
			#print('In FIRST IF STATEMENT')
			if CurVC_size < UpperBound:
				OptVC = CurVC.copy()
				#print('OPTIMUM:', OptVC)
				print('Current Opt VC size', CurVC_size)
				UpperBound = CurVC_size
				#print('New VC:',OptVC)
				times.append((CurVC_size,time.time()-start_time))
			backtrack = True
			#print('First backtrack-vertex-',vi)
				
		else:   #partial solution
			#maxnode, maxdegree = find_maxdeg(CurG)
			CurLB = Lowerbound(CurG) + CurVC_size
			#print(CurLB)
			#CurLB=297

			if CurLB < UpperBound:  # worth exploring
				# print('upper',UpperBound)
				vj = find_maxdeg(CurG)
				Frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
				Frontier.append((vj[0], 1, (vi, state)))
				# print('Frontier',Frontier)
			else:
				# end of path, will result in worse solution,backtrack to parent
				backtrack=True
				#print('Second backtrack-vertex-',vi)


		if backtrack==True:
			#print('Hello. CurNode:',vi,state)
			if Frontier != []:	#otherwise no more candidates to process
				nextnode_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))
				#print(nextnode_parent)

				# backtrack to the level of nextnode_parent
				if nextnode_parent in CurVC:
					
					id = CurVC.index(nextnode_parent) + 1
					while id < len(CurVC):	#undo changes from end of CurVC back up to parent node
						mynode, mystate = CurVC.pop()	#undo the addition to CurVC
						CurG.add_node(mynode)	#undo the deletion from CurG
						
						# find all the edges connected to vi in Graph G
						# or the edges that connected to the nodes that not in current VC set.
						
						curVC_nodes = list(map(lambda t:t[0], CurVC))
						for nd in G.neighbors(mynode):
							if (nd in CurG.nodes()) and (nd not in curVC_nodes):
								CurG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

				elif nextnode_parent == (-1, -1):
					# backtrack to the root node
					CurVC.clear()
					CurG = G.copy()
				else:
					print('error in backtracking step')

		end_time=time.time()
		delta_time=end_time-start_time

	return OptVC,times

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
	deglist = g.degree()
	deglist_sorted = sorted(deglist, reverse=True, key=operator.itemgetter(1))  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

#EXTIMATE LOWERBOUND
def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb


def ceil(d):
    """
        return the minimum integer that is bigger than d
    """ 
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    


def VC_Size(VC):
	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size

 
adj_list = parse("data_besar.txt")	
g = create_graph(adj_list)

start_time = time.time()
listVC,times = BnB(g)

for element in listVC:
		if element[1]==0:
			listVC.remove(element)
end_time = time.time()

print(times)
print(listVC)

print(f"Running time : {end_time-start_time}")

# Sumber : https://github.com/sangyh/minimum-vertex-cover/blob/master/BnB_Edited.py


