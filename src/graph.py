__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csv_parse  # CSV parser
from sys import argv as cli_args  # CLI args
from os import path, makedirs, listdir  # Filesystem control
import networkx as nx  # Graph creation and GEXP creation

# Global variables
metadata = []  # CSV metadata
author_csv = []  # Author fields
# Create graph object
graph = nx.DiGraph()

# CLI args
input_dlm = cli_args[1]
input_name = cli_args[2]
output_path = cli_args[3] + input_name + "/"
input_paths = cli_args[4:]
input_files = []

# Get input files and output path
for input_dir in input_paths:

    # Get sorted subdirectories of input directories
    input_subdir = sorted(listdir(input_dir))[1:]

    # Iterate files in subdirectories
    for input_file in input_subdir:

        # Put conference and filename into input file array
        input_files.append([input_dir.split('/')[len(input_dir.split('/'))-2], input_dir + input_file])


# Create output directory if needed
if not path.isdir(output_path):
    makedirs(output_path)

# Get all files in input dir
for filename in input_files:
    # Read each file
    csv_file = open(filename[1], "r")

    with csv_file as current_file:

        # Parse file into records
        records = csv_parse(current_file)

        # Save metadata and create author nodes
        for record in records:

            # Save metadata
            metadata.append(record)

            field = record[1].split(input_dlm)
            # Parse names
            for i in range(len(field)):

                # Strip whitespace
                field[i] = field[i].replace(' ', '')

                # Check for author conflict
                if graph.has_node(field[i]):

                    # Mixed conference field
                    graph.add_node(field[i], conference="Mixed")

                else:

                    # Conference field from parsed conference
                    graph.add_node(field[i], id=graph.number_of_nodes()+1, conference=filename[0])

            # Save field
            author_csv.append(field)

# Remove fluff from fields
author_csv = author_csv[2:]

# Create and count edges between co-authors
for field in author_csv:

    # Check for multi author papers
    if len(field) > 1:
        for edge_start_name in field:

            # Get edge start and possible edge endpoints
            edge_start_name = edge_start_name.replace(' ', '')
            name_index = field.index(edge_start_name)
            other_names = field[:name_index] + field[name_index + 1:]

            # Check all possible endpoints
            for edge_end_name in other_names:
                graph.add_edge(edge_start_name, edge_end_name)

# Write gexf file for graph
edges_gexf_path = output_path + input_name + ".gexf"
nx.write_gexf(graph, edges_gexf_path)

# Write log statements to file
log_path = output_path + input_name + "log.txt"
log_handler = open(log_path, "w+")
log_msg = str(graph.number_of_edges()) + " author edges successfully written to " + edges_gexf_path + " in GEXF format"
log_handler.write(log_msg)
log_handler.close()
