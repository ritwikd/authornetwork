__author__ = 'Ritwik Dutta'

# Imports for various required modules
from csv import reader as csv_parse  # CSV parser
from shlex import split # Text splitter
from sys import argv as cli_args  # CLI args
from os import path, makedirs, listdir  # Filesystem control
import networkx as nx  # Graph creation and GEXP creation

# Global variables
metadata = []  # CSV metadata
author_csv = []  # Author fields

# Tag vars
tag_list = {}
tag_imp = { 'author' : 1, 'reviewer': 2, 'tpc' : 3}

# For edges between
inst_dict = {}
paper_dict = {}

# Create graph object
graph = nx.DiGraph()

# CLI args
input_dlm = cli_args[1]
input_name = cli_args[2]
output_path = cli_args[3] + input_name + "//"
input_paths = cli_args[5:]
multi_conf = cli_args[4]
input_files = []

# Get input files and output path
for input_dir in input_paths:

    # Get sorted subdirectories of input directories
    input_subdir = sorted(listdir(input_dir))

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
                for name in field:

                    # Strip whitespace
                    name = name.replace(' ', '')

                    # Set importance and tag
                    name_tag = "author"

                    titlewords = split(record[0].strip().replace("'", '').replace('"',''))


                    # Check for other tag
                    if len(titlewords) == 1:

                        # Add to reviewer list
                        name_tag = titlewords[0].lower()
                        importance = 3

                    # Add to corresponding part of dict
                    if name_tag not in tag_list.keys():
                        tag_list[name_tag] = []
                    tag_list[name_tag].append(name)

                    # Get importance from dict 
                    if name_tag in tag_imp.keys():
                        importance = tag_imp[name_tag]


                    # Check if multiple or single conference
                    if multi_conf == "True":

                        # Check for author conflict
                        if graph.has_node(name):
                            graph.add_node(name, id=graph.number_of_nodes()+1, conference="mixed", institution=record[2], importance=importance, tag=name_tag)

                    else:

                        # Conference field from parsed conference
                        graph.add_node(name, id=graph.number_of_nodes()+1, conference=filename[0], institution=record[2], importance=importance, tag=name_tag)

# Create array for raw people
people = []

# Populate array with all from sublists
for key in tag_list.keys():
    people += tag_list[key]

# Step through people
for person in people:

    # Default variables
    tag = ""
    importance = 0

    # Step through all keys
    for key in tag_list.keys():

        # Check for person in sublist
        if person in tag_list[key]:

            # Add new tag to author properties
            tag +=key + "_"
            if key in tag_imp.keys():
                importance +=tag_imp[key]

    # Set corresponding data in node
    graph.add_node(person, tag=tag, importance=importance)

# Remove fluff from fields
metadata = metadata[2:]

# Add authors to dictionary
for row in metadata:

    # Check for right row
    if len(row) > 2:

        # Get institution from row
        paper = row[0]

        # Get list of authors
        authors = row[1].split(input_dlm)

        # Step through authors
        for author in authors:

            # Create institution arrays when necessary
            if paper not in paper_dict.keys():
                paper_dict[paper] = []

            # Add author to dictionary under institution
            paper_dict[paper].append(author)

# Create and count edges between people from the same institution
for paper in paper_dict.keys():

    # Get all authors of institution
    authors = paper_dict[paper]

    # Step through all possible edge starts
    for edge_start_name in paper_dict[paper]:

        # Get all possible edge endpoints and strip name
        name_index = authors.index(edge_start_name)
        edge_start_name = edge_start_name.replace(' ', '')
        other_names = authors[:name_index] + authors[name_index + 1:]

        # Create all possible edges
        for edge_end_name in other_names:

            edge_end_name = edge_end_name.replace(' ', '')

            # Check for existing edges
            if not graph.has_edge(edge_start_name, edge_end_name) and paper.lower().strip() not in tag_imp.keys():

                # Add co-author connection
                graph.add_edge(edge_start_name, edge_end_name, weight=1, tag="paper")

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

            # Create institution arrays when necessary
            if institution not in inst_dict.keys():
                inst_dict[institution] = []

            # Add author to dictionary under institution
            inst_dict[institution].append(author)

# Create and count edges between people from the same institution
for institution in inst_dict.keys():

    if len(institution) < 3:
        print institution

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
            if not graph.has_edge(edge_start_name, edge_end_name):

                # Set edge tag
                tag = "institutional"

                # Check and set social tag tag
                if len(institution) < 1:
                    tag = "social"

                # Add institutional connection
                graph.add_edge(edge_start_name, edge_end_name, weight=1, tag=tag)




# Create GEXF output path
edges_gexf_path = (output_path + input_name + ".gexf")

nx.write_gexf(graph, edges_gexf_path)

# Write log statements to file
log_path = output_path + input_name + "log.txt"
log_handler = open(log_path, "w+")
log_msg = str(graph.number_of_edges()) + " author edges successfully written to " + edges_gexf_path + " in GEXF format"
log_handler.write(log_msg)
log_handler.close()
