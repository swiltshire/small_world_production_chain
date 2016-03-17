from generate_small_world_production_chain import *
from plot_small_world_production_chain import *
from small_world_production_chain_SIR import *


# -- DEFINE EXPERIMENT VARIABLES BELOW -- #

# Network Initialization:
num_agents = 500
grid_size = 1000
max_time_steps = 1000

proportion_producers = .98
proportion_feed_mills = .01
proportion_slaughter_plants = .01

producer_producer_avg_deg = 1
producer_feed_mill_avg_deg = .75
producer_slaughter_plant_avg_deg = 1

# SIR model
producer_feed_mill_contact_rate = .15
producer_slaughter_plant_contact_rate = .15
producer_producer_contact_rate = .05

prob_source_producer_to_dest_producer_spread = .95
prob_dest_producer_to_source_producer_spread = .05
prob_producer_to_feed_mill_spread = .05
prob_feed_mill_to_producer_spread = .05
prob_producer_to_slaughter_plant_spread = .05
prob_slaughter_plant_to_producer_spread = .05

producer_avg_duration = 30
feed_mill_avg_duration = 7
slaughter_plant_avg_duration = 7

# Network Plot
draw_plot = True
plot_network = True
display_feed_mill_voronoi = False
display_slaughter_plant_voronoi = True

# -- END VARIABLE DEFINITIONS -- #


(network_graph,
	node_positions,
	producer_list,
	feed_mill_list,
	slaughter_plant_list) = \
	generate_small_world_production_chain(
			num_agents,
			grid_size,
			proportion_producers,
			proportion_feed_mills,
			proportion_slaughter_plants,
			producer_producer_avg_deg,
			producer_feed_mill_avg_deg,
			producer_slaughter_plant_avg_deg)

# print DataFrame(sorted(nx.to_pandas_dataframe(network_graph)))

small_world_production_chain_SIR(
		network_graph,
		producer_list,
		feed_mill_list,
		slaughter_plant_list,
		max_time_steps,
		producer_feed_mill_contact_rate,
		producer_slaughter_plant_contact_rate,
		producer_producer_contact_rate,
		prob_source_producer_to_dest_producer_spread,
		prob_dest_producer_to_source_producer_spread,
		prob_producer_to_feed_mill_spread,
		prob_feed_mill_to_producer_spread,
		prob_producer_to_slaughter_plant_spread,
		prob_slaughter_plant_to_producer_spread,
		producer_avg_duration,
		feed_mill_avg_duration,
		slaughter_plant_avg_duration)

if draw_plot:
	plot_small_world_production_chain(
			grid_size,
			network_graph,
			node_positions,
			producer_list,
			feed_mill_list,
			slaughter_plant_list,
			plot_network,
			display_feed_mill_voronoi,
			display_slaughter_plant_voronoi)