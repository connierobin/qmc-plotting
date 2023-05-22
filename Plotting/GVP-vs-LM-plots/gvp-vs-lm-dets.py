from asyncio import format_helpers
from json.tool import main
import os, sys
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import statistics

# Go through the file to extract the ci values and tags
def process_file(filename, frozen_J):
    # Arrays to hold the resulting data
    frozen_J_vars = []      # contains the J's that should be included at every iter if it's frozen
    this_iter_vars = []     # list of numbers
    all_iters_vars=[]       # list of lists of numbers
    tags=[]                 # list of variable types. E.g. 'ci', 'ci', 'ci', 'eH', 'eH', ...
    # Variables to track where we are in the file
    updatesection = False
    collecting = False
    havetags = False
    collecting_frozen_J = False
    done_collecting_frozen_J = not frozen_J
    frozen_J_start = 'Wavefunction setup'
    frozen_J_end = 'Created SPOSet builder'
    # Open file
    f=open(filename,'r')
    # Process lines in file one at a time
    for line in f:
        if frozen_J and not done_collecting_frozen_J:
            if collecting_frozen_J:
                # check for the 'done' string
                if frozen_J_end in line:
                    # print("done collecting frozen J")
                    collecting_frozen_J = False
                    done_collecting_frozen_J = True
                # attempt to collect a J parameter if it is present. Since the J's are frozen it should say OFF
                elif 'OFF' in line:
                    # print(f'tag: {str(line.split()[0])}')
                    # grab the tag
                    tags.append(str(line.split()[0]))
                    # grab the value
                    frozen_J_vars.append(float(line.split()[1]))
            elif frozen_J_start in line:
                collecting_frozen_J = True
        # Collecting set to true upon finding an <optVariables> tag
        # Stop collecting when we hit the end of the variable section
        if collecting and "</optVariables" not in line:
            this_iter_vars.append(float(line.split()[1]))
            # Also grab the tags for the different variable sets (uu, ud, eX, ci, etc.)
            # Only do this on the first iteration
            if not havetags:
                # print(f'acquiring tag: {str(line.split()[0])}')
                tags.append(str(line.split()[0]))
                # temp = str(line.split()[0])
                # tags.append(temp.split("_")[0])
        elif "<optVariables" in line and not updatesection:
            collecting = True
            # print(f"start collecting. tags length: {len(tags)}")
            if frozen_J:
                [this_iter_vars.append(frozen_J_vars[i]) for i in range(len(frozen_J_vars))]
        elif "</optVariables" in line:
            if len(tags)>0:
                havetags=True
            collecting = False
            if (len(this_iter_vars)>0):
                all_iters_vars.append(this_iter_vars)
            this_iter_vars = []
            if updatesection:
                updatesection = False
        # If using the hybrid method, linear method, or block linear method
        # An intermediate set of parameters is printed, don't collect these
        elif "initial energy" in line or "Updating the guiding" in line:
            updatesection=True
        elif "Applying the update" in line:
            updatesection=False
    f.close()
    return (all_iters_vars, tags)

# Find avg10 values for each parameter, collapsing all iterations into just one vector
def calc_avg10_from_data(all_files_vars):
    all_files_avg10 = []
    for vars in all_files_vars:
        num_iters = len(vars)
        num_params = len(vars[0])
        this_file_avg10 = np.zeros(num_params)
        for iter in vars:
            for ci_index in range(len(iter)):
                this_file_avg10[ci_index] += iter[ci_index]
        for i in range(len(this_file_avg10)):
            this_file_avg10[i] = this_file_avg10[i] / num_iters
        all_files_avg10.append(this_file_avg10)
    return all_files_avg10

