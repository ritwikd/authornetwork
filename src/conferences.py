__author__ = 'Ritwik Dutta'

from os import listdir, system
from time import time

# Set input path for files
conferences_global_path = 'input/Conferences/'

# get names of all categories in input directory
conference_categories = listdir(conferences_global_path)

# Get start time
total_start_time = time()

for category in conference_categories:

    # Get full path to category
    conference_category_path = conferences_global_path + category + '/'

    # Get list of conferences in category
    conference_names = listdir(conference_category_path)

    for name in conference_names:

        # Get full path to conference
        conference_name_path = conference_category_path + name + '/'

        # Start timing individual run
        time_start = time()

        # Run graph generation on conference directory
        system("python graph.py " + conference_name_path + ' output/Conferences/ ";"')

        # Finish timing individual run
        time_end = time()
        time_elapsed = time_end - time_start

        # Print output message
        print "Graph of " + name + "\t generated in " + str(time_elapsed) + " seconds."

# Get total time elapse
total_end_time = time()
total_elapsed_time = total_end_time - total_start_time

# Print final output message
print "All conference graphs generated in " + str(total_elapsed_time) + " seconds."
