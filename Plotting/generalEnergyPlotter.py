#! /usr/bin/env python

import optparse
import os
import sys
import copy

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import math

# Colors to plot with. From ColorBrewer, at colorbrewer2.org
color_list = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3','#ff7f00', '#ffff33', '#a65628', '#f781bf', '#999999']

# Hard coded maximum limit of the x axis
maxIter = 100           # max value of x axis

# Arrays to hold the input info given by the user
qmc_files = []  # array of filenames to read through
plotting_choices = []   # array of numbers indicating which quantities to plot
data_labels = []        # a list of the labels to use for the plot

# Strings to search for in the output files
# Different data is printed at each iteration when using the Linear Method or another method
# If certain data is not printed for a method, a nonsense string is used as the indicator for
# the data to ensure that there are no hits for it.
LM_str_dict = {'energy': 'le_mean =',
               'uncertainty_of_variance': 'uncertainty =',  # std err of variance
               'variance': 'le_variance =',
               'std_err': 'stat err =',
               'target': 'target function =',
               'target_err': 'target stat err =',
               'std_dev': 'std dev =',
               'grad_norm': 'not printed in Linear Method',
               'param_update_size': 'not printed in the Linear Method',
               'largest_param_update': 'not printed in the Linear Method',
               'method_identifier': 'Inside LM engine\'s get_param',
               'data_start': 'Double check filter inside engine_checkConfig: false',
               'data_end': 'Solving the linear method equations'}

#TODO:Connie look at computeFinalizationUncertainties() in DescentEngine.cpp to see if the uncertainty
# of variance is in fact printed in the descent methods. 
descent_str_dict = {'energy': 'Energy Average:',
                    'uncertainty_of_variance': 'not printed outside Linear Method',
                    'variance': 'Energy Variance:',
                    'std_err': 'Energy Standard Error:',
                    'target': 'Target Function Average:',
                    'target_err': 'Target Function Error:',
                    'std_dev': 'Energy Standard Deviation:',
                    'grad_norm': 'Norm of gradient vector:',    # grad norm of target function, not of energy. 
                    'param_update_size': 'Parameter update vector magnitude:',
                    'largest_param_update': 'Largest magnitude parameter update:',
                    'method_identifier': 'Omega from input file',
                    'data_start': 'Before engine_checkConfigurations',
                    'data_end': 'Computing average energy and its variance over stored steps and its standard error'}

target_dict = {'excited': 'Target: excited state',
               'excited_closest': 'Target: closest excited state',
               'gvp': 'Target: generalized variational principle',
               'ground': 'Target: ground state'}

# TODO:Connie change from curly braces to a regular array
# Arrays to hold the lists of data from each file. 
# If a file does not have this information, the entry will be a blank list for the
# element corresponding to that file. 
energies = {}
uncertainties_of_variances = {}
variances = {}
std_err = {}
target_fn = {}
target_std_err = {}
std_dev = {}
grad_norms = {}
param_update_sizes = {}
largest_param_updates = {}

# Values for the average of the last 10 iterations for various values. 
# Will only be correct for the current file being read. 
avg10E = 0.0
avg10std_err = 0.0
avg10target_fn = 0.0
avg10target_std_err = 0.0
avg10std_dev = 0.0
avg10variances = 0.0
avg10uncertainty_of_variances = 0.0
avg10grad_norms = 0.0
avg10param_update_sizes = 0.0
avg10largest_param_updates = 0.0

# Values for the standard devation of the last 10 iterations for various values. 
# Will only be correct for the current file being read. 
stdev10E = 0.0
stdev10std_err = 0.0
stdev10target_fn = 0.0
stdev10target_std_err = 0.0
stdev10std_dev = 0.0
stdev10variances = 0.0
stdev10uncertainty_of_variances = 0.0
stdev10grad_norms = 0.0
stdev10param_update_sizes = 0.0
stdev10largest_param_updates = 0.0

