from asyncio import format_helpers
from json.tool import main
import os, sys
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import statistics
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# all_1b1_files = os.listdir('1b1')
# gvp_1b1_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run003' in all_1b1_files[i]])
# gvp_1b1_split_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run002' in all_1b1_files[i]])
# gvp_1b1_splitabs_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvpabs_run001' in all_1b1_files[i]])

all_h2ogs_files = os.listdir('h2ogs')
edesc_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_edescci_run001' in all_h2ogs_files[i]])
edesc_h2ogs_sub_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_edesccisub_run001' in all_h2ogs_files[i]])
gvp_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpttci_run001' in all_h2ogs_files[i]])
gvp_h2ogs_sub_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpttcisub_run001' in all_h2ogs_files[i]])
gvp_h2ogs_split_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpsplitci_run001' in all_h2ogs_files[i]])
gvp_h2ogs_split_sub_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpsplitcisub_run001' in all_h2ogs_files[i]])
gvp_h2ogs_splitabs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpabsci_run001' in all_h2ogs_files[i]])
gvp_h2ogs_splitabs_sub_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpabscisub_run001' in all_h2ogs_files[i]])
lm_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_lmcombci_run001' in all_h2ogs_files[i]])
te_h2ogs_sub_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_tecombci_run001' in all_h2ogs_files[i]])

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

name_list = ["E desc", "E desc with substeps", "GVP", "GVP with substeps", "GVP split", "GVP split with substeps", "GVP split abs", "GVP split abs with substeps", "LM", "targetExcited"]
color_list = ["red", "blue", "green", "black", "purple", "orange", "cyan", "pink", "yellow", "gray"]

