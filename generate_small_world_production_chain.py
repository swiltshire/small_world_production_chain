import networkx as nx
from scipy.spatial import Voronoi, voronoi_plot_2d, cKDTree
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

def generate_small_world_production_chain (
		num_agents,
		grid_size,
		proportion_producers,
		proportion_feed_mills,
		proportion_slaughter_plants,
		producer_producer_avg_deg,
		producer_feed_mill_avg_deg,
		producer_slaughter_plant_avg_deg):

	# initialize node positions
	node_positions = {}
	producer_list = []
	feed_mill_list = []
	slaughter_plant_list = []
	for i in range(int(num_agents * proportion_producers)):
		producer_list.append("Producer " + str('%03d' % i))
		node_positions["Producer " + str('%03d' % i)] = (np.random.randint(0,grid_size), np.random.randint(0,grid_size))

	for i in range(int(num_agents * proportion_feed_mills)):
		feed_mill_list.append("Feed Mill " + str('%03d' % i))
		node_positions["Feed Mill " + str('%03d' % i)] = (np.random.randint(0,grid_size), np.random.randint(0,grid_size))

	for i in range(int(num_agents * proportion_slaughter_plants)):
		slaughter_plant_list.append("Slaughter Plant " + str('%03d' % i))
		node_positions["Slaughter Plant " + str('%03d' % i)] = (np.random.randint(0,grid_size), np.random.randint(0,grid_size))

	# copy node labels to graph
	network_graph = nx.DiGraph()
	network_graph.add_nodes_from(sorted(node_positions.keys()))

	# generate voronoi trees for each node type
	producer_voronoi_kdtree = cKDTree([node_positions[key] for key in producer_list])
	feed_mill_voronoi_kdtree = cKDTree([node_positions[key] for key in feed_mill_list])
	slaughter_plant_voronoi_kdtree = cKDTree([node_positions[key] for key in slaughter_plant_list])

	# connect nodes according to probabilities
	for producer in producer_list:
		this_producer_feed_mill_deg = np.random.poisson(lam = producer_feed_mill_avg_deg)
		for i in range(this_producer_feed_mill_deg):
			network_graph.add_edge(feed_mill_list[feed_mill_voronoi_kdtree.query(node_positions[producer], k=i+2)[1][i+1]], producer)

		this_producer_producer_deg = np.random.poisson(lam = producer_producer_avg_deg)
		for i in range(this_producer_producer_deg):
			network_graph.add_edge(producer, producer_list[producer_voronoi_kdtree.query(node_positions[producer], k=i+2)[1][i+1]])

		this_producer_slaughter_plant_deg = np.random.poisson(lam = producer_slaughter_plant_avg_deg)
		for i in range(this_producer_slaughter_plant_deg):
			network_graph.add_edge(slaughter_plant_list[slaughter_plant_voronoi_kdtree.query(node_positions[producer], k=i+2)[1][i+1]], producer)

	return (network_graph, node_positions, producer_list, feed_mill_list, slaughter_plant_list)