# Arrays to hold the lists of data to plot. 
# If data does not exist or is not supposed to be plotted for a given file and data piece,
# the corresponding list will be an empty list. 
energy_to_plot = []
uncertainties_of_variances_to_plot = []
variance_to_plot = []
std_err_to_plot = []
target_fn_to_plot = []
target_std_err_to_plot = []
std_dev_to_plot = []
grad_norms_to_plot = []
param_update_sizes_to_plot = []
largest_param_updates_to_plot = []

# Holds all of the avg10 data for all the files. Each list holds the data in the order of the files. 
# Data for a given data piece for a given file is an average from the last 10 iterations. 
energy_avg10_list = []
uncertainties_of_variances_avg10_list = []
variance_avg10_list = []
std_err_avg10_list = []
target_fn_avg10_list = []
target_std_err_avg10_list = []
std_dev_avg10_list = []
grad_norms_avg10_list = []
param_update_sizes_avg10_list = []
largest_param_updates_avg10_list = []

# Holds all of the stdev10 data for all the files. Each list holds the data in the order of the files. 
# Data for a given data piece for a given file is the standard deviation of the last 10 iterations. 
energy_stdev10_list = []
uncertainties_of_variances_stdev10_list = []
variance_stdev10_list = []
std_err_stdev10_list = []
target_fn_stdev10_list = []
target_std_err_stdev10_list = []
std_dev_stdev10_list = []
grad_norms_stdev10_list = []
param_update_sizes_stdev10_list = []
largest_param_updates_stdev10_list = []

# Reads the options provided from the command line. 
def parse_options(args):
    '''Parse arguments from the command line. Expecting 1 input file name.'''

    parser = optparse.OptionParser(usage=__doc__)
    (options, filename) = parser.parse_args(args)

    if len(filename) == 0:
        parser.print_help()
        sys.exit(1)

    return (options, filename)

# Reads the input file to gather the names of the output files to read, 
# the data labels to use, and which sets of data to plot. 
def read_input_file(input_file):
    f = open(input_file, 'r')
    input_lines = f.readlines()

    for choice in input_lines[0].split():
        plotting_choices.append(choice)
    #plotting_choices.append(input_lines[0].split())

    for line in input_lines[1:]:
        words = line.split()
        qmc_files.append(words[0])
        data_labels.append(words[1])
        #plotting_choices.append(words[2:])

# Pulls data from the given file and populates all the relevant global variables.
# Namely:
# - LinearMethodUsed or DescentMethodUsed
# - lists: energies, variances, uncertainties_of_variances, std_err, target_fn, target_std_err, std_dev, grad_norms
def extract_data(qmc_file):

    # Need to identify based on the file whether it's using LM or just descent methods
    LinearMethodUsed = False
    DescentMethodUsed = False

    # Try to identify based on the file which type of variational principle is being optimized
    TargetExcitedUsed = False
    TargetExcitedClosestUsed = False
    TargetGVPUsed = False
    TargetGroundUsed = False

    # Set up variables for looping through each line of the file
    have_data = False
    iteration = 0
    f = open(qmc_file)

    for line in f:
        # Check if the identifier line for either is here, to identify which method this file uses
        if not (LinearMethodUsed or DescentMethodUsed):
            if LM_str_dict['method_identifier'] in line:
                LinearMethodUsed = True
                str_dict = LM_str_dict
                print("The following values are reported from the Linear Method")
            elif descent_str_dict['method_identifier'] in line:
                DescentMethodUsed = True
                str_dict = descent_str_dict
                print("The following values are reported from a descent method")
            else:
                continue

        # Check if the target identifier line is used, to identify which variational principle is targeted
        if not (TargetExcitedUsed or TargetExcitedClosestUsed or TargetGVPUsed or TargetGroundUsed):
            if target_dict['excited'] in line:
                TargetExcitedUsed = True
            elif target_dict['excited_closest'] in line:
                TargetExcitedClosestUsed = True
            elif target_dict['gvp'] in line:
                TargetGVPUsed = True
            elif target_dict['ground'] in line:
                TargetGroundUsed = True

        if str_dict['data_start'] in line:
            have_data = True

        if have_data:
            if str_dict['energy'] in line:
                values = line.split()
                energies[iteration] = float(values[-1])
            elif str_dict['uncertainty_of_variance'] in line:
                values = line.split()
                uncertainties_of_variances[iteration] = float(values[-1])
            elif str_dict['variance'] in line:
                values = line.split()
                variances[iteration] = float(values[-1])
            elif str_dict['std_err'] in line:
                values = line.split()
                std_err[iteration] = float(values[-1])
            elif str_dict['target'] in line:
                values = line.split()
                if 'N/A' in values[3]:
                    target_fn[iteration] = 0.0
                elif 'Average' not in values[3]:    # TEMPORARY FIX
                #else:
                    target_fn[iteration] = float(values[-1])
            elif str_dict['target_err'] in line:
                values = line.split()
                target_std_err[iteration] = float(values[-1])
            elif str_dict['std_dev'] in line:
                values = line.split()
                std_dev[iteration] = float(values[-1])
            elif str_dict['grad_norm'] in line:
                values = line.split()
                grad_norms[iteration] = float(values[-1])
            elif str_dict['param_update_size'] in line:
                values = line.split()
                param_update_sizes[iteration] = float(values[-1])
            elif str_dict['largest_param_update'] in line:
                values = line.split()
                largest_param_updates[iteration] = float(values[-1])
            elif str_dict['data_end'] in line:
                # TODO:Connie modify this so that instead of "iteration" it's "number of samples"
                # so that LM results and regular descent results are easier to compare
                have_data = False
                iteration += 1

        if str_dict['data_start'] in line:
            have_data = True

    f.close()

