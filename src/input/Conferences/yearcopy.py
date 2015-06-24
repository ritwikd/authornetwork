__author__ = 'Ritwik Dutta'

from os import system, makedirs

year_start = 1995
year_range = 20

for year in xrange(year_start, year_start + year_range + 1):
    makedirs('../Years/' + str(year))
    command = 'cp `find . -type f | grep '+ str(year) + '` ../Years/' + str(year) + ''
    system(command)
