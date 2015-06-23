__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csvreader
from sys import argv as cmd_args
from os import path, makedirs, listdir

# Get info from CLI args
input_data_path = cmd_args[1]
input_data_delimiter = cmd_args[2]
# Generate full I/O paths
input_data_files = listdir(input_data_path)
input_data_name = input_data_path.split("/")[3]
output_data_path = "output/" + input_data_name + "/"
# Make output directory if nonexistent
if not path.isdir(output_data_path):
    makedirs(output_data_path)

# Create variables to hold graph information
csv_metadata = []
csv_author_fields = []
csv_author_fields = csv_author_fields[2:]
names_separated = []
graph_node_ids = {}
graph_edges = {}

# Read CSV file and save metadata
for filename in input_data_files:
    with open(input_data_path + filename, "r") as citation_data:
        data_reader = csvreader(citation_data)
        for citation in data_reader:
            csv_author_fields.append(citation[1])
            csv_metadata.append(citation)

# Create nodes for author
for field in csv_author_fields:
    field_names = field.split(input_data_delimiter)
    for name in field_names:
        name = name.strip()
        # Add new authors to name array and create ID
        if name not in names_separated:
            names_separated.append(name)
            graph_node_ids[name] = len(names_separated)
total_names = len(names_separated)

# Open edge file handler and related vars
csv_nodes_fp = output_data_path + input_data_name + "nodes.csv"
csv_nodes_fh = open(csv_nodes_fp, "w+")
csv_nodes_delimiter = ";"
# Write nodes to file in CSV format
csv_nodes_fh.write("Label" + csv_nodes_delimiter + "Id\n")
for name in names_separated:
    csv_nodes_fh.write(name + csv_nodes_delimiter + str(graph_node_ids[name]) + "\n")
csv_nodes_fh.close()

# Create empty edge array for each author
for name in names_separated:
    graph_edges[graph_node_ids[name]] = []

# Create edges between co-authors
total_edges = 0
for field in csv_author_fields:
    field_names = field.split(';')
    for edge_start_name in field_names:
        name_index = field_names.index(edge_start_name)
        other_names = field_names[:name_index] + field_names[name_index + 1:]
        for edge_end_name in other_names:
            # Create ids for start and end of edge
            edge_start_id = graph_node_ids[edge_start_name.strip()]
            edge_end_id = graph_node_ids[edge_end_name.strip()]
            # Check if edge exists currently and if not create it
            if edge_end_id not in graph_edges[edge_start_id]:
                if edge_start_id not in graph_edges[edge_end_id]:
                    graph_edges[edge_start_id].append(edge_end_id)
                    total_edges += 1

# Open edge file handler and related vars
csv_edges_fp = output_data_path + input_data_name + "edges.csv"
csv_edges_fh = open(csv_edges_fp, "w+")
csv_edges_delimiter = ","
# Write edges to file in CSV format
csv_edges_fh.write("Source" + csv_edges_delimiter + "Target\n")
for edge_start_id in graph_edges.keys():
    for edge_end_id in graph_edges[edge_start_id]:
        csv_edges_fh.write(str(edge_start_id) + csv_edges_delimiter + str(edge_end_id) + "\n")
csv_edges_fh.close()

# Write log statements to file
csv_log_fp = output_data_path + input_data_name + "log.txt"
csv_log_fh = open(csv_log_fp, "w+")
csv_log_fh.write(str(total_names) + " author names successfully written to " + csv_nodes_fp + " in CSV format.\n")
csv_log_fh.write(str(total_edges) + " author edges successfully written to " + csv_edges_fp + " in CSV format.")
csv_log_fh.close()
