__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csv_parse  # CSV parser
from sys import argv as cli_args  # CLI args
from os import path, makedirs, listdir  # Filesystem control
import networkx as nx  # Graph creation and GEXP creation

# Global variables
metadata = []  # CSV metadata
author_csv = []  # Author fields
authors = []  # Author names
edges = {}  # Graph edges

# CLI args
input_path = cli_args[1]
input_dlm = cli_args[3]
input_name = input_path.split("/")[3]

# Name argument override
if len(cli_args) == 5:
    input_name = cli_args[4]

# Get input files and output path
input_files = listdir(input_path)
output_path = cli_args[2] + input_name + "/"

# Create output directory if needed
if not path.isdir(output_path):
    makedirs(output_path)

# Get all files in input dir
for filename in input_files:

    # Read each file
    csv_file = open(input_path + filename, "r")
    with csv_file as current_file:

        # Parse file into records
        records = csv_parse(current_file)

        # Save metadata and create author nodes
        for record in records:

            # Save metadata
            metadata.append(record)
            author_field = record[1].split(input_dlm)

            # Parse names
            for i in range(len(author_field)):

                # Strip whitespace
                author_field[i] = author_field[i].replace(' ', '')

                # Create node and empty edge set
                if author_field[i] not in authors:
                    authors.append(author_field[i])
                    edges[author_field[i]] = []

            # Save field
            author_csv.append(author_field)

# Remove fluff from fields
author_csv = author_csv[2:]

# Create graph object
graph = nx.DiGraph()

# Create and count edges between co-authors
edge_number = 0
for field in author_csv:

    # Check for multi author papers
    if len(author_field) > 1:
        for edge_start_name in author_field:

            # Get edge start and possible edge endpoints
            edge_start_name = edge_start_name.replace(' ', '')
            name_index = author_field.index(edge_start_name)
            other_names = author_field[:name_index] + author_field[name_index + 1:]

            # Check all possible endpoints
            for edge_end_name in other_names:

                # Strip whitespace
                edge_end_name = edge_end_name.replace(' ', '')

                # Check for edge existence
                if edge_end_name not in edges[edge_start_name.strip()]:

                    # Check for edge in other direction
                    if edge_start_name not in edges[edge_end_name]:
                        # Create edge and add to graph and dict
                        graph.add_edge(edge_start_name, edge_end_name)
                        edges[edge_start_name] = edges[edge_end_name]
                        edge_number += 1


# Write gexf file for graph
edges_gexf_path = output_path + input_name + ".gexf"
nx.write_gexf(graph, edges_gexf_path)

# Write log statements to file
log_path = output_path + input_name + "log.txt"
log_handler = open(log_path, "w+")
log_msg = str(edge_number) + " author edges successfully written to " + edges_gexf_path + " in GEXF format"
log_handler.write(log_msg)
log_handler.close()
