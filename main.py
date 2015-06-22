import csv
__author__ = 'sld-generic'


author_fields_csv_raw = []

#Read CSV file
with open("data.csv", "r") as publication_data:
    reader = csv.reader(publication_data)
    #Process by row
    for row in reader:

        author_fields_csv_raw.append(row[1])

author_fields_csv_raw = author_fields_csv_raw[2:]

authors_field_csv_separated = []

for author_field_csv in author_fields_csv_raw:
    author_names = author_field_csv.split(';')
    for author_name in author_names:
        if author_name not in authors_field_csv_separated:
            authors_field_csv_separated.append(author_name)

output_author_nodes_csv = open("output/author_nodes.csv", "w+")

for author in authors_field_csv_separated:
    output_author_nodes_csv.write(author + ",")
output_author_nodes_csv.close()


