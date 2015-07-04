__author__ = 'Ritwik Dutta'

def run(gen_path):

    from os import listdir, system
    from time import time
    from platform import platform
    from tqdm import tqdm


    # Set input path for files
    years_global_path = 'input/Years/'

    # Get names of and count all years in input directory
    conference_years = sorted(listdir(years_global_path))

    # Get start time
    total_start_time = time()

    # Go through all years
    for i in tqdm(range(len(conference_years))):

        # Get year variable
        year = conference_years[i]

        # Make sure non-directory paths are not run
        if '.' not in year:

            # Get full path to year
            year_path = years_global_path + year + '/'

            # Create graph generation command
            gen_cmd = 'python ' + gen_path + ' ";" ' + year + ' output/Years/ ' + year_path

            # Modify query for Windows systems
            if 'Windows' in platform():
                gen_cmd = 'C:\Python27\python.exe ' + gen_path + ' ";" ' + year + ' output/Years/ True ' + year_path

            # Run graph generation on year directory
            system(gen_cmd)



    # Get total time elapsed
    total_end_time = time()
    total_elapsed_time = total_end_time - total_start_time


    # Print final output message
    print "All year graphs generated in " + str(total_elapsed_time) + " seconds."