# Checks that the data vectors are all the same length, so that the printing doesn't fail
def check_data():
    wrong_lengths = False
    # Check that all the data is the same length
    if len(energies) != len(variances) and len(variances) != 0:
        wrong_lengths = True
    if len(energies) != len(uncertainties_of_variances) and len(uncertainties_of_variances) != 0:
        wrong_lengths = True
    if len(energies) != len(std_err) and len(std_err) != 0:
        wrong_lengths = True
    if len(energies) != len(target_fn) and len(target_fn) != 0:
        wrong_lengths = True
    if len(energies) != len(target_std_err) and len(target_std_err) != 0:
        wrong_lengths = True
    if len(energies) != len(std_dev) and len(std_dev) != 0:
        wrong_lengths = True
    if len(energies) != len(grad_norms) and len(grad_norms) != 0:
        wrong_lengths = True
    if len(energies) != len(param_update_sizes) and len(param_update_sizes) != 0:
        wrong_lengths = True
    if len(energies) != len(largest_param_updates) and len(largest_param_updates) != 0:
        wrong_lengths = True
    if wrong_lengths:    
        print("Error: data is not the same length")
        print("energies: " + str(len(energies)))
        print("variances: " + str(len(variances)))
        print("uncertainties_of_variances: " + str(len(uncertainties_of_variances)))
        print("std_err: " + str(len(std_err)))
        print("target_fn: " + str(len(target_fn)))
        print("target_std_err: " + str(len(target_std_err)))
        print("std_dev: " + str(len(std_dev)))
        print("grad_norms: " + str(len(grad_norms)))
        print("param_update_sizes: " + str(len(param_update_sizes)))
        print("largest_param_updates: " + str(len(largest_param_updates)))
        sys.exit(1)