# Go through the file to extract all the data:
# energies, variances, uncertainty of variances, standard err, 
# target function, target function standard error, standard deviation,
# gradient norms, parameter update sizes, largest parameter update sizes
def extract_data(qmc_file, target_state_used=False):
    # Arrays to hold the resulting data
    energies = []
    variances = []
    uncertainties_of_variances = []
    standard_deviations = []
    standard_errors = []
    target_functions = []
    target_fn_standard_errors = []
    grad_norms = []
    this_iter_lderivs = []
    all_iters_lderivs = []
    param_update_sizes = []
    largest_param_updates = []
    qmc_timing = None
    total_timing = None

    # Variables to track where we are in the file
    collecting_lderivs = False
    stat_err_counter = 0

    # Need to identify based on the file whether it's using LM or just descent methods
    LinearMethodUsed = False
    DescentMethodUsed = False

    # Try to identify based on the file which type of variational principle is being optimized
    TargetExcitedUsed = target_state_used
    TargetExcitedClosestUsed = False
    TargetGVPUsed = False
    TargetGroundUsed = False

    # Set up variables for looping through each line of the file
    have_data = False
    iteration = 0
    f = open(qmc_file)
    for line in f:
        # IDENTIFY METHOD
        # Check if the identifier line for either is here, to identify which method this file uses
        if not (LinearMethodUsed or DescentMethodUsed):
            if LM_str_dict['method_identifier'] in line:
                LinearMethodUsed = True
                str_dict = LM_str_dict
                #print("The following values are reported from the Linear Method")
            elif descent_str_dict['method_identifier'] in line:
                DescentMethodUsed = True
                str_dict = descent_str_dict
                #print("The following values are reported from a descent method")
            else:
                continue
        # Check if the target identifier line is used, to identify which variational principle is targeted
        if not (TargetExcitedUsed or TargetExcitedClosestUsed or TargetGVPUsed or TargetGroundUsed):
            if target_dict['excited'] in line:
                TargetExcitedUsed = True
                #print("Target Excited used")
            elif target_dict['excited_closest'] in line:
                TargetExcitedClosestUsed = True
                #print("Target Excited Closest used")
            elif target_dict['gvp'] in line:
                TargetGVPUsed = True
                #print("GVP used")
            elif target_dict['ground'] in line:
                TargetGroundUsed = True
                #print("Target Ground State used")

        # COLLECT DATA EXCEPT LDERIVS
        if str_dict['data_start'] in line:
            have_data = True
        if have_data:
            if str_dict['energy'] in line:
                energies.append(float(line.split()[-1]))
            elif str_dict['uncertainty_of_variance'] in line:
                uncertainties_of_variances.append(float(line.split()[-1]))
            elif str_dict['variance'] in line:
                variances.append(float(line.split()[-1]))
            elif str_dict['target'] in line:
                values = line.split()
                if 'N/A' in values[3]:
                    target_functions.append(0.0)
                elif 'Average' not in values[3]:    # TEMPORARY FIX
                    target_functions.append(float(line.split()[-1]))
            elif str_dict['target_err'] in line:
                target_fn_standard_errors.append(float(line.split()[-1]))
            elif str_dict['std_err'] in line:       # MUST put this after target err because this string may be a subset of that string
                if LinearMethodUsed and (TargetExcitedUsed or TargetExcitedClosestUsed):
                    if stat_err_counter % 3 == 0:   # The target fn error is caught before this so there are only 3 instances per iteration left
                        standard_errors.append(float(line.split()[-1]))
                    stat_err_counter += 1
                else:
                    standard_errors.append(float(line.split()[-1]))
            elif str_dict['std_dev'] in line:
                standard_deviations.append(float(line.split()[-1]))
            elif str_dict['grad_norm'] in line:
                grad_norms.append(float(line.split()[-1]))
            elif str_dict['param_update_size'] in line:
                param_update_sizes.append(float(line.split()[-1]))
            elif str_dict['largest_param_update'] in line:
                largest_param_updates.append(float(line.split()[-1]))
            elif str_dict['data_end'] in line:
                # TODO:Connie modify this so that instead of "iteration" it's "number of samples"
                # so that LM results and regular descent results are easier to compare
                have_data = False
                iteration += 1
        if str_dict['data_start'] in line:
            have_data = True
        # Collect timing value if present
        elif "QMC Execution time" in line:
            qmc_timing = float(line.split()[-2])
        elif "Total Execution time" in line:
            total_timing = float(line.split()[-2])
        # COLLECT LDERIVS
        # Stop collecting lderivs if we hit the end of the lderivs section
        if "</lderivs>" in line:
            collecting_lderivs = False
            all_iters_lderivs.append(this_iter_lderivs)
            this_iter_lderivs = []
        # Collect lderivs if currently collecting them
        elif collecting_lderivs:
            this_iter_lderivs.append(float(line))
        # Start collecting lderivs if we find the line
        elif "<lderivs>" in line:
            collecting_lderivs = True

    f.close()
    return (energies, variances, uncertainties_of_variances, standard_deviations, standard_errors, target_functions, target_fn_standard_errors, grad_norms, all_iters_lderivs, param_update_sizes, largest_param_updates, qmc_timing, total_timing)

# This function is WRONG and should not be used. Use extract_data() instead
def process_file(filename):
    # Arrays to hold the resulting data
    energies = []
    variances = []
    target_functions = []
    this_iter_lderivs = []
    all_iters_lderivs = []
    qmc_timing = None
    total_timing = None

    # Variables to track where we are in the file
    collecting_lderivs = False

    # Open the file
    f=open(filename, 'r')
    for line in f:
        # Stop collecting lderivs if we hit the end of the lderivs section
        if "</lderivs>" in line:
            collecting_lderivs = False
            all_iters_lderivs.append(this_iter_lderivs)
            this_iter_lderivs = []
        # Collect lderivs if currently collecting them
        elif collecting_lderivs:
            this_iter_lderivs.append(float(line))
        # Start collecting lderivs if we find the line
        elif "<lderivs>" in line:
            collecting_lderivs = True
        # Collect energy value if present
        elif "VMC Eavg" in line:
            energies.append(float(line.split()[-1]))
        # Collect variance if present
        elif "VMC Evar" in line:
            variances.append(float(line.split()[-1]))
        # Collect target function if present
        elif "Target Function Average:" in line:
            target_functions.append(float(line.split()[-1]))
        # Collect timing value if present
        elif "QMC Execution time" in line:
            qmc_timing = float(line.split()[-2])
        elif "Total Execution time" in line:
            total_timing = float(line.split()[-2])
    f.close()
    return (energies, variances, target_functions, all_iters_lderivs, qmc_timing, total_timing)