# Find all the norm_params for all the iterations
def all_norm_param(list_list_coeff, aufbau_coeff):
    all_norm_coeff = []
    iter_counter = 0
    for list_coeff in list_list_coeff:
        this_iter_norm_coeff = []
        iter_counter += 1
        total = sum([coeff*coeff for coeff in list_coeff]) + aufbau_coeff ** 2
        #print(f"Normalized CI iteration {iter_counter}:")
        for i in range(len(list_coeff)):
            #print(list_coeff[i]*list_coeff[i]/total)
            this_iter_norm_coeff.append(list_coeff[i]*list_coeff[i]/total)
        all_norm_coeff.append(this_iter_norm_coeff)
    return all_norm_coeff

# Find all the percent_params for all the iterations
def all_percent_param(list_list_coeff, aufbau_coeff):
    # whether to do paired up or not paired up
    do_paired_up = False
    # get the norm info as a starting point
    all_norm_coeff = all_norm_param(list_list_coeff, aufbau_coeff)
    # set up
    all_percent_coeff = []
    # calculate percentages
    for list_coeff in all_norm_coeff:
        if do_paired_up:
            print("Using paired up coeffs")
            if len(list_coeff) % 2 != 0:
                print("Possible incorrect behavior: odd number of coefficients. Paired up percentages may be off by one.")
                altered_list_coeff = [list_coeff[2*i+1] + list_coeff[2*i+2] for i in range(int(len(list_coeff) / 2))]
            else:
                altered_list_coeff = [list_coeff[2*i] + list_coeff[2*i+1] for i in range(int(len(list_coeff) / 2))]
        else:
            print("Not using paired up coeffs")
            altered_list_coeff = list_coeff
        print(f"length of altered list: {len(altered_list_coeff)}")
        # Calculate normalized aufbau coeff
        total_from_norm = sum([coeff*coeff for coeff in altered_list_coeff]) + aufbau_coeff ** 2
        normalized_aufbau_coeff = abs(aufbau_coeff) / total_from_norm
        # Calculate total of all paired up values
        total = sum(altered_list_coeff) + normalized_aufbau_coeff
        # calculate percentages
        this_iter_percent_coeff = []
        for i in range(len(altered_list_coeff)):
            this_iter_percent_coeff.append(altered_list_coeff[i] / total)
        all_percent_coeff.append(this_iter_percent_coeff)
    return all_percent_coeff

# Plot GVP data and LM data on one plot
def plot_gvp_and_lm_data(all_gvp_files_data, all_lm_files_data, dets_range, title, x, ticks):
    # First, plot the norms
    plt.figure(title)
    #plt.xticks(x, ticks)
    for i in range(len(all_gvp_files_data)):
        gvp_data = all_gvp_files_data[i]
        x = np.arange(len(gvp_data))
        plt.plot(x, gvp_data, marker='o', label='gvp %s' % (dets_range[i]))
    for i in range(len(all_lm_files_data)):
        lm_data = all_lm_files_data[i]
        x = np.arange(len(lm_data))
        plt.plot(x, lm_data, marker='o', label='lm %s' % (dets_range[i]))
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))

# Plot difference data
def plot_difference(all_files_difference_data, dets_range, title, x, ticks):
    plt.figure(title)
    plt.xticks(x, ticks)
    for i in range(len(all_files_difference_data)):
        this_file_difference_data = all_files_difference_data[i]
        x = np.arange(len(this_file_difference_data))
        plt.plot(x, this_file_difference_data, marker='o', label='%s' % (dets_range[i]))
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("GVP minus LM")