# Print all the data extracted from the data files, as well as the average of the
# last 10 numbers for each quantity to get a finalized value.
def print_data():
    # Print the header.
    sys.stdout.write(' #1._Iteration')
    if len(energies) > 0:
        column_text = '2._Energy'
        sys.stdout.write('%22s' % column_text)
    if len(std_err) > 0:
        column_text = '3._Error'
        sys.stdout.write('%22s' % column_text)
    if len(target_fn) > 0:
        column_text = '4._Target_function'
        sys.stdout.write('%22s' % column_text)
    if len(target_std_err) > 0:
        column_text = '5._Target_error'
        sys.stdout.write('%22s' % column_text)
    if len(std_dev) > 0:
        column_text = '6._Standard_deviation'
        sys.stdout.write('%22s' % column_text)
    if len(variances) > 0:
        column_text = '7._Crude:_Variance'
        sys.stdout.write('%22s' % column_text)
    if len(uncertainties_of_variances) > 0:
        column_text = '8._Crude:_uncertainty_of_Variance'
        sys.stdout.write('%22s' % column_text)
    if len(grad_norms) > 0:
        column_text = '9._Grad_norms'
        sys.stdout.write('%22s' % column_text)
    if len(param_update_sizes) > 0:
        column_text = '10._Param_update_sizes'
        sys.stdout.write('%22s' % column_text)
    if len(largest_param_updates) > 0:
        column_text = '11._Largest_param_updates'
        sys.stdout.write('%22s' % column_text)
    sys.stdout.write('\n')

    # Extract and print information for each iteration.
    for iter in energies:
        sys.stdout.write('     %9d' % iter)
        if len(energies) > 0:
            sys.stdout.write('   %19.12e' % energies[iter])
        if len(std_err) > 0:
            sys.stdout.write('   %19.12e' % std_err[iter])
        if len(target_fn) > 0:
            sys.stdout.write('   %19.12e' % target_fn[iter])
        if len(target_std_err) > 0:
            sys.stdout.write('   %19.12e' % target_std_err[iter])
        if len(std_dev) > 0:
            sys.stdout.write('   %19.12e' % std_dev[iter])
        if len(variances) > 0:
            sys.stdout.write('   %19.12e' % variances[iter])
        if len(uncertainties_of_variances) > 0:
            sys.stdout.write('   %19.12e' % uncertainties_of_variances[iter])
        if len(grad_norms) > 0:
            sys.stdout.write('   %19.12e' % grad_norms[iter])
        if len(param_update_sizes) > 0:
            sys.stdout.write('   %19.12e' % param_update_sizes[iter])
        if len(largest_param_updates) > 0:
            sys.stdout.write('   %19.12e' % largest_param_updates[iter])
        sys.stdout.write('\n')

    # I typically take averages over the last 10 linear method iterations for the values I report
    # as the result of optimization
    # The same idea is applicable to other descent methods
    # I also calculate the standard deviation to give a sense of error and to make error bars. 

    numIter1 = len(energies)
    # nonlocal maxIter
    # maxIter = numIter1      #TODO:Connie change this to actually be the max samples instead of number of iterations

    print("These values are averaged over the last 10 iterations to come to a final value")

    if len(energies) > 0:
        energies_list = list(energies.values())
        print("Energy")
        avg10E = np.mean(energies_list[numIter1-11:numIter1-1])
        stdev10E = np.std(energies_list[numIter1-11:numIter1-1])
        print(f"{avg10E} +/- {stdev10E}")
        energy_avg10_list.append(avg10E)
        energy_stdev10_list.append(stdev10E)

    if len(std_err) > 0:
        std_err_list = list(std_err.values())
        print("Energy Uncertainty")
        avg10std_err = np.mean(std_err_list[numIter1-11:numIter1-1])
        stdev10std_err = np.std(std_err_list[numIter1-11:numIter1-1])
        print(avg10std_err)
        std_err_avg10_list.append(avg10std_err)
        std_err_stdev10_list.append(stdev10std_err)

    if len(target_fn) > 0:
        target_fn_list = list(target_fn.values())
        print("Target Function")
        avg10target_fn = np.mean(target_fn_list[numIter1-11:numIter1-1])
        stdev10target_fn = np.std(target_fn_list[numIter1-11:numIter1-1])
        print(f"{avg10target_fn} +/- {stdev10target_fn}")
        target_fn_avg10_list.append(avg10target_fn)
        target_fn_stdev10_list.append(stdev10target_fn)

    if len(target_std_err) > 0:
        target_std_err_list = list(target_std_err.values())
        print("Target Function Uncertainty")
        avg10target_std_err = np.mean(target_std_err_list[numIter1-11:numIter1-1])
        stdev10target_std_err = np.std(target_std_err_list[numIter1-11:numIter1-1])
        print(avg10target_std_err)
        target_std_err_avg10_list.append(avg10target_std_err)
        target_std_err_stdev10_list.append(stdev10target_std_err)

    if len(std_dev) > 0:
        std_dev_list = list(std_dev.values())
        print("Standard Deviation")
        avg10std_dev = np.mean(std_dev_list[numIter1-11:numIter1-1])
        stdev10std_dev = np.std(std_dev_list[numIter1-11:numIter1-1])
        print(avg10std_dev)
        std_dev_avg10_list.append(avg10std_dev)
        std_dev_stdev10_list.append(stdev10std_dev)

    if len(variances) > 0:
        variances_list = list(variances.values())
        print("Variance")
        avg10variances = np.mean(variances_list[numIter1-11:numIter1-1])
        stdev10variances = np.std(variances_list[numIter1-11:numIter1-1])
        print(f"{avg10variances} +/- {stdev10variances}")
        variance_avg10_list.append(avg10variances)
        variance_stdev10_list.append(stdev10variances)

    if len(uncertainties_of_variances) > 0:
        uncertainties_of_variances_list = list(uncertainties_of_variances.values())
        print("Variance Uncertainty")
        avg10uncertainty_of_variances = np.mean(uncertainties_of_variances_list[numIter1-11:numIter1-1])
        stdev10uncertainty_of_variances = np.std(uncertainties_of_variances_list[numIter1-11:numIter1-1])
        print(avg10uncertainty_of_variances)
        uncertainties_of_variances_stdev10_list.append(stdev10uncertainty_of_variances)

    if len(grad_norms) > 0:
        grad_norms_list = list(grad_norms.values())
        print("Gradient Norm")
        avg10grad_norms = np.mean(grad_norms_list[numIter1-11:numIter1-1])
        stdev10grad_norms = np.std(grad_norms_list[numIter1-11:numIter1-1])
        print(f"{avg10grad_norms} +/- {stdev10grad_norms}")
        grad_norms_avg10_list.append(avg10grad_norms)
        grad_norms_stdev10_list.append(stdev10grad_norms)
    
    if len(param_update_sizes) > 0:
        param_update_sizes_list = list(param_update_sizes.values())
        print("Param Update Sizes")
        avg10param_update_sizes = np.mean(param_update_sizes_list[numIter1-11:numIter1-1])
        stdev10param_update_sizes = np.std(param_update_sizes_list[numIter1-11:numIter1-1])
        print(f"{avg10param_update_sizes} +/- {stdev10param_update_sizes}")
        param_update_sizes_avg10_list.append(avg10param_update_sizes)
        param_update_sizes_stdev10_list.append(stdev10param_update_sizes)
    
    if len(largest_param_updates) > 0:
        largest_param_updates_list = list(largest_param_updates.values())
        print("Largest Param Updates")
        avg10largest_param_updates = np.mean(largest_param_updates_list[numIter1-11:numIter1-1])
        stdev10largest_param_updates = np.std(largest_param_updates_list[numIter1-11:numIter1-1])
        print(f"{avg10largest_param_updates} +/- {stdev10largest_param_updates}")
        largest_param_updates_avg10_list.append(avg10largest_param_updates)
        largest_param_updates_stdev10_list.append(stdev10largest_param_updates)