def read_files(file_names, all_energies, all_variances, all_uncert_of_varriances, all_stdevs, all_stderrs, all_target_functions, all_target_fn_stderrs, all_grad_norms, all_lderivs, all_param_update_sizes, all_largest_param_updates, all_qmc_timings, all_total_timings, target_state_used=None, max_files=None):
    current_energies = []
    current_variances = []
    current_uncert_of_variances = []
    current_stdevs = []
    current_stderrs = []
    current_target_functions = []
    current_target_fn_stderrs = []
    current_grad_norms = []
    current_lderivs = []
    current_param_update_sizes = []
    current_largest_param_updates = []
    current_qmc_timing = []
    current_total_timing = []

    for (i, file) in enumerate(file_names):
        if max_files and i > max_files:
            continue
        print("Reading in %s" % (file))
        if target_state_used is not None:
            (energies, variances, uncertainties_of_variances, standard_deviations, \
            standard_errors, target_functions, target_fn_standard_errors, grad_norms, \
            lderivs, param_update_sizes, largest_param_updates, qmc_timing, \
            total_timing) = extract_data(file, target_state_used=target_state_used)
        else:
            (energies, variances, uncertainties_of_variances, standard_deviations, \
            standard_errors, target_functions, target_fn_standard_errors, grad_norms, \
            lderivs, param_update_sizes, largest_param_updates, qmc_timing, \
            total_timing) = extract_data(file)
        #(energies, variances, target_functions, lderivs, qmc_timing, total_timing) = process_file(file)
        current_energies.append(energies)
        current_variances.append(variances)
        current_uncert_of_variances.append(uncertainties_of_variances)
        current_stdevs.append(standard_deviations)
        current_stderrs.append(standard_errors)
        current_target_functions.append(target_functions)
        current_target_fn_stderrs.append(target_fn_standard_errors)
        current_grad_norms.append(grad_norms)
        current_lderivs.append(lderivs)
        current_param_update_sizes.append(param_update_sizes)
        current_largest_param_updates.append(largest_param_updates)
        current_qmc_timing.append(qmc_timing)
        current_total_timing.append(total_timing)
    all_energies.append(current_energies)
    all_variances.append(current_variances)
    all_uncert_of_varriances.append(current_uncert_of_variances)
    all_stdevs.append(current_stdevs)
    all_stderrs.append(current_stderrs)
    all_target_functions.append(current_target_functions)
    all_target_fn_stderrs.append(current_target_fn_stderrs)
    all_grad_norms.append(current_grad_norms)
    all_lderivs.append(current_lderivs)
    all_param_update_sizes.append(current_param_update_sizes)
    all_largest_param_updates.append(current_largest_param_updates)
    all_qmc_timings.append(current_qmc_timing)
    all_total_timings.append(current_total_timing)

# Shrink data through averaging buckets of size n_ci
def shrink_data(all_data, n_ci):
    all_shrunk_data = []
    all_shrunk_errs = []
    for this_run_data in all_data:
        this_file_shrunk_data = []
        this_file_shrunk_err = []
        for dataset in this_run_data:
            if len(dataset) % n_ci != 0:
                print(f'data of length {len(dataset)} is not divisible by {n_ci}')
                return all_data
            shrunk_data = [sum(dataset[ n_ci*i : n_ci*(i+1) ]) / n_ci for i in range(int(len(dataset)/n_ci))]
            shrunk_err = [np.std(dataset[ n_ci*i : n_ci*(i+1) ]) / np.sqrt(n_ci) for i in range(int(len(dataset)/n_ci))]
            this_file_shrunk_data.append(shrunk_data)
            this_file_shrunk_err.append(shrunk_err)
        all_shrunk_data.append(this_file_shrunk_data)
        all_shrunk_errs.append(this_file_shrunk_err)
    return (all_shrunk_data, all_shrunk_errs)

