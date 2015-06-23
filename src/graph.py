__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csvreader
from sys import argv as cmd_args
from os import path, makedirs, listdir
import networkx as nx

# Get info from CLI args
input_data_path = cmd_args[1]
input_data_delimiter = cmd_args[3]
input_data_name = input_data_path.split("/")[3]
# Check for name arg
if len(cmd_args) == 5:
    input_data_name = cmd_args[4]
# Generate full I/O paths and create folders if needed
input_data_files = listdir(input_data_path)
output_data_path = cmd_args[2] + input_data_name + "/"
if not path.isdir(output_data_path):
    makedirs(output_data_path)

# Create variables to hold graph information
csv_metadata = []
csv_author_fields = []
csv_author_fields = csv_author_fields[2:]
names_separated = []
graph_edges = {}

# Read CSV file
for filename in input_data_files:
    with open(input_data_path + filename, "r") as citation_data:

        # Get and save metadata
        data_reader = csvreader(citation_data)
        for citation in data_reader:
            csv_author_fields.append(citation[1].strip())
            csv_metadata.append(citation)

# Create nodes for author
for field in csv_author_fields:

    # Get names and strip whitespace
    field_names = field.split(input_data_delimiter)
    for i in range(len(field_names)):
        field_names[i] = field_names[i].replace(' ', '')

    # Add new authors to name array and create ID
    for name in field_names:
        if name not in names_separated:
            names_separated.append(name.replace(' ', ''))

# Count total names
total_names = len(names_separated)

# Create graph object
graph = nx.DiGraph()

# Create edges between co-authors
total_edges = 0
for field in csv_author_fields[2:]:

    # Get names and strip whitespace
    field_names = field.split(input_data_delimiter)
    for i in range(len(field_names)):
        field_names[i] = field_names[i].replace(' ', '')

    # Only multi author papers
    if len(field_names) > 1:
        for edge_start_name in field_names:

            # Get edge start and possible edge endpoints
            edge_start_name = edge_start_name.replace(' ', '')
            name_index = field_names.index(edge_start_name)
            other_names = field_names[:name_index] + field_names[name_index + 1:]

            # Check all possible endpoints
            for edge_end_name in other_names:

                # Strip whitespace
                edge_end_name = edge_end_name.replace(' ', '')

                # Create empty edge array for nodes
                if edge_start_name not in graph_edges.keys():
                    graph_edges[edge_start_name] = []
                if edge_end_name not in graph_edges.keys():
                    graph_edges[edge_end_name] = []

                # Create edges that are nonexistent in both directions
                if edge_end_name not in graph_edges[edge_start_name.strip()]:
                    if edge_start_name not in graph_edges[edge_end_name]:
                        graph.add_edge(edge_start_name, edge_end_name)
                        total_edges += 1


# Write gexf file for graph
edges_gexf_fp = output_data_path + input_data_name + ".gexf"
nx.write_gexf(graph, edges_gexf_fp)

# Write log statements to file
csv_log_fp = output_data_path + input_data_name + "log.txt"
csv_log_fh = open(csv_log_fp, "w+")
csv_log_fh.write(str(total_edges) + " author edges successfully written to " + edges_gexf_fp + " in GEXF format")
csv_log_fh.close()