# Save any data that is chosen to be plotted into data lists so that it can
# be plotted after all the files are processed. 
# Save the list of data points to plot, as well as the "avg10" value, which is the average
# of the last 10 data points. 
def collect_data_for_plots():
    # Check that enough plotting choices are given, and provide instructions if it is not
    if len(plotting_choices) < 10:
        print("Please specify 10 plotting choices in the input file. ")
        print("After the file name, put a data label for that file, then put a series of 1's and 0's with spaces between corresponding to whether you would like to plot each of the following things: ")
        print("1. Energy")
        print("2. Energy Standard Error")
        print("3. Target Function")
        print("4. Target Function Standard Error")
        print("5. Standard Deviation")
        print("6. Variance")
        print("7. Variance Uncertainty")
        print("8. Gradient Norm")
        print("9. Parameter Update Size")
        print("10. Largest Parameter Update")
        print("For example:")
        print("exampleFile.out myData1 1 0 1 0 0 0 0 0 0 0")
        print("This would include the data from exampleFile.out on the Energy plot and the Target Function plot, and label it myData1. ")

    # Collect the Energy data
    if int(plotting_choices[0]) == 1:
        energy_to_plot.append(copy.deepcopy(energies))
    else:
        energy_to_plot.append([])
    
    # Collect the Energy Uncertainty data
    if int(plotting_choices[1]) == 1:
        std_err_to_plot.append(copy.deepcopy(std_err))
    else:
        std_err_to_plot.append([])

    # Collect the Target Function data
    if int(plotting_choices[2]) == 1:
        target_fn_to_plot.append(copy.deepcopy(target_fn))
    else:
        target_fn_to_plot.append([])

    # Collet the Target Function Uncertainty data
    if int(plotting_choices[3]) == 1:
        target_std_err_to_plot.append(copy.deepcopy(target_std_err))
    else:
        target_std_err_to_plot.append([])

    # Collect the Standard Deviation data
    if int(plotting_choices[4]) == 1:
        std_dev_to_plot.append(copy.deepcopy(std_dev))
    else:
        std_dev_to_plot.append([])

    # Collect the Variance data
    if int(plotting_choices[5]) == 1:
        variance_to_plot.append(copy.deepcopy(variances))
    else:
        variance_to_plot.append([])

    # Collect the Variance Uncertainty data
    if int(plotting_choices[6]) == 1:
        uncertainties_of_variances_to_plot.append(copy.deepcopy(uncertainties_of_variances))
    else:
        uncertainties_of_variances_to_plot.append([])

    # Collect the Gradient Norm data
    if int(plotting_choices[7]) == 1:
        grad_norms_to_plot.append(copy.deepcopy(grad_norms))
    else:
        grad_norms_to_plot.append([])
    
    # Collect the Parameter Update Size data
    if int(plotting_choices[8]) == 1:
        param_update_sizes_to_plot.append(copy.deepcopy(param_update_sizes))
    else:
        param_update_sizes_to_plot.append([])

    # Collect the Gradient Norm data
    if int(plotting_choices[9]) == 1:
        largest_param_updates_to_plot.append(copy.deepcopy(largest_param_updates))
    else:
        largest_param_updates_to_plot.append([])

