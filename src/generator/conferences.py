__author__ = 'Ritwik Dutta'

def run(gen_path):

    from os import listdir, system
    from time import time
    from platform import platform
    from tqdm import tqdm

    # Set input path for files
    conferences_global_path = 'input/Conferences/'

    # Get names of all categories in input directory
    conference_categories = listdir(conferences_global_path)

    # Create array to store conference paths
    conference_paths = []

    # Get start time
    total_start_time = time()

    # Step through all categories
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

                #Add to array
                conference_paths.append(conference_path)

        # Catch cases of non-directory items
        except OSError:
            pass

    # Go through all conference paths
    for i in tqdm(range(len(conference_paths))):

        # Create graph generation command
        gen_cmd = 'python ' + gen_path + ' ";" ' + name + ' output/Conferences/ ' + conference_paths[i]

        # Modify query for Windows systems
        if 'Windows' in platform():
            gen_cmd = 'C:\Python27\python.exe ' + gen_path + ' ";" ' + name + ' output/Conferences/ ' + conference_paths[i]

        # Run graph generation on year directory
        system(gen_cmd)

        # Generate and print output
        split_path = conference_paths[i].split('/')


    # Get total time elapse
    total_end_time = time()
    total_elapsed_time = total_end_time - total_start_time

    # Print final output message
    print "All conference graphs generated in " + str(round(total_elapsed_time, 3)) + " seconds."