# Plot one set of energy data
def plot_subplot_data(vector_data, data_label, data_color, ax=None, errbars=None, subplot_title=None, avgN=0, marker_style=None):
    current_x = 0
    first = True
    if marker_style == None:
        marker_style = 'o'
    for (i, data) in enumerate(vector_data):
        x = np.arange(current_x, current_x + 0.5, 0.5 / len(data))
        current_x = current_x + 0.5
        if errbars is not None:
            cur_errbars = errbars[i]
            # Old way to do the x axis, each tick is a data point:
            #x = np.arange(current_x, current_x + len(data))
            #current_x = current_x + len(data)
            # New way to do the x axis, each tick is a half-macroiteration:
            if first:
                ax.errorbar(x, data, yerr=cur_errbars, marker=marker_style, label=data_label, color=data_color)
                first = False
            else:
                ax.errorbar(x, data, yerr=cur_errbars, marker=marker_style, color=data_color)
        else:
            if first:
                ax.errorbar(x, data, marker=marker_style, label=data_label, color=data_color)
                first = False
            else:
                ax.errorbar(x, data, marker=marker_style, color=data_color)
        ax.set_title(subplot_title)

    # Plot a line showing the final result, if desired
    if avgN > 0:
        final_result = np.average(vector_data[-1][-avgN:])
        ax.axhline(xmin=0, xmax=current_x, y=final_result, color=data_color, linestyle='-')
        # x_range = np.array([0, current_x])
        # ax.fill_between(x_range, final_result-errbars[-1][-1], final_result+errbars[-1][-1], color=data_color, alpha=0.1)
    # Axis formatting for energy plots only
    # flat_ax_list[j].yaxis.set_major_formatter('{x:.3f}')             # Use mHa units
    # flat_ax_list[j].yaxis.set_major_locator(MultipleLocator(0.001))
    # If it's using an offset do this
    #ax.yaxis.get_major_formatter().set_useOffset(False)
    # Macroiteration formatting
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))    # default is no labels on the minor ticks

