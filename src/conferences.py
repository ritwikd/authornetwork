__author__ = 'Ritwik Dutta'

from os import listdir, system
from time import time

conferences_global_path = 'input/Conferences/'

conference_categories = listdir(conferences_global_path)
for category in conference_categories:
    conference_category_path = conferences_global_path+ category + '/'
    conference_names = listdir(conference_category_path)
    for name in conference_names:
        conference_name_path = conference_category_path +  name + '/'
        time_start = time()
        system("python graph.py " + conference_name_path + ' output/Conferences/ ";"')
        time_end = time()
        time_elapsed = time_end - time_start
        print "Graph of " + name + " generated in " + str(time_elapsed) + " seconds."

print "All conference graphs generated."