#Imports for various required modules
from csv import reader as csvreader
from sys import argv as cmd_args
from os import path,makedirs

__author__ = 'Ritwik Dutta'

#Create input path var
input_data_path = cmd_args[1]
#Create output path var
output_data_path = cmd_args[2]
#Check if output directory exists
if not path.isdir(output_data_path):
    #If not, create output path
    makedirs(output_data_path)
#Create input data delimiter var
input_data_delimiter = cmd_args[3]

# Create array for holding raw header fields
csv_author_fields = []
# Remove header fields
csv_author_fields = csv_author_fields[2:]
# Create array for separated author names
names_separated = []
# Create dict for holding ID
graph_node_ids = {}
# Create dict for holding edges
graph_edges = {}

# Read CSV file
with open(input_data_path, "r") as citation_data:
    data_reader = csvreader(citation_data)
    # Process by row
    for citation in data_reader:
        # Add author field to array
        csv_author_fields.append(citation[1])

# Parse by field per document
for field in csv_author_fields:
    # Split by semicolon delimiter
    field_names = field.split(input_data_delimiter)
    # Step through each individual author name
    for name in field_names:
        # Remove prefixed whitespace from author name
        name = name.strip()
        # Check if author already in array
        if name not in names_separated:
            # If not, add to array
            names_separated.append(name)
            graph_node_ids[name] = len(names_separated)
# Get total number of authors
total_names = len(names_separated)

# Create output handler and file
csv_nodes_fh = open(output_data_path + "author_nodes.csv", "w+")
# Set output nodes file delimiter
csv_nodes_delimiter = ";"
# Write CSV column title
csv_nodes_fh.write("Label" + csv_nodes_delimiter + "Id\n")
# Step through each author name
for name in names_separated:
    csv_nodes_fh.write(name + csv_nodes_delimiter + str(graph_node_ids[name]) + "\n")
# Print output nodes info
print str(total_names) + " author names successfully written to file in CSV format."
# Close output nodes handler
csv_nodes_fh.close()

# Step through each author name
for name in names_separated:
    # Create empty edge array for each author
    graph_edges[graph_node_ids[name]] = []

# Step through each field in all fields
for field in csv_author_fields:
    # Split names at semicolon delimiter
    field_names = field.split(';')
    # Step through each name in the field
    for edge_start_name in field_names:
        # Build list of all other author names in the field for edges
        name_index = field_names.index(edge_start_name)
        other_names = field_names[:name_index] + field_names[name_index + 1:]
        # Step through every possible edge end
        for edge_end_name in other_names:
            # Create ids for start and end of edge
            edge_start_id = graph_node_ids[edge_start_name.strip()]
            edge_end_id = graph_node_ids[edge_end_name.strip()]
            # Check if edge exists currently
            if edge_end_id not in graph_edges[edge_start_id]:
                # Check if edge already exists in reverse
                if edge_start_id not in graph_edges[edge_end_id]:
                    # Create edge
                    graph_edges[edge_start_id].append(edge_end_id)

# Create output edges handler and file
csv_edges_fh = open(output_data_path + "author_edges.csv", "w+")
# Set output edges file delimiter
csv_edges_delimiter = ","
# Write CSV column title
csv_edges_fh.write("Source" + csv_edges_delimiter + "Target\n")
# Create variable to hold number of edges
total_edges = 0
# Step through each author start id
for edge_start_id in graph_edges.keys():
    # Step through each author end id
    for edge_end_id in graph_edges[edge_start_id]:
        # Write edge in delimited format
        csv_edges_fh.write(str(edge_start_id) + csv_edges_delimiter + str(edge_end_id) + "\n")
        # Increment edge total
        total_edges += 1
# Print output edges
print str(total_edges) + " author edges successfully written to file in CSV format."
# Close output edges handler
csv_edges_fh.close()