def main():
    ############################
    # TEST-SPECIFIC PARAMETERS #
    ############################
    # Files to read from 004 to 016. The zfill function prepends a "0" for the single digit numbers. 
    #dets_range = list(range(4, 18, 2))
    #dets_range = list(range(4, 8 , 2))
    #dets_range.extend([32, 64, 128, 256, 384, 512])
    #gvp_files = [f"GVP/h2onosym-gvp-dets{str(i).zfill(3)}-1.out" for i in dets_range]
    #lm_files = [f"LM/h2onosym-lm-dets{str(i).zfill(3)}-1.out" for i in dets_range]
    # gvp_files = ["h2onosym-gvpj-2b.out"]
    # lm_files = ["h2onosym-lm-ts-1.out"]
    gvp_files = ["h2onosym-gs-2M-1mili-1.out"]      # 8/30/22 Trying to see why my LM ground state is so much better than my GVP ground state
    lm_files = ["h2onosym-lm-gs-10.out"]
    gvp_frozen_J = [True]
    lm_frozen_J = [False]
    dets_range = [1]

    ################
    # GENERAL CODE #
    ################
    # Array to hold the resulting data
    all_gvp_files_vars = []
    all_gvp_files_tags = []
    all_lm_files_vars = []
    all_lm_files_tags = []
    # Read all the files
    for (gvp_file, frozen_J) in zip(gvp_files, gvp_frozen_J):
        print(f"Processing {gvp_file} with frozen J = {frozen_J}...")
        (this_file_vars, this_file_tags) = process_file(gvp_file, frozen_J)
        all_gvp_files_vars.append(this_file_vars)
        all_gvp_files_tags.append(this_file_tags)
    for (lm_file, frozen_J) in zip(lm_files, lm_frozen_J):
        print(f"Processing {lm_file} with frozen J = {frozen_J}...")
        (this_file_vars, this_file_tags) = process_file(lm_file, frozen_J)
        all_lm_files_vars.append(this_file_vars)
        all_lm_files_tags.append(this_file_tags)
    # Check that the tags match between GVP and LM
    for i in range(len(all_gvp_files_tags[-1])):
        if all_gvp_files_tags[-1][i] != all_lm_files_tags[-1][i]:
            print(f"Tag mismatch found. GVP: {all_gvp_files_tags[-1][i]}\tLM: {all_lm_files_tags[-1][i]}")
    # First calculate the average of the final 10 values to get a less biased / random result to consider
    # This also collapses all of the iterations of ci values down to just one list of ci values per file
    all_gvp_files_avg10 = calc_avg10_from_data(all_gvp_files_vars)
    all_lm_files_avg10 = calc_avg10_from_data(all_lm_files_vars)
    # Next calculate the norms of all of the ci values so they are more comparable between GVP and LM
    all_gvp_files_norm = all_norm_param(all_gvp_files_avg10, 0) # aufbau set to 0 because this is excited state
    all_lm_files_norm = all_norm_param(all_lm_files_avg10, 0)
    # Calculate the percents differences for the GVP results vs. the LM results
    all_gvp_files_percent = all_percent_param(all_gvp_files_avg10, 0) # aufbau set to 0 because this is excited state
    all_lm_files_percent = all_percent_param(all_lm_files_avg10, 0)
    # Subtract to get the percent differences and the norm differences, making sure to subtract the correct ones
    all_files_norm_difference = [[all_gvp_files_norm[i][j] - all_lm_files_norm[i][j] for j in range(len(all_gvp_files_norm[i]))] for i in range(len(all_gvp_files_norm))]
    all_files_percent_difference = [[all_gvp_files_percent[i][j] - all_lm_files_percent[i][j] for j in range(len(all_gvp_files_percent[i]))] for i in range(len(all_gvp_files_percent))]
    
    # PLOTTING
    # Set up for all plots
    tags_length = len(all_gvp_files_tags[-1])
    x = np.array(range(tags_length))
    ticks = all_gvp_files_tags[-1]
    # First, plot the norms
    plot_gvp_and_lm_data(all_gvp_files_norm, all_lm_files_norm, dets_range, "norm", x, ticks)
    # Next, plot the percents
    plot_gvp_and_lm_data(all_gvp_files_percent, all_lm_files_percent, dets_range, "percent", x, ticks)
    # Plot the differences
    plot_difference(all_files_norm_difference, dets_range, 'norm differences', x, ticks)
    half_tags_length = int(tags_length / 2)
    x = np.array(range(half_tags_length))
    ticks = [all_gvp_files_tags[-1][2*i+1] for i in range(half_tags_length)]
    plot_difference(all_files_percent_difference, dets_range, 'percent differences', x, ticks)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0))
    plt.show()

if __name__ == "__main__":
    main()