# Reset vectors to use them for the next file
def clean_vectors():
    energies.clear()
    uncertainties_of_variances.clear()
    variances.clear()
    std_err.clear()
    target_fn.clear()
    target_std_err.clear()
    std_dev.clear()
    grad_norms.clear()

# Put together the plot using matplotlib, and generate all the needed subplots
# for each quantity that has been scraped. 
def plot_data():
     # TODO:Connie Use the dict names for maximum generality?

    # set up plot
    fig = plt.figure()

    # Show the filenames that are used for this plot
    props = dict(boxstyle='square', facecolor='white')
    plt.gcf().text(0.1, 0.05, '\n'.join(qmc_files), bbox=props)
    # plt.text(.85, 0.95, '\n'.join(qmc_files), transform=plt.gcf().transFigure, horizontalalignment='left', verticalalignment='top', bbox=props)


    # Add ENERGY subplot
    #add_subplot_with_error_bars(fig, energy_to_plot, energy_avg10_list, energy_stdev10_list, std_err_to_plot, 'Energy', 'Energy (Ha)', 'Energy')
    add_subplot(fig, energy_to_plot, energy_avg10_list, energy_stdev10_list, 'Energy', 'Energy (Ha)', 'Energy')

    # Add STANDARD ERROR subplot
    add_subplot(fig, std_err_to_plot, std_err_avg10_list, std_err_stdev10_list, 'Standard Error', 'Std Err (Ha)', 'Std Err')

    # Add TARGET FUNCTION subplot
    add_subplot(fig, target_fn_to_plot, target_fn_avg10_list, target_fn_stdev10_list, 'Target Function', 'Target Fn Value', 'Targ Fn')

    # Add TARGET FUNCTION STANDARD ERROR subplot
    add_subplot(fig, target_std_err_to_plot, target_std_err_avg10_list, target_std_err_stdev10_list, 'Target Function Standard Error', 'Target Std Err', 'Targ Std Err')

    #TODO:Connie be more clear in the plot title what this is the std dev of. I think it's the energy?
    # Add STANDARD DEVIATION subplot
    add_subplot(fig, std_dev_to_plot, std_dev_avg10_list, std_dev_stdev10_list, 'Standard Deviation', 'Std Dev', 'Std Dev')

    # Add VARIANCE subplot
    add_subplot(fig, variance_to_plot, variance_avg10_list, variance_stdev10_list, 'Variance', 'Variance', 'Var')

    #TODO:Connie change this to stay std dev or std err instead of "uncertainty"
    # Add TARGET FUNCTION STANDARD ERROR subplot
    add_subplot(fig, uncertainties_of_variances_to_plot, uncertainties_of_variances_avg10_list, uncertainties_of_variances_stdev10_list, 'Variance Uncertainty', 'Var Uncertainty', 'Var Unc')

    #TODO:Connie make it clear what this is the gradient norm of! I think it's the energy?
    # Add GRADIENT NORM subplot
    add_subplot(fig, grad_norms_to_plot, grad_norms_avg10_list, grad_norms_stdev10_list, 'Gradient Norm', 'Grad Norm', 'Grad Norm')

    # Add PARAM UPDATE SIZE subplot
    add_subplot(fig, param_update_sizes_to_plot, param_update_sizes_avg10_list, param_update_sizes_stdev10_list, 'Param Update Size', 'Param Update Size', 'Param Update Size')

    # Add LARGEST PARAM UPDATE subplot
    add_subplot(fig, largest_param_updates_to_plot, largest_param_updates_avg10_list, largest_param_updates_stdev10_list, 'Largest Param Update', 'Largest Param Update', 'Largest Param Update')

    # Show only "outer" axis labels
    for ax in fig.get_axes():
        ax.label_outer()
    
    # Plot all subplots!
    plt.show()

