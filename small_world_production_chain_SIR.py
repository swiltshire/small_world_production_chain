import networkx as nx
from scipy.spatial import Voronoi, voronoi_plot_2d, cKDTree
import numpy as np
from pandas import *
import matplotlib.pyplot as plt

def small_world_production_chain_SIR(
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
		slaughter_plant_avg_duration):

	#dictionary encodes the infected agent and the time step the infection will end
	infected_agents = {producer_list[0]: np.random.poisson(producer_avg_duration)}
	cumulative_infected_agents = [producer_list[0]]

	#SIR code
	infection_duration = 0
	infections_over_time = []
	for time_step in range(max_time_steps):
		for producer in producer_list:

			#evaluate each sucessor for potential contact
			for potential_contact in network_graph.successors(producer):

				#potential contact is a producer
				if (potential_contact in producer_list) and (np.random.random() < producer_producer_contact_rate):
					#producer -> producer contact has occurred
					if (np.random.random() < prob_source_producer_to_dest_producer_spread) and (producer in infected_agents.keys()):
						#infection spread from source producer to dest producer
						infected_agents[potential_contact] = time_step + np.random.poisson(producer_avg_duration)
						if not (potential_contact in cumulative_infected_agents):
							cumulative_infected_agents.append(potential_contact)
					if (np.random.random() < prob_dest_producer_to_source_producer_spread) and (potential_contact in infected_agents.keys()):
						#infection spread from dest producer to source producer
						infected_agents[producer] = time_step + np.random.poisson(producer_avg_duration)
						if not (producer in cumulative_infected_agents):
							cumulative_infected_agents.append(producer)

				#potential contact is a slaughter plant
				elif (potential_contact in slaughter_plant_list) and (np.random.random() < producer_slaughter_plant_contact_rate):
					#producer -> slaughter plant contact has occurred
					if (np.random.random() < prob_producer_to_slaughter_plant_spread) and (producer in infected_agents.keys()):
						#infection spread from producer to slaughter plant
						infected_agents[potential_contact] = time_step + np.random.poisson(slaughter_plant_avg_duration)
						if not (potential_contact in cumulative_infected_agents):
							cumulative_infected_agents.append(potential_contact)
					if (np.random.random() < prob_slaughter_plant_to_producer_spread) and (potential_contact in infected_agents.keys()):
						#infection spread from slaughter plant to producer
						infected_agents[producer] = time_step + np.random.poisson(producer_avg_duration)
						if not (producer in cumulative_infected_agents):
							cumulative_infected_agents.append(producer)

			#evaluate each predecessor for potential contact
			for potential_contact in network_graph.predecessors(producer):

				#potential contact is a feed mill
				if (potential_contact in feed_mill_list) and (np.random.random() < producer_feed_mill_contact_rate):
					#producer -> feed mill contact has occurred
					if (np.random.random() < prob_producer_to_feed_mill_spread) and (producer in infected_agents.keys()):
						#infection spread from producer to feed mill
						infected_agents[potential_contact] = time_step + np.random.poisson(feed_mill_avg_duration)
						if not (potential_contact in cumulative_infected_agents):
							cumulative_infected_agents.append(potential_contact)
					if (np.random.random() < prob_feed_mill_to_producer_spread) and (potential_contact in infected_agents.keys()):
						#infection spread from feed mill to producer
						infected_agents[producer] = time_step + np.random.poisson(producer_avg_duration)
						if not (producer in cumulative_infected_agents):
							cumulative_infected_agents.append(producer)

		for infected_agent in infected_agents.keys():
			if infected_agents[infected_agent] <= time_step:
				del infected_agents[infected_agent]

		infections_over_time.append(len(infected_agents))
		infection_duration += 1
		if len(infected_agents) == 0:
			break

	print infections_over_time
	print "Infection Duration = " + str(infection_duration)
	print "Cumulative Infections = " + str(len(cumulative_infected_agents))
	return