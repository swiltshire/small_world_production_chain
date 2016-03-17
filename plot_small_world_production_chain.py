import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
from scipy.spatial import Voronoi, voronoi_plot_2d, cKDTree
import numpy as np
from pandas import *
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from matplotlib.cm import *
from voronoi_finite_polygons_2d import *

def plot_small_world_production_chain(
		grid_size,
		network_graph,
		node_positions,
		producer_list,
		feed_mill_list,
		slaughter_plant_list,
		plot_network,
		display_feed_mill_voronoi,
		display_slaughter_plant_voronoi):

	plt.figure(figsize=(10,10))
	plt.xlim(0, grid_size)
	plt.ylim(0, grid_size)

	if display_feed_mill_voronoi:
		feed_mill_voronoi = Voronoi([node_positions[key] for key in feed_mill_list])
		regions, vertices = voronoi_finite_polygons_2d(feed_mill_voronoi)
		num_regions = len(regions)
		blue_cmap = LinearSegmentedColormap.from_list(name='blue_cmap', colors =['#E5E5FF', '#0000FF'], N=num_regions)
		for i in range(len(regions)):
			polygon = vertices[regions[i]]
			plt.subplot()
			plt.fill(*zip(*polygon), color = blue_cmap(1.*i/num_regions), alpha=0.3)

	if display_slaughter_plant_voronoi:
		slaughter_plant_voronoi = Voronoi([node_positions[key] for key in slaughter_plant_list])
		regions, vertices = voronoi_finite_polygons_2d(slaughter_plant_voronoi)
		num_regions = len(regions)
		red_cmap = LinearSegmentedColormap.from_list(name='red_cmap', colors =['#FFE5E5', '#FF0000'], N=num_regions)
		for i in range(len(regions)):
			polygon = vertices[regions[i]]
			plt.subplot()
			plt.fill(*zip(*polygon), color = red_cmap(1.*i/num_regions), alpha=0.3)

	if plot_network:
		plt.subplot()
		nx.draw_networkx_nodes(network_graph, node_positions, nodelist = producer_list, node_color='yellow', linewidths=.5, node_size=20)
		nx.draw_networkx_nodes(network_graph, node_positions, nodelist = feed_mill_list, node_color='blue', linewidths=.5, node_size=20)
		nx.draw_networkx_nodes(network_graph, node_positions, nodelist = slaughter_plant_list, node_color='red', linewidths=.5, node_size=20)
		nx.draw_networkx_edges(network_graph, node_positions)
	plt.show()
	# plt.savefig("network_test.png", format="png")

	return