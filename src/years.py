__author__ = 'Ritwik Dutta'

from os import listdir, system
from time import time

conferences_global_path = 'input/Years/'

conference_years = listdir(conferences_global_path)
total_start_time = time()
for year in conference_years:
    year_path = conferences_global_path + year + '/'
    time_start = time()
    system("python graph.py " + year_path + ' output/Years/ ";" ' + year)
    time_end = time()
    time_elapsed = time_end - time_start
    print "Graph of " + year + "\t generated in " + str(time_elapsed) + " seconds."

total_end_time = time()
total_elapsed_time = total_end_time - total_start_time
print "All year graphs generated in " + str(total_elapsed_time) + " seconds."
