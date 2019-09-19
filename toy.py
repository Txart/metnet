import networkx as nx
import numpy as np



def initialize_node_properties(graph):
    """
    Adds random soil depth
    """
    for node in g_random.nodes():
        depth = np.random.random() * SOIL_DEPTH
        g_random.nodes[node]['depth'] = depth
        g_random.nodes[node]['o2'] = False # Initialization
        
    return 0

def fill_with_air(graph, surface_nodes):
    """
    All nodes connected to a surface node (depth = 0) get o2 = True.
    Modifies graph in place.
    Returns air filled nodes sorted list
    """
    for node in graph.nodes():
        graph.nodes[node]['o2'] = False # Reinitialize
    
    air_filled_nodes = set()
    for i in surface_nodes:
        air_filled_nodes.update(nx.algorithms.descendants(graph, i))
    
    for af_node in air_filled_nodes:
        g_random.nodes[node]['o2'] = True
    
    return list(air_filled_nodes)

def remove_waterlogged(graph, water_table):
    """
    Removes the edges corresponding to the nodes that are deeper than water_table -1.
    Returns removed water nodes.
    """
    water_nodes = [node for node,attr in g_random.nodes(data=True) if attr['depth'] >= water_table]
    for wn in water_nodes:
        edges_to_remove = [edges for edges in g_random.edges(wn)]
        g_random.remove_edges_from(edges_to_remove)
    
    return water_nodes

class PoreNetwork():
    def __init__(self, graph, n_nodes, n_edges):
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.air_filled_nodes = []
        self.waterlogged_nodes = []
        
        surface_nodes = [node for node,attr in g_random.nodes(data=True) if attr['depth']==0]
        self.surface_nodes = tuple(surface_nodes) # surface_nodes don't change
        
# Make other class like so:
# class graph_random(nx.gnm_random_graph, PoreNetwork) This will inherit from the two.
        
        

N_NODES = 1000
N_EDGES = 1000
SOIL_DEPTH = 100

TIMESTEPS = 100
dt = SOIL_DEPTH/TIMESTEPS


# Create graphs
g_complete = nx.complete_graph(N_NODES)
g_random = nx.gnm_random_graph(n=N_NODES, m=N_EDGES)
#g_barabasi_albert = nx.barabasi_albert_graph(n=N_NODES, m=N_EDGES)
graphs = [g_complete, g_random]

# Add properties to nodes: depth, o2.
for graph in graphs:
    initialize_node_properties(graph)

# Copute surface nodes    
surface_nodes = [node for node,attr in g_random.nodes(data=True) if attr['depth']==0]
surface_nodes = tuple(surface_nodes) # surface_nodes don't change

wt = SOIL_DEPTH 

"""
Dynamics
"""
data_over_time = []
wt_values = np.arange(0, SOIL_DEPTH, dt) # Water table, measured positively downward from surface. wt=10 means 10 distance units below surface.
wt_values = wt_values[::-1] # Reverse numpy array: water table increases from above to below.
for wt in wt_values:
    print(wt)
    # If a node is waterlogged, its edges are removed.
    waterlogged_nodes = remove_waterlogged(g_random, wt)
    # Re-compute which nodes are filled by air
    air_filled_nodes = fill_with_air(g_random, surface_nodes)
    
    data_over_time.append([len(air_filled_nodes)/N_NODES, wt, dt])

    
    
"""
Plots
"""
import matplotlib.pyplot as plt

data = np.array(data_over_time)

# 2 y axis, legends
#fig, ax1 = plt.subplots()
#ax1.set_xlabel('time')
#color = 'tab:red'
#ax1.set_ylabel(' ', color=color)
#p1 = ax1.plot(data[:,2], data[:,0], label='air filled pore fraction', color=color)
#
#ax2 = ax1.twinx() # 2nd axes
#color = 'tab:blue'
#ax2.set_ylabel(' ', color=color)
#p2 = ax2.plot(data[:,2], -data[:,1], label='water table depth', color=color)
#
#fig.tight_layout()
#
## All labels in the same legend
#plots = p1 + p2
#labels = [l.get_label() for l in plots]
#ax1.legend(plots, labels, loc=0)

fig, ax = plt.subplots()
ax.set_ylabel('WT depth')
ax.set_xlabel('Fraction of air filled pores')
ax.plot(data[:,0], -data[:,1])

plt.show()






        