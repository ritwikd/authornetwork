__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csv_parse
from sys import argv as cmd_args
from os import path, makedirs, listdir
import networkx as nx

# CLI args
input_path  = cmd_args[1]
input_delim = cmd_args[3]
input_name  = input_path.split("/")[3]

# Check for name arg
if len(cmd_args) == 5:
    input_name = cmd_args[4]

# Generate full I/O paths and create folders if needed
input_data_files = listdir(input_path)
output_data_path = cmd_args[2] + input_name + "/"
if not path.isdir(output_data_path):
    makedirs(output_data_path)

# Program vars
metadata    = [] # CSV metadata
author_flds = [] # Author fields
authors     = [] # Author names
edges       = {} # Graph edges

# Get all files in input dir
for filename in input_data_files:

    # Read each file
    csv_file = open(input_path + filename, "r")
    with csv_file as current_file:

        # Parse file into records
        records = csv_parse(current_file)

        # Save metadata and create author nodes
        for record in records:

            # Save metadata
            metadata.append(record)
            author_field = record[1].split(input_delim)


            # Parse names
            for i in range(len(author_field)):

                #Strip whitespace
                author_field[i] = author_field[i].replace(' ', '')

                # Create node and empty edge set
                if author_field[i] not in authors:
                    authors.append(author_field[i])
                    edges[author_field[i]] = []

            # Save stripper
            author_flds.append(author_field)

# Remove fluff from fields
author_flds = author_flds[2:]

# Create graph object
graph = nx.DiGraph()

# Create and count edges between co-authors
edge_number = 0
for field in author_flds:

    # Get names and strip whitespace
    author_field = field.split(input_delim)
    for i in range(len(author_field)):
        author_field[i] = author_field[i].replace(' ', '')

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

                # Create edges that are nonexistent in both directions
                if edge_end_name not in edges[edge_start_name.strip()]:
                    if edge_start_name not in edges[edge_end_name]:
                        graph.add_edge(edge_start_name, edge_end_name)
                        edges[edge_start_name] = edges[edge_end_name]
                        edge_number += 1


# Write gexf file for graph
edges_gexf_fp = output_data_path + input_name + ".gexf"
nx.write_gexf(graph, edges_gexf_fp)

# Write log statements to file
log_filepath = output_data_path + input_name + "log.txt"
log_filehandler = open(log_filepath, "w+")
log_filehandler.write(str(edge_number) + " author edges successfully written to " + edges_gexf_fp + " in GEXF format")
log_filehandler.close()
