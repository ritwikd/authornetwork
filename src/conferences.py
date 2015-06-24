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

    # Enable non directory data to be in path
    try:

        # Get list of conferences in category
        conference_names = listdir(conference_category_path)

        for name in conference_names:

            # Get full path to conference
            conference_path = conference_category_path + name + '/'

            # Start timing individual run
            time_start = time()

            # Run graph generation on conference directory
            system('python graph.py ";" ' + name + ' output/Conferences/ ' + conference_path)

            # Finish timing individual run
            time_end = time()
            time_elapsed = time_end - time_start

            # Print output message
            print "Graph of " + name + "\t generated in " + str(round(time_elapsed, 3)) + " seconds."

    # Catch cases of non-directory items
    except OSError:
        pass


# Get total time elapse
total_end_time = time()
total_elapsed_time = total_end_time - total_start_time

# Print final output message
print "All conference graphs generated in " + str(round(total_elapsed_time, 3)) + " seconds."