# TODO:Connie change the x axis to number of samples instead?
# Adds a subplot to the matplotlib figure provided. 
# Plots the values listed in values_to_plot (which is a list of lists of data, some of which may be empty)
# Draws a box to display the values from values_avg10_list
# Places the plot title given from plot_title
# Places the y axis label given from yaxis_label
# Labels the data in a legend using the results_label provided
def add_subplot(fig, values_to_plot, values_avg10_list, values_stdev10_list, plot_title, yaxis_label, results_label):
    added_subplot = False
    results_lines = [] # temporary string to hold the finalized values to be displayed on each plot

    # Add the given data to the subplot
    for i in range(len(values_to_plot)):
        data_list = values_to_plot[i]
        if len(data_list) > 0:
            if added_subplot == False:
                # make sure this only gets run once for subplot setup
                added_subplot = True
                # alter subplot geometry
                n = len(fig.axes)
                for j in range(n):
                    fig.axes[j].change_geometry(n+1, 1, j+1)
                # create subplot
                ax = fig.add_subplot(n+1, 1, n+1)
            # Add data to subplot
            ax.plot(range(1, len(data_list)+1), list(data_list.values()), marker='o', color=color_list[i % len(color_list)],label='%s: %s' % (results_label, data_labels[i]))
            results_lines.append('Avg10 %s: $%.5f$ +/- $%.5f$  %s' % (results_label, values_avg10_list[i], values_stdev10_list[i], data_labels[i]))

    if added_subplot == True:
        # White background for the plot
        props = dict(boxstyle='square', facecolor='white')

        # Axes and title settings
        ax.set_title(plot_title)
        ax.set_xlabel('Iteration Number', horizontalalignment='right')
        ax.set_ylabel(yaxis_label)
        # ax.set_ylim(linE-.01,linE+.01)   # Often helpful to zoom in on converged part of optimization
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

        # Add vertical grid lines
        ax = plt.gca()
        ax.grid(which='major', axis='x', linestyle='--')
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.grid(which='minor', axis='x', linestyle=':')

        # Place the legend
        ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))

        # Make a text box for the results string, showing the average of the last 10 energies
        results_str = '\n'.join(results_lines)
        ax.text(.1, .95, results_str, transform=ax.transAxes, horizontalalignment='left', verticalalignment='top', bbox=props)
        
        # Adjust the position and size of the subplot
        box = ax.get_position()
        ax.set_position([box.x0, box.y0+box.height*.15, box.width, box.height*.85])

# TODO:Connie change the x axis to number of samples instead?
# Adds a subplot to the matplotlib figure provided. 
# Plots the values listed in values_to_plot (which is a list of lists of data, some of which may be empty)
# Draws a box to display the values from values_avg10_list
# Places the plot title given from plot_title
# Places the y axis label given from yaxis_label
# Labels the data in a legend using the results_label provided
def add_subplot_with_error_bars(fig, values_to_plot, values_avg10_list, values_stdev10_list, errors_to_plot, plot_title, yaxis_label, results_label):
    added_subplot = False
    results_lines = [] # temporary string to hold the finalized values to be displayed on each plot

    # Add the given data to the subplot
    for i in range(len(values_to_plot)):
        data_list = list(values_to_plot[i].values())
        #error_list = list(errors_to_plot[i].values())
        error_list = errors_to_plot[i]
        error_list[-1] = values_stdev10_list[i]
        if len(data_list) > 0:
            if added_subplot == False:
                # make sure this only gets run once for subplot setup
                added_subplot = True
                # alter subplot geometry
                n = len(fig.axes)
                for j in range(n):
                    fig.axes[j].change_geometry(n+1, 1, j+1)
                # create subplot
                ax = fig.add_subplot(n+1, 1, n+1)
            # Add data to subplot
            ax.errorbar(range(1, len(data_list)+1), data_list, yerr=error_list, marker='o', color=color_list[i % len(color_list)],label='%s: %s' % (results_label, data_labels[i]))
            results_lines.append('Avg10 %s: $%.5f$ +/- $%.5f$  %s' % (results_label, values_avg10_list[i], values_stdev10_list[i], data_labels[i]))
    results_lines.append('Error stated is stdev10, plotted is stderr except final which is stdev10')

    if added_subplot == True:
        # White background for the plot
        props = dict(boxstyle='square', facecolor='white')

        # Axes and title settings
        ax.set_title(plot_title)
        ax.set_xlabel('Iteration Number', horizontalalignment='right')
        ax.set_ylabel(yaxis_label)
        # ax.set_ylim(linE-.01,linE+.01)   # Often helpful to zoom in on converged part of optimization
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

        # Add vertical grid lines
        ax = plt.gca()
        ax.grid(which='major', axis='x', linestyle='--')
        ax.xaxis.set_minor_locator(MultipleLocator(10))
        ax.grid(which='minor', axis='x', linestyle=':')

        # Place the legend
        ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))

        # Make a text box for the results string, showing the average of the last 10 energies
        results_str = '\n'.join(results_lines)
        ax.text(.1, .95, results_str, transform=ax.transAxes, horizontalalignment='left', verticalalignment='top', bbox=props)
        
        # Adjust the position and size of the subplot
        box = ax.get_position()
        ax.set_position([box.x0, box.y0+box.height*.15, box.width, box.height*.85])

if __name__ == '__main__':
    (options, input_files) = parse_options(sys.argv[1:])
    read_input_file(input_files[0])
    #energies, uncertainties_of_variances, variances, std_err, target_fn, target_std_err, std_dev, grad_norms = extract_data(data_files)
    for i in range(len(qmc_files)):
        qmc_file = str(qmc_files[i])
        extract_data(qmc_file)
        check_data()
        print_data()
        collect_data_for_plots()
        clean_vectors()
    plot_data()
