__author__ = 'Ritwik'

from generator import years, conferences

print "Generating per-conference graphs.\n"
conferences.run("generator/main/graph.py")
print "\nGeneration completed.\n"


print "Generating per-year graphs.\n"
years.run("generator/main/graph.py")
print "\nGeneration completed.\n"

