# Feb 15: working graph but not meaningful weights and thus occupations shown 
# Committing this version so that I can do the unit test assignments on time, will refine later

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Define a helper function to add_skills for later 
def add_skills(jobs_graph, node_id, row):
    if (row['Element ID'], row['Element Name']) not in jobs_graph.nodes[node_id]['skills']:
        jobs_graph.nodes[node_id]['skills'].append((row['Element ID'], row['Element Name']))

# Define helper function 2 to add neighbors for later 
def add_neighbor(jobs_graph, group, neighbor_idx, current_node, row):
    neighbor_node = group.iloc[neighbor_idx]['O*NET-SOC Code']
    # we dont' want loops to self
    if current_node == neighbor_node:
        return

    if not jobs_graph.has_node(neighbor_node):
        jobs_graph.add_node(neighbor_node, label=group.iloc[neighbor_idx]['Title'], skills=[])
        
    add_skills(jobs_graph, neighbor_node, row)

    if not jobs_graph.has_edge(current_node, neighbor_node):
        jobs_graph.add_edge(current_node, neighbor_node)
        jobs_graph[current_node][neighbor_node]["weight"] = 0

    jobs_graph[current_node][neighbor_node]["weight"] = jobs_graph[current_node][neighbor_node]["weight"] + 1


# Define main function to build the jobs graph
def build_jobs_graph(path_to_jobs):
    df = pd.read_excel(path_to_jobs)

    # only use skills with importance greater than 2.5
    # Original line led to warning: filtered_df = df[df['Scale ID'] == 'IM'][df['Data Value'] > 2.5]
    # Filter in 2 steps, starting with IM rows only
    IM_only_df = df[df['Scale ID'] == 'IM']

    #Filter for Importance > 2.5
    filtered_df = IM_only_df[IM_only_df['Data Value'] > 2.5]
    filtered_df = filtered_df.reset_index()

    # group data by Element ID so we can then iterate over each occupation tied to each skill 
    grouped_df = filtered_df.groupby('Element ID')

    # Initialize graph
    jobs_graph = nx.Graph()

    for code, group in grouped_df:
        # iterate over all groups (one group represents one occupation)
        index = 0
        for row_idx, row in group.iterrows():
            # iterate over all occupations tied to a skill
            # and add an edge between occupation in the same occupation if it doesn't exist
            # increase weight for every additional time two occupations are tied to the same occupation
            current_node = row['O*NET-SOC Code']
            if not jobs_graph.has_node(current_node):
                jobs_graph.add_node(current_node, label=row['Title'], skills=[])
                
            add_skills(jobs_graph, current_node, row)

            for neighbor_idx in range(index+1, group.count()['index']):
                add_neighbor(jobs_graph, group, neighbor_idx, current_node, row)

            index = index+1

    return jobs_graph


jobs_graph = build_jobs_graph("data/Skills.xlsx")  