# Plot energies
def plot_energies(all_energies, errbars=None, avgN=0, fig_title=None):
    plt.figure("Energies")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, energies in enumerate(all_energies):
        plot_subplot_data(energies, name_list[i], color_list[i], ax=ax, errbars=errbars[i], avgN=avgN, subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Energy (Ha)")
    plt.subplots_adjust(wspace=0.3, hspace=0.35)

# Plot error bars
def plot_errbars(all_errbars, avgN=0, fig_title=None, marker_style=None):
    plt.figure("Error Bars")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, errbars in enumerate(all_errbars):
        plot_subplot_data(errbars, name_list[i], color_list[i], marker_style=marker_style, ax=ax, avgN=avgN, subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Energy Error Bars (Ha)")
    plt.subplots_adjust(wspace=0.3, hspace=0.35)

# Plot target function
def plot_target_functions(all_target_functions, errbars=None, avgN=0, fig_title=None):
    plt.figure("Target Functions")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, target_function in enumerate(all_target_functions):
        plot_subplot_data(target_function, name_list[i], color_list[i], ax=ax, avgN=avgN, errbars=errbars[i], subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Target Function")

# Plot subplots
def multiplot(multi_all_data, num_rows, num_cols, multi_errbars=None, fig_title=None, subplot_titles=None, ylabel=None, xlabel=None, avgN=0):
    fig, (ax_list) = plt.subplots(nrows=num_rows, ncols=num_cols, sharex=False)
    flat_ax_list = ax_list.flatten()
    num_blank_grids = len(flat_ax_list) - len(multi_all_data)
    for j, all_data in enumerate(multi_all_data):
        errbars = multi_errbars[j]
        fig.suptitle(fig_title)
        # plt.figure(fig_title)
        for i, data in enumerate(all_data):
            if j == 0:
                plot_subplot_data(data, name_list[i], color_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
            else:
                plot_subplot_data(data, None, color_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
            # flat_ax_list[j].yaxis.set_major_formatter('{x:.3f}')             # Use mHa units
            # flat_ax_list[j].yaxis.set_major_locator(MultipleLocator(0.001))
        # Only label the "outer" y axes
        if j % num_cols == 0:
            flat_ax_list[j].set(ylabel=ylabel)
        flat_ax_list[j].set(xlabel=xlabel)
        # flat_ax_list[j].label_outer()
    for k in range(num_blank_grids):
        flat_ax_list[-1*k - 1].axis('off')
    plt.subplots_adjust(wspace=0.3, hspace=0.35)
    #fig.legend(loc='lower right', bbox_to_anchor=(.95, 1.0))
    fig.legend(loc='lower right')
    fig.set_size_inches(10,6,forward=True)

# Plot a whole bunch of average 10 energies over macro iterations
def multiplot_avgN(multi_all_files, multi_all_energies, num_rows, num_cols, subplot_titles, N1=10, N2=10):
    fig, (ax_list) = plt.subplots(nrows=num_rows, ncols=num_cols, sharex=False)
    flat_ax_list = ax_list.flatten()
    num_blank_grids = len(flat_ax_list) - len(multi_all_files)
    for j, all_files in enumerate(multi_all_files):
        plot_avgN(all_files, multi_all_energies[j], N1=N1, N2=N2, ax=flat_ax_list[j], title=subplot_titles[j])
        # Only label the "outer" y axes
        if j % num_cols != 0:
            flat_ax_list[j].set(ylabel=None)
        # flat_ax_list[j].label_outer()
    for k in range(num_blank_grids):
        flat_ax_list[-1*k - 1].axis('off')
    plt.subplots_adjust(wspace=0.3, hspace=0.35)
    #fig.legend(loc='lower right', bbox_to_anchor=(.95, 1.0))
    fig.legend(loc='lower right')
    fig.set_size_inches(10,6,forward=True)

# Plot average 10 energies over macro iterations
# N1 is the factor to shrink the CI iterations, N2 is the factor to shrink the Jastrow iterations
def plot_avgN(all_files, all_energies, N1=10, N2=10, ax=None, title=None):
    need_legend = False
    if ax == None:
        ax = plt.gca()
        need_legend = True
    markers_list = ['o', 'X', 's', 'p', '*', 'D', 'v', '1', 'P', '6']
    ax.set_title(title)
    #plt.figure("Energies, avg10")
    # compiled_file_list = []
    avg_N_list = []
    err_N_list = []
    for i, files_list in enumerate(all_files):
        avg_N_list = []
        err_N_list = []
        for j, file in enumerate(files_list):
            if j%2 == 0:
                avg_N = np.average(all_energies[i][j][-N1:])
                err_N = np.std(all_energies[i][j][-N1:]) / np.sqrt(N1)
            else:
                avg_N = np.average(all_energies[i][j][-N2:])
                err_N = np.std(all_energies[i][j][-N2:]) / np.sqrt(N2)
            avg_N_list.append(avg_N)
            err_N_list.append(err_N)
            # compiled_file_list.append(file)
            #plt.plot([j], avg_10, marker=markers_list[i], label=file, color=color_list[i])
            if j == 0:
                ax.errorbar([(j+1)/2], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i], label=name_list[i], color=color_list[i]),
            else:
                ax.errorbar([(j+1)/2], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i], color=color_list[i])
            print(f"{file}: {avg_N} +/- {err_N}")
        # use this code to only connect the lines for every other point
        every_second_x_list = [(j+1)/2 for j in range(len(files_list)) if j%2 == 1]
        every_second_avg_N_list = [avg_N_list[i] for i in range(len(avg_N_list)) if i%2 == 1]
        ax.plot(every_second_x_list, every_second_avg_N_list, color=color_list[i])
        # use this code to connect the lines for all points
        # plt.plot(range(len(files_list)), avg_N_list, color=color_list[i])
    ax.set(xlabel="Macroiteration", ylabel="Energy (Ha)")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    # plt.ylabel("Energy (Ha)")
    if need_legend:
        plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
        plt.subplots_adjust(wspace=0.3, hspace=0.35)

# Determine the best method(s) by averaging over a varying number of points to see which has the lowest number
# and has the most consistent / converged result
def rank_final_results(all_energies):
    x_list = np.arange(0,1000,10)
    plt.figure("Final Results")
    for i, energies in enumerate(all_energies):
        data = energies[-1]
        x_list = np.arange(0,len(data),10)
        y_list = []
        err_list = []
        for x in x_list:
            cur_val = np.average(data[-x:])
            y_list.append(cur_val)
            cur_err = np.std(data[-x:])
            if np.abs(cur_err) > 0.0000:
                err_list.append(0)
            else:
                err_list.append(cur_err)
        plt.errorbar(x_list, y_list, yerr=err_list, label=name_list[i], color=color_list[i])
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.xlabel("Number of Final Steps Averaged Over")
    plt.ylabel("Energy (Ha)")
    plt.gca().yaxis.set_major_formatter('{x:.4f}')             # Use mHa units

def rank_final_results_vs_time(all_energies, all_times):
    x_list = np.arange(0,1000,10)
    plt.figure("Final Results vs. Time")
    for i, energies in enumerate(all_energies):
        data = energies[-1]
        time_data = all_times[i]
        plain_x_list = np.arange(0,len(data),10)
        x_list = np.arange(0,len(data),10) * (time_data[0] / len(data))
        y_list = []
        err_list = []
        for x in plain_x_list:
            cur_val = np.average(data[-x:])
            y_list.append(cur_val)
            cur_err = np.std(data[-x:])
            if np.abs(cur_err) > 0.0000:
                err_list.append(0)
            else:
                err_list.append(cur_err)
        plt.errorbar(x_list, y_list, yerr=err_list, label=name_list[i], color=color_list[i])
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.xlabel("Total Execution Time (s)")
    plt.ylabel("Energy (Ha)")
    plt.gca().yaxis.set_major_formatter('{x:.4f}')             # Use mHa units

def main():
    # Arrays to hold the resulting data
    h2ogs_energies = []
    h2ogs_variances = []
    h2ogs_uncertainties_of_variances = []
    h2ogs_standard_deviations = []
    h2ogs_standard_errors = []
    h2ogs_target_functions = []
    h2ogs_target_fn_standard_errors = []
    h2ogs_grad_norms = []
    h2ogs_all_iters_lderivs = []
    h2ogs_param_update_sizes = []
    h2ogs_largest_param_updates = []
    h2ogs_qmc_timing = []
    h2ogs_total_timing = []

    h2o1b1_energies = []
    h2o1b1_variances = []
    h2o1b1_uncertainties_of_variances = []
    h2o1b1_standard_deviations = []
    h2o1b1_standard_errors = []
    h2o1b1_target_functions = []
    h2o1b1_target_fn_standard_errors = []
    h2o1b1_grad_norms = []
    h2o1b1_all_iters_lderivs = []
    h2o1b1_param_update_sizes = []
    h2o1b1_largest_param_updates = []
    h2o1b1_qmc_timing = []
    h2o1b1_total_timing = []

    # Variables to tweak the plotting
    energy_shrink_amount = 10
    errbar_shrink_amount = 10
    targetfn_shrink_amount = 100
    variance_shrink_amount = 100
    max_files = None

    ##########
    # H2O GS #
    ##########
    # Read the files
    h2ogs_files = [edesc_h2ogs_filenames, 
                   edesc_h2ogs_sub_filenames,
                   gvp_h2ogs_filenames, 
                   gvp_h2ogs_sub_filenames,
                   gvp_h2ogs_split_filenames, 
                   gvp_h2ogs_split_sub_filenames, 
                   gvp_h2ogs_splitabs_filenames,
                   gvp_h2ogs_splitabs_sub_filenames,
                   lm_h2ogs_filenames,
                   te_h2ogs_sub_filenames]
    target_state_used_list = [False, False, False, False, False, False, False, False, False, True]
    for (i, state_files) in enumerate(h2ogs_files):
        read_files(state_files, h2ogs_energies, h2ogs_variances, h2ogs_uncertainties_of_variances, h2ogs_standard_deviations, h2ogs_standard_errors, h2ogs_target_functions, h2ogs_target_fn_standard_errors, h2ogs_grad_norms, h2ogs_all_iters_lderivs, h2ogs_param_update_sizes, h2ogs_largest_param_updates, h2ogs_qmc_timing, h2ogs_total_timing, target_state_used=target_state_used_list[i], max_files=max_files)

    # plot_avgN(h2ogs_files, h2ogs_energies, N1=100, N2=10)
    # plot_energies(h2ogs_energies, errbars=h2ogs_standard_errors, avgN=100, fig_title='H2O Ground State')
    rank_final_results(h2ogs_energies)
    rank_final_results_vs_time(h2ogs_energies, h2ogs_total_timing)
    # plot_energies(h2ogs_energies[0:8], errbars=h2ogs_standard_errors[0:8], avgN=100, fig_title='H2O Ground State Descent Methods')
    # plot_errbars(h2ogs_standard_errors, avgN=10, fig_title='H2O Ground State')
    # plot_target_functions(h2ogs_target_functions, errbars=h2ogs_target_fn_standard_errors, fig_title='H2O Ground State')
    plt.show()

    # # Shrink the data size through averaging so it's easier to read
    (shrunk_h2ogs_energies, shrunk_h2ogs_err) = shrink_data(h2ogs_energies, energy_shrink_amount)
    (shrunk_h2ogs_standard_errors, shrunk_h2ogs_errbars_err) = shrink_data(h2ogs_standard_errors, errbar_shrink_amount)
    # (shrunk_h2ogs_targetfn, shrunk_h2ogs_target_err) = shrink_data(h2ogs_target_functions, targetfn_shrink_amount)
    # (shrunk_h2ogs_variance, shrunk_h2ogs_variance_err) = shrink_data(h2ogs_variances, variance_shrink_amount)
    
    # # Plot the shrunk data
    # plot_avgN(h2ogs_files, h2ogs_energies, N1=100, N2=10)
    # plot_energies(shrunk_h2ogs_energies, errbars=shrunk_h2ogs_err, avgN=1, fig_title='H2O Ground State')
    plot_energies(shrunk_h2ogs_energies[0:8], errbars=shrunk_h2ogs_err[0:8], avgN=1, fig_title='H2O Ground State Descent Methods')
    plot_errbars(shrunk_h2ogs_standard_errors, avgN=10, fig_title='H2O Ground State QMC Error Bars')
    plot_errbars(shrunk_h2ogs_err, avgN=10, fig_title='H2O Ground State Calculated Error Bars', marker_style='P')
    # plot_target_functions(shrunk_h2ogs_targetfn, errbars=shrunk_h2ogs_target_err, fig_title='H2O Ground State')
    plt.show()

    # ###########
    # # H2O 1B1 #
    # ###########
    # # Read the files to get data
    # h2o1b1_files = [gvp_1b1_filenames, gvp_1b1_split_filenames, gvp_1b1_splitabs_filenames]
    # for state_files in h2o1b1_files:
    #     read_files(state_files, h2o1b1_energies, h2o1b1_variances, h2o1b1_uncertainties_of_variances, h2o1b1_standard_deviations, h2o1b1_standard_errors, h2o1b1_target_functions, h2o1b1_target_fn_standard_errors, h2o1b1_grad_norms, h2o1b1_all_iters_lderivs, h2o1b1_param_update_sizes, h2o1b1_largest_param_updates, h2o1b1_qmc_timing, h2o1b1_total_timing)
    
    # # Shrink the data size through averaging so it's easier to read
    # (shrunk_h2o1b1_energies, shrunk_h2o1b1_err) = shrink_data(h2o1b1_energies, energy_shrink_amount, energyj_shrink_amount)
    # (shrunk_h2o1b1_targetfn, shrunk_h2o1b1_target_err) = shrink_data(h2o1b1_target_functions, targetfn_shrink_amount, targetfnj_shrink_amount)
    # (shrunk_h2o1b1_variance, shrunk_h2o1b1_variance_err) = shrink_data(h2o1b1_variances, variance_shrink_amount, variancej_shrink_amount)

    # # Plot the data
    # plot_avgN(h2o1b1_files, h2o1b1_energies, N1=100, N2=10)
    # plot_energies(shrunk_h2o1b1_energies, errbars=shrunk_h2o1b1_err, fig_title='H2O 1B1 State')
    # plot_target_functions(shrunk_h2o1b1_targetfn, errbars=shrunk_h2o1b1_target_err, fig_title='H2O 1B1 State')
    # plt.show()

    # #############
    # # MULTIPLOT #
    # #############

    # subplot_titles = ['Formaldehyde Ground State', 'Formaldehyde N to Pi* State', 'Formaldehyde Pi to Pi* State', 'H2O Ground State', 'H2O 1B1 State']

    # # Energies
    # multi_all_energies = [shrunk_formgs_energies, shrunk_formn2p_energies, shrunk_formp2p_energies, shrunk_h2ogs_energies, shrunk_h2o1b1_energies]
    # multi_all_energy_errs = [shrunk_formgs_err, shrunk_formn2p_err, shrunk_formp2p_err, shrunk_h2ogs_err, shrunk_h2o1b1_err]
    # multiplot(multi_all_energies, 2, 3, avgN=1, multi_errbars=multi_all_energy_errs, fig_title="Energies", subplot_titles=['Formaldehyde Ground State', 'Formaldehyde N to Pi* State', 'Formaldehyde Pi to Pi* State', 'H2O Ground State', 'H2O 1B1 State'], ylabel="Energy (Ha)", xlabel="Macroiterations")
    # # plt.show()

    # # AvgN's
    # multi_all_energies = [formgs_energies, formn2p_energies, formp2p_energies, h2ogs_energies, h2o1b1_energies]
    # multi_all_files = [formgs_files, formn2pistar_files, formp2pistar_files, h2ogs_files, h2o1b1_files]
    # multiplot_avgN(multi_all_files, multi_all_energies, 2, 3, subplot_titles, N1=100, N2=10)

    # # Target Functions
    # multi_all_targetfn = [shrunk_formgs_targetfn, shrunk_formn2p_targetfn, shrunk_formp2p_targetfn, shrunk_h2ogs_targetfn, shrunk_h2o1b1_targetfn]
    # multi_all_targetfn_errs = [shrunk_formgs_target_err, shrunk_formn2p_target_err, shrunk_formp2p_target_err, shrunk_h2ogs_target_err, shrunk_h2o1b1_target_err]
    # multiplot(multi_all_targetfn, 2, 3, multi_errbars=multi_all_targetfn_errs, fig_title="Target Functions", subplot_titles=['Formaldehyde Ground State', 'Formaldehyde N to Pi* State', 'Formaldehyde Pi to Pi* State', 'H2O Ground State', 'H2O 1B1 State'], ylabel="Target Function", xlabel="Macroiterations")
    
    # plt.show()

    # Variances
    # multi_all_variance = [shrunk_formgs_variance, shrunk_formn2p_variance, shrunk_formp2p_variance, shrunk_h2ogs_variance, shrunk_h2o1b1_variance]
    # multi_all_variance_errs = [shrunk_formgs_variance_err, shrunk_formn2p_variance_err, shrunk_formp2p_variance_err, shrunk_h2ogs_variance_err, shrunk_h2o1b1_variance_err]
    # multiplot(multi_all_variance, 2, 3, multi_errbars=multi_all_variance_errs, fig_title="Variances", subplot_titles=['Formaldehyde Ground State', 'Formaldehyde N to Pi* State', 'Formaldehyde Pi to Pi* State', 'H2O Ground State', 'H2O 1B1 State'], ylabel="Variance", xlabel="Iterations, roughly")
    # plt.show()

if __name__ == "__main__":
    main()