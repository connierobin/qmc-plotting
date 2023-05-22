from asyncio import format_helpers
from json.tool import main
import os, sys
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import statistics
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

all_h2ogs_files = os.listdir('h2ogs')
# edesc_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_edesc_run001' in all_h2ogs_files[i]])
# lm_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_lmc_run001' in all_h2ogs_files[i]])
# gvp_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvptt_run003' in all_h2ogs_files[i]])
# gvp_h2ogs_split_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvptt_run002' in all_h2ogs_files[i]])
# gvp_h2ogs_splitabs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpabs_run001' in all_h2ogs_files[i]])
te_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_tec_run001' in all_h2ogs_files[i]])
te_h2ogs_32dets_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_tec_32dets_run001' in all_h2ogs_files[i]])
te_h2ogs_48dets_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_tec_48dets_run001' in all_h2ogs_files[i]])

all_1b1_files = os.listdir('h2o1b1')
# edesc_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_edesc_run001' in all_1b1_files[i]])
# lm_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_lmc_run001' in all_1b1_files[i]])
# gvp_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run003' in all_1b1_files[i]])
# gvp_1b1_split_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run002' in all_1b1_files[i]])
# gvp_1b1_splitabs_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvpabs_run001' in all_1b1_files[i]])
te_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_tec_run001' in all_1b1_files[i]])

all_formgs_files = os.listdir('formgs')
# edesc_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_edesc_run001' in all_formgs_files[i]])
# lm_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_lmc_run001' in all_formgs_files[i]])
# gvp_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvptt_run001' in all_formgs_files[i]])
# gvp_formgs_split_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvptt_run004' in all_formgs_files[i]])
# gvp_formgs_splitabs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvpabs_run002' in all_formgs_files[i]])
te_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_tec_run002' in all_formgs_files[i]])
te_formgs_45dets_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_tec_45dets_run001' in all_formgs_files[i]])
te_formgs_56dets_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_tec_56dets_run001' in all_formgs_files[i]])

all_formn2pistar_files = os.listdir('formn2pistar')
# edesc_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_edesc_run001' in all_formn2pistar_files[i]])
# lm_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_lmc_run001' in all_formn2pistar_files[i]])
# gvp_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvptt_run001' in all_formn2pistar_files[i]])
# gvp_formn2pistar_split_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvptt_run003' in all_formn2pistar_files[i]])
# gvp_formn2pistar_splitabs_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvpabs_run001' in all_formn2pistar_files[i]])
te_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_tec_run002' in all_formn2pistar_files[i]])

all_formpi2pistar_files = os.listdir('formpi2pistar')
# gvp_formpi2pistar_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_gvptt_run001' in all_formpi2pistar_files[i]])
# gvp_formpi2pistar_split_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_gvptt_run003' in all_formpi2pistar_files[i]])
# gvp_formpi2pistar_splitabs_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_gvpabs_run001' in all_formpi2pistar_files[i]])
# lm_formpi2pistar_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_lmc_run001' in all_formpi2pistar_files[i]])
te_formpi2pistar_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_tec_run002' in all_formpi2pistar_files[i]])

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

color_list = ["red", "blue", "green", "black", "purple", "orange"]
jfirst_list = [False, False, False, False, False]

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

def read_files(file_names, all_energies, all_variances, all_uncert_of_varriances, all_stdevs, all_stderrs, all_target_functions, all_target_fn_stderrs, all_grad_norms, all_lderivs, all_param_update_sizes, all_largest_param_updates, all_qmc_timings, all_total_timings, target_state_used=None):
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

    for file in file_names:
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

# Shrink data through averaging buckets of size n_ci and n_j alternating
def shrink_data(all_data, n_ci, n_j):
    all_shrunk_data = []
    all_shrunk_errs = []
    for this_run_data in all_data:
        this_file_shrunk_data = []
        this_file_shrunk_err = []
        toggle = 0
        for dataset in this_run_data:
            if toggle == 0:
                n = n_ci
                toggle = 1
            else:
                n = n_j
                toggle = 0
            if len(dataset) % n != 0:
                print(f'data of length {len(dataset)} is not divisible by {n}')
                return all_data
            shrunk_data = [sum(dataset[ n*i : n*(i+1) ]) / n for i in range(int(len(dataset)/n))]
            shrunk_err = [np.std(dataset[ n*i : n*(i+1) ]) / np.sqrt(n) for i in range(int(len(dataset)/n))]
            this_file_shrunk_data.append(shrunk_data)
            this_file_shrunk_err.append(shrunk_err)
        all_shrunk_data.append(this_file_shrunk_data)
        all_shrunk_errs.append(this_file_shrunk_err)
    return (all_shrunk_data, all_shrunk_errs)

# Plot one set of energy data
def plot_subplot_data(vector_data, data_label, data_color, jfirst, ax=None, errbars=None, subplot_title=None, avgN=0):
    current_x = 0
    plotting_jastrows = jfirst
    first = True
    for (i, data) in enumerate(vector_data):
        if len(data) == 0:
            continue
        cur_errbars = errbars[i]
        # Old way to do the x axis, each tick is a data point:
        #x = np.arange(current_x, current_x + len(data))
        #current_x = current_x + len(data)
        # New way to do the x axis, each tick is a half-macroiteration:
        x = np.arange(current_x, current_x + 0.5, 0.5 / len(data))
        current_x = current_x + 0.5
        if first:
            if plotting_jastrows:
                ax.errorbar(x, data, yerr=cur_errbars, marker='x', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                ax.errorbar(x, data, yerr=cur_errbars, marker='o', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            first = False
        else:
            if plotting_jastrows:
                ax.errorbar(x, data, yerr=cur_errbars, marker='x', color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                ax.errorbar(x, data, yerr=cur_errbars, marker='o', color=data_color)
                plotting_jastrows = not plotting_jastrows
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

# Plot one set of energy data
def plot_subplot_final_lines(vector_data, data_label, data_color, jfirst, ax=None, errbars=None, subplot_title=None, avgN=0):
    current_x = 0
    plotting_jastrows = jfirst
    first = True
    print('before')
    print(len(vector_data))
    print(len(vector_data[-1]))
    print(vector_data[-1][-avgN])
    for (i, data) in enumerate(vector_data):
        cur_errbars = errbars[i]
        # Old way to do the x axis, each tick is a data point:
        #x = np.arange(current_x, current_x + len(data))
        #current_x = current_x + len(data)
        # New way to do the x axis, each tick is a half-macroiteration:
        x = np.arange(current_x, current_x + 0.5, 0.5 / len(data))
        current_x = current_x + 0.5
        if first:
            if plotting_jastrows:
                #ax.errorbar(x, data, yerr=cur_errbars, marker='x', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                # ax.errorbar(x, data, yerr=cur_errbars, marker='o', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            first = False
        else:
            if plotting_jastrows:
                # ax.errorbar(x, data, yerr=cur_errbars, marker='x', color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                # WHY does uncommenting this line change how the axhline show up????
                # ax.errorbar(x, data, yerr=cur_errbars, marker='o', color=data_color)
                plotting_jastrows = not plotting_jastrows
        ax.set_title(subplot_title)

    current_x = 10
    print('after')
    print(len(vector_data))
    print(len(vector_data[-1]))
    print(vector_data[-1][-avgN])
    # Plot a line showing the final result, if desired
    if avgN > 0:
        final_result = np.average(vector_data[-1][-avgN:])
        final_errs = np.std(vector_data[-1][-avgN:])
        ax.axhline(xmin=0, xmax=current_x, y=final_result, color=data_color, label=data_label, linestyle='-')
        x_range = np.array([0, current_x])
        ax.fill_between(x_range, final_result-final_errs, final_result+final_errs, color=data_color, alpha=0.1)
    # Axis formatting for energy plots only
    # flat_ax_list[j].yaxis.set_major_formatter('{x:.3f}')             # Use mHa units
    # flat_ax_list[j].yaxis.set_major_locator(MultipleLocator(0.001))
    # If it's using an offset do this
    ax.yaxis.get_major_formatter().set_useOffset(False)
    # Macroiteration formatting
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))    # default is no labels on the minor ticks

# Plot energies
def plot_energies(all_energies, errbars=None, avgN=0, fig_title=None, labels=None):
    plt.figure("Energies")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, energies in enumerate(all_energies):
        if labels is None:
            label = None
        else:
            label = labels[i]
        plot_subplot_data(energies, label, color_list[i], jfirst_list[i], ax=ax, errbars=errbars[i], avgN=avgN, subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Energy (Ha)")
    plt.subplots_adjust(wspace=0.3, hspace=0.35)

# Plot target function
def plot_target_functions(all_target_functions, errbars=None, avgN=0, fig_title=None):
    plt.figure("Target Functions")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, target_function in enumerate(all_target_functions):
        plot_subplot_data(target_function, name_list[i], color_list[i], jfirst_list[i], ax=ax, avgN=avgN, errbars=errbars[i], subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Target Function")

# Plot variances
def plot_variances(all_variances, errbars=None, avgN=0, fig_title=None, labels=None):
    plt.figure("Variances")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, variance in enumerate(all_variances):
        if labels is None:
            label = None
        else:
            label = labels[i]
        plot_subplot_data(variance, label, color_list[i], jfirst_list[i], ax=ax, avgN=avgN, errbars=errbars[i], subplot_title=fig_title)
    ax.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    ax.set(xlabel="Macroiteration", ylabel="Variance")

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
                plot_subplot_data(data, name_list[i], color_list[i], jfirst_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
            else:
                plot_subplot_data(data, None, color_list[i], jfirst_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
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

# Plot subplots
def multiplot_final_lines(multi_all_data, num_rows, num_cols, multi_errbars=None, fig_title=None, subplot_titles=None, ylabel=None, xlabel=None, avgN=0):
    fig, (ax_list) = plt.subplots(nrows=num_rows, ncols=num_cols, sharex=False)
    flat_ax_list = ax_list.flatten()
    num_blank_grids = len(flat_ax_list) - len(multi_all_data)
    for j, all_data in enumerate(multi_all_data):
        errbars = multi_errbars[j]
        fig.suptitle(fig_title)
        # plt.figure(fig_title)
        for i, data in enumerate(all_data):
            if j == 0:
                plot_subplot_final_lines(data, name_list[i], color_list[i], jfirst_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
            else:
                plot_subplot_final_lines(data, None, color_list[i], jfirst_list[i], ax=flat_ax_list[j], errbars=errbars[i], avgN=avgN, subplot_title=subplot_titles[j])
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
        if j == 0:
            plot_avgN(all_files, multi_all_energies[j], N1=N1, N2=N2, ax=flat_ax_list[j], title=subplot_titles[j], labels=name_list)
        else:
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
def plot_avgN(all_files, all_energies, N1=10, N2=10, ax=None, title=None, labels=None):
    need_legend = False
    if ax == None:
        ax = plt.gca()
        need_legend = True
    markers_list = ['o', 'x', 's', 'p', 'P']
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
            if labels == None:
                label = None
            else:
                label = labels[i]
            if j == 0:
                ax.errorbar([(j+1)/2], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i], label=label, color=color_list[i]),
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


def main():
    # Arrays to hold the resulting data
    h2o_energies = []
    h2o_variances = []
    h2o_uncertainties_of_variances = []
    h2o_standard_deviations = []
    h2o_standard_errors = []
    h2o_target_functions = []
    h2o_target_fn_standard_errors = []
    h2o_grad_norms = []
    h2o_all_iters_lderivs = []
    h2o_param_update_sizes = []
    h2o_largest_param_updates = []
    h2o_qmc_timing = []
    h2o_total_timing = []

    form_energies = []
    form_variances = []
    form_uncertainties_of_variances = []
    form_standard_deviations = []
    form_standard_errors = []
    form_target_functions = []
    form_target_fn_standard_errors = []
    form_grad_norms = []
    form_all_iters_lderivs = []
    form_param_update_sizes = []
    form_largest_param_updates = []
    form_qmc_timing = []
    form_total_timing = []

    # Variables to tweak the plotting
    energy_shrink_amount = 20
    energyj_shrink_amount = 20
    targetfn_shrink_amount = 20
    targetfnj_shrink_amount = 20
    variance_shrink_amount = 20
    variancej_shrink_amount = 20

    name_list_h2o = ["gs 32 dets", "gs 48 dets", "gs 70 dets", "1b1 75 dets"]
    name_list_form = ["gs 45 dets", "gs 56 dets", "gs 70 dets", "n2p 77 dets", "p2p 140 dets"]

    #######
    # H2O #
    #######
    # Read the files
    h2o_files = [te_h2ogs_32dets_filenames,
                   te_h2ogs_48dets_filenames, 
                   te_h2ogs_filenames,
                   te_1b1_filenames]
    target_state_used_list = [True, True, True, True]
    for (i, state_files) in enumerate(h2o_files):
        read_files(state_files, h2o_energies, h2o_variances, h2o_uncertainties_of_variances, h2o_standard_deviations, h2o_standard_errors, h2o_target_functions, h2o_target_fn_standard_errors, h2o_grad_norms, h2o_all_iters_lderivs, h2o_param_update_sizes, h2o_largest_param_updates, h2o_qmc_timing, h2o_total_timing, target_state_used=target_state_used_list[i])
    
    # Shrink the data size through averaging so it's easier to read
    (shrunk_h2o_energies, shrunk_h2o_err) = shrink_data(h2o_energies, energy_shrink_amount, energyj_shrink_amount)
    # (shrunk_h2ogs_targetfn, shrunk_h2ogs_target_err) = shrink_data(h2ogs_target_functions, targetfn_shrink_amount, targetfnj_shrink_amount)
    (shrunk_h2o_variance, shrunk_h2o_variance_err) = shrink_data(h2o_variances, variance_shrink_amount, variancej_shrink_amount)
    
    # Plot the data
    plot_avgN(h2o_files, h2o_energies, N1=100, N2=100, labels=name_list_h2o)
    plot_energies(shrunk_h2o_energies, errbars=shrunk_h2o_err, avgN=1, fig_title='H2O Ground State and 1B1 State', labels=name_list_h2o)
    # plot_target_functions(shrunk_h2ogs_targetfn, errbars=shrunk_h2ogs_target_err, fig_title='H2O Ground State')
    plot_variances(shrunk_h2o_variance, errbars=shrunk_h2o_variance_err, fig_title='H2O Ground State and 1B1 State', labels=name_list_h2o)
    plt.show()

    ########
    # FORM #
    ########
    # Read the files to get data
    form_files = [te_formgs_45dets_filenames,
                    te_formgs_56dets_filenames,
                    te_formgs_filenames,
                    te_formn2pistar_filenames,
                    te_formpi2pistar_filenames]
    for state_files in form_files:
        read_files(state_files, form_energies, form_variances, form_uncertainties_of_variances, form_standard_deviations, form_standard_errors, form_target_functions, form_target_fn_standard_errors, form_grad_norms, form_all_iters_lderivs, form_param_update_sizes, form_largest_param_updates, form_qmc_timing, form_total_timing)    
    # Shrink the data size through averaging so it's easier to read
    (shrunk_form_energies, shrunk_form_err) = shrink_data(form_energies, energy_shrink_amount, energyj_shrink_amount)
    # (shrunk_formgs_targetfn, shrunk_formgs_target_err) = shrink_data(formgs_target_functions, targetfn_shrink_amount, targetfnj_shrink_amount)
    (shrunk_form_variance, shrunk_form_variance_err) = shrink_data(form_variances, variance_shrink_amount, variancej_shrink_amount)

    # Plot the data
    plot_avgN(form_files, form_energies, N1=100, N2=100, labels=name_list_form)
    plot_energies(shrunk_form_energies, errbars=shrunk_form_err, avgN=1, fig_title='Formaldehyde', labels=name_list_form)
    # plot_target_functions(shrunk_formgs_targetfn, errbars=shrunk_formgs_target_err, avgN=1, fig_title='Formaldehyde Ground State')
    plot_variances(shrunk_form_variance, errbars=shrunk_form_variance_err, fig_title='Formaldehyde Ground State', labels=name_list_form)
    plt.show()

if __name__ == "__main__":
    main()