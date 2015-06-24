__author__ = 'Ritwik Dutta'

from os import listdir, system
from time import time

# Set input path for files
years_global_path = 'input/Years/'

# Get names of all years in input directory
conference_years = listdir(years_global_path)

# Get start time
total_start_time = time()

for year in conference_years:

    # Get full path to year
    year_path = years_global_path + year + '/'

    # Start timing individual run
    time_start = time()

    # Run graph generation on year directory
    system("python graph.py " + year_path + ' output/Years/ ";" ' + year)

    # Finish timing individual run
    time_end = time()
    time_elapsed = time_end - time_start

    # Print output message
    print "Graph of " + year + "\t generated in " + str(time_elapsed) + " seconds."

# Get total time elapsed
total_end_time = time()
total_elapsed_time = total_end_time - total_start_time

# Print final output message
print "All year graphs generated in " + str(total_elapsed_time) + " seconds."
