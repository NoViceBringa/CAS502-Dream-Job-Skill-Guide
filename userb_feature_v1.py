# import relevant libraries
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Define a helper function that add skills to each node. This will be called upon later
def add_skills(jobs_graph, node_id, row):

    #Create a skill_id variable for easier reference 
    skill_id = row['Element ID']
    
    #If the specific skill don't already exist, pull in the skill ID, skill name, importance, level data 
    if skill_id not in jobs_graph.nodes[node_id]['skills']:
        jobs_graph.nodes[node_id]['skills'][skill_id] = {
            'name': row['Element Name'],
            'importance': float(row['Importance']),
            'level': float(row['Level']),
        }

# Define helper function 2 to add neighbors to each node. This will be called upon later 
def add_neighbor(jobs_graph, group, neighbor_idx, current_node, row, skill_id):

    # Define neighbor row as the row at neighbor_idx position 
    neighbor_row = group.iloc[neighbor_idx]

    # Use ONET SOC code as the node ID for neighbor_node 
    neighbor_node = neighbor_row['O*NET-SOC Code']
    
    # we don't want loops to self
    if current_node == neighbor_node:
        return
        
    # Add node to the graph if it doesn't already exist. 
    # Use the 'Title' field as the label of the node. 
    # Create an empty skills dictionary for later use
    if not jobs_graph.has_node(neighbor_node):
        jobs_graph.add_node(neighbor_node, label=group.iloc[neighbor_idx]['Title'], skills={})

    # Call upon the add_skills function defined above
    add_skills(jobs_graph, neighbor_node, neighbor_row)

    # We want to add edges between two occupations only when the skills match on both Importance and Level 
    # Pull the skills dictionaries from both curent and neighbor notes for comparison 
    skills_a = jobs_graph.nodes[current_node]['skills']
    skills_b = jobs_graph.nodes[neighbor_node]['skills']

    # Look up this specific skill_id in each occupation's skills dictionary 
    # This compares one skill at a time (not the entire skills dictionary).
    a = skills_a.get(skill_id)
    b = skills_b.get(skill_id)

    # Add edge between 2 occupations only if the skill Importance and Level data match on the same skill_id 
    if a['importance'] == b['importance'] and a['level'] == b['level']:
        if not jobs_graph.has_edge(current_node, neighbor_node):
            jobs_graph.add_edge(current_node, neighbor_node, weight=0)

            # Every time an skill overlaps in Importance and Skill, add 1 to the weight 
            jobs_graph[current_node][neighbor_node]['weight'] = jobs_graph[current_node][neighbor_node]['weight'] + 1

# Define main function to build the jobs graph
def build_jobs_graph(path_to_jobs):
    df = pd.read_excel(path_to_jobs)

    # Add a column to round up Importance and Level data 
    df['Rounded data']=df['Data Value'].round()

    # Flatten the data to make Importance and Level data their own columns for easier manipulation later
    # Use Rounded data for both columns 
    flat_df = (
        df.pivot_table(
            index=["O*NET-SOC Code", "Title", "Element ID", "Element Name"],
            columns="Scale Name",          # "Importance" vs "Level"
            values="Rounded data",           # or use "Rounded data" if you prefer
            aggfunc="first"
        )
        .reset_index()
    )

    # Filter out data by:
    # Importance must be > 2.5 (mid point of data range)
    # Level must be > 3 (mid point of data range) 
    filtered_flat_df = flat_df[(flat_df['Importance'] > 2.5) & (flat_df['Level'] > 3)]
    filtered_flat_df.reset_index()

    # group data by Element ID so we can then iterate over each occupation tied to each skill 
    grouped_df = filtered_flat_df.groupby('Element ID')

    # Initialize graph
    jobs_graph = nx.Graph()

    # Build the graph 
    for skill_id, group in grouped_df:
        # iterate over all groups (one group represents one skill)
        # create an index so it the loop can compare to subsequent rows instead of to the same one later 
        index = 0
        for row_idx, row in group.iterrows():
            # iterate over all occupations tied to a skill
            current_node = row['O*NET-SOC Code']

            # Add node if it doesn't already exist
            # Use 'Title' as node label
            # Add an empty skills dictionary for later 
            if not jobs_graph.has_node(current_node):
                jobs_graph.add_node(current_node, label=row['Title'], skills={})

            # Call upon the add_skills function defined above
            add_skills(jobs_graph, current_node, row)

            # Call the add_neighbor function defined earlier for all the other occupations in this group
            for neighbor_idx in range(index + 1, len(group)):
                add_neighbor(jobs_graph, group, neighbor_idx, current_node, row, skill_id)
    
            index = index+1

    return jobs_graph


# Build the graph with real data
jobs_graph = build_jobs_graph("data/Skills.xlsx") 

# Ask user for input 
selected_title = input("Enter your current title (e.g. Physicists: ")

# Define and occupation cc variable so that we can search for the matching label to the user input title in the dataset 
occ = None
for node, data in jobs_graph.nodes(data=True):
    if data.get("label") == selected_title:
        occ = node
        # Stop the loop when the matching title is found 
        break 

# Print error if selected_title cannot be matched to data in dataset
if occ is None:
    print("Title not found!")

# Find the top neighbors to the selected_title, sort them by weight of edges in descending orders so it's highest weight first  
else:
    neighbors = sorted(
        jobs_graph[occ].items(),
        key=lambda kv: kv[1].get("weight", 1),
        reverse=True
    )

    print("\nTop 5 related occupations and number of shared skills with same importance and level:")

    # Print the top 5 closest occupations to the selected_title based on weight 
    for n, attr in neighbors[:5]:
        print(
           jobs_graph.nodes[n]["label"],
            "|", attr["weight"]
        )
