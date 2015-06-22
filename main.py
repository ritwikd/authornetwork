import csv

__author__ = 'sld-generic'

# Create array for holding raw header fields
author_fields_csv_raw = []

# Read CSV file
with open("input/data.csv", "r") as publication_data:
    reader = csv.reader(publication_data)
    # Process by row
    for row in reader:
        # Add author field to array
        author_fields_csv_raw.append(row[1])

# Remove header fields
author_fields_csv_raw = author_fields_csv_raw[2:]
# Create array for separated author names
authors_field_csv_separated = []
# Create dict for holding ID
author_ids = {}
# Create dict for holding edges
author_edges = {}

# Parse by field per document
for author_field_csv in author_fields_csv_raw:
    # Split by semicolon delimiter
    author_names = author_field_csv.split(';')
    # Step through each individual author name
    for author_name in author_names:
        # Remove prefixed whitespace from author name
        author_name = author_name.strip()
        # Check if author already in array
        if author_name not in authors_field_csv_separated:
            # If not, add to array
            authors_field_csv_separated.append(author_name)
            author_ids[author_name] = len(authors_field_csv_separated)

# Get total number of authors
num_total_authors = len(authors_field_csv_separated)

# Create output handler and file
output_author_nodes_csv = open("output/author_nodes.csv", "w+")
# Set output file delimiter
output_author_nodes_csv_delimiter = ";"
# Write CSV column title
output_author_nodes_csv.write("Label" + output_author_nodes_csv_delimiter + "Id\n")
# Step through each author name
for author_name in authors_field_csv_separated:
    output_author_nodes_csv.write(author_name + output_author_nodes_csv_delimiter + str(author_ids[author_name]) + "\n")
# Print output
print str(num_total_authors) + " author names successfully written to file in CSV format."
# Close output handler
output_author_nodes_csv.close()

# Step through each author name
for author_name in authors_field_csv_separated:
    # Create empty edge array for each author
    author_edges[author_ids[author_name]] = []

# Step through each field in all fields
for author_field_csv in author_fields_csv_raw:
    # Split names at semicolon delimiter
    author_names = author_field_csv.split(';')
    # Step through each name in the field
    for edge_start_author in author_names:
        # Build list of all other author names in the field for edges
        author_name_index = author_names.index(edge_start_author)
        author_names_other = author_names[:author_name_index] + author_names[author_name_index + 1:]
        # Step through every possible edge end
        for edge_end_author in author_names_other:
            # Create ids for start and end of edge
            edge_start_id = author_ids[edge_start_author.strip()]
            edge_end_id = author_ids[edge_end_author.strip()]
            # Check if edge exists currently
            if edge_end_id not in author_edges[edge_start_id]:
                # Check if edge already exists in reverse
                if edge_start_id not in author_edges[edge_end_id]:
                    # Create edge
                    author_edges[edge_start_id].append(edge_end_id)

# Create output handler and file
output_author_edges_csv = open("output/author_edges.csv", "w+")
# Set output file delimiter
output_author_edges_csv_delimiter = ","
# Write CSV column title
output_author_edges_csv.write("Source" + output_author_edges_csv_delimiter + "Target\n")
# Init variable to hold number of edges
edges_total = 0
# Step through each author start id
for edge_start_id in author_edges.keys():
    # Step through each author end id
    for edge_end_id in author_edges[edge_start_id]:
        # Write edge in delimited format
        output_author_edges_csv.write(str(edge_start_id) + output_author_edges_csv_delimiter + str(edge_end_id) + "\n")
        # Increment edge total
        edges_total += 1
# Print output
print str(edges_total) + " author edges successfully written to file in CSV format."
# Close output handler
output_author_nodes_csv.close()
