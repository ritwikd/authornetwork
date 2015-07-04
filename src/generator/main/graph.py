__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csv_parse  # CSV parser
from sys import argv as cli_args  # CLI args
from os import path, makedirs, listdir  # Filesystem control
import networkx as nx  # Graph creation and GEXP creation

# Global variables
metadata = []  # CSV metadata
author_csv = []  # Author fields
# For edges between
inst_dict = {}
# Create graph object
graph = nx.DiGraph()

# CLI args
input_dlm = cli_args[1]
input_name = cli_args[2]
output_path = cli_args[3] + input_name + "/"
input_paths = cli_args[5:]
multi_conf = cli_args[4]
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

            # Make sure record is a valid publication record
            if len(record) > 2:

                # Save metadata
                metadata.append(record)
                field = record[1].split(input_dlm)

                # Parse names
                for i in range(len(field)):

                    # Strip whitespace
                    field[i] = field[i].replace(' ', '')

                    # Check if multiple or single conference
                    if multi_conf == "True":

                        # Check for author conflict
                        if graph.has_node(field[i]):

                            # Mixed conference field
                            graph.add_node(field[i], conference="Mixed", institution=record[2], importance=1)

                    else:

                        # Conference field from parsed conference
                        graph.add_node(field[i], id=graph.number_of_nodes()+1, conference=filename[0], institution=record[2], importance=1)

                # Save field
                author_csv.append(field)

# Remove fluff from fields
author_csv = author_csv[2:]
metadata = metadata[2:]

# Create and count edges between co-authors
for field in author_csv:

    # Check for multi author papers
    if len(field) > 1:

        # Step through all possible edge starts
        for edge_start_name in field:

            # Get all possible edge endpoints
            name_index = field.index(edge_start_name)
            other_names = field[:name_index] + field[name_index + 1:]

            # Create all possible edges
            for edge_end_name in other_names:

                # Check for existing edges
                if graph.has_edge(edge_start_name, edge_end_name):

                     # Get existing edge info
                    edge_info = graph.get_edge_data(edge_start_name, edge_end_name)

                    # Get new weight
                    new_weight = edge_info['weight'] + 1
                    if new_weight > 2:
                        new_weight = 2

                    #Increment edge size
                    graph.add_edge(edge_start_name, edge_end_name, weight=new_weight)

                # Add edge
                graph.add_edge(edge_start_name, edge_end_name, weight=1)

# Create institution connection dictionary
for row in metadata:

    # Check for right row
    if len(row) > 2:

        # Get institution from row
        institution = row[2]

        # Create arr for institution
        inst_dict[institution] = []

# Add authors to dictionary
for row in metadata:

    # Check for right row
    if len(row) > 2:

        # Get institution from row
        institution = row[2]
        # Get list of authors
        authors = row[1].split(input_dlm)
        # Step through authors
        for author in authors:
            # Add author to dictionary under institution
            inst_dict[institution].append(author)

# Create and count edges between people from the same institution
for institution in inst_dict.keys():

    # Get all authors of institution
    authors = inst_dict[institution]
    # Step through all possible edge starts
    for edge_start_name in inst_dict[institution]:

        # Get all possible edge endpoints and strip name
        name_index = authors.index(edge_start_name)
        edge_start_name = edge_start_name.replace(' ', '')
        other_names = authors[:name_index] + authors[name_index + 1:]

        # Create all possible edges
        for edge_end_name in other_names:

            edge_end_name = edge_end_name.replace(' ', '')

            # Check for existing edges
            if graph.has_edge(edge_start_name, edge_end_name):

                # Get existing edge info
                edge_info = graph.get_edge_data(edge_start_name, edge_end_name)

                # Get new weight
                new_weight = edge_info['weight'] + 1
                if new_weight > 2:
                    new_weight = 2

                #Increment edge size
                graph.add_edge(edge_start_name, edge_end_name, weight=new_weight)

                # Change nodes to higher weight
                graph.add_node(edge_start_name, importance=3)
                graph.add_node(edge_end_name, importance=3)

            else:

                # Add institutional connection
                graph.add_edge(edge_start_name, edge_end_name, weight=1)

# Create GEXF output path
edges_gexf_path = output_path + input_name + ".gexf"

try:

    # Write gexf file for graph
    nx.write_gexf(graph, edges_gexf_path)

except IOError:

    # Output for errors with file input and output
    print edges_gexf_path + " cannot be written."

# Write log statements to file
log_path = output_path + input_name + "log.txt"
log_handler = open(log_path, "w+")
log_msg = str(graph.number_of_edges()) + " author edges successfully written to " + edges_gexf_path + " in GEXF format"
log_handler.write(log_msg)
log_handler.close()
