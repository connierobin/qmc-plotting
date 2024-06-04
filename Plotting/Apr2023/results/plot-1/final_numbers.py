from asyncio import format_helpers
from json.tool import main
import os, sys
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import statistics
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

all_h2ogs_files = os.listdir('h2ogs')
edesc_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_edesc_run001' in all_h2ogs_files[i]])
lm_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_lmc_run001' in all_h2ogs_files[i]])
gvp_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvptt_run003' in all_h2ogs_files[i]])
# gvp_h2ogs_split_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvptt_run002' in all_h2ogs_files[i]])
# gvp_h2ogs_splitabs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_gvpabs_run001' in all_h2ogs_files[i]])
te_h2ogs_filenames = sorted([f'h2ogs/{all_h2ogs_files[i]}' for i in range(len(all_h2ogs_files)) if 'h2o_gs_tec_run001' in all_h2ogs_files[i]])

all_1b1_files = os.listdir('h2o1b1')
edesc_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_edesc_run001' in all_1b1_files[i]])
lm_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_lmc_run001' in all_1b1_files[i]])
gvp_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run003' in all_1b1_files[i]])
# gvp_1b1_split_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvptt_run002' in all_1b1_files[i]])
# gvp_1b1_splitabs_filenames = sorted([f'1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_gvpabs_run001' in all_1b1_files[i]])
te_1b1_filenames = sorted([f'h2o1b1/{all_1b1_files[i]}' for i in range(len(all_1b1_files)) if 'h2o_1b1_tec_run001' in all_1b1_files[i]])

all_formgs_files = os.listdir('formgs')
edesc_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_edesc_run001' in all_formgs_files[i]])
lm_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_lmc_run001' in all_formgs_files[i]])
gvp_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvptt_run001' in all_formgs_files[i]])
# gvp_formgs_split_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvptt_run004' in all_formgs_files[i]])
# gvp_formgs_splitabs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_gvpabs_run002' in all_formgs_files[i]])
te_formgs_filenames = sorted([f'formgs/{all_formgs_files[i]}' for i in range(len(all_formgs_files)) if 'form_gs_tec_run002' in all_formgs_files[i]])

all_formn2pistar_files = os.listdir('formn2pistar')
edesc_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_edesc_run001' in all_formn2pistar_files[i]])
lm_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_lmc_run001' in all_formn2pistar_files[i]])
gvp_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvptt_run001' in all_formn2pistar_files[i]])
# gvp_formn2pistar_split_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvptt_run003' in all_formn2pistar_files[i]])
# gvp_formn2pistar_splitabs_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_gvpabs_run001' in all_formn2pistar_files[i]])
te_formn2pistar_filenames = sorted([f'formn2pistar/{all_formn2pistar_files[i]}' for i in range(len(all_formn2pistar_files)) if 'form_n2pistar_tec_run002' in all_formn2pistar_files[i]])

all_formpi2pistar_files = os.listdir('formpi2pistar')
gvp_formpi2pistar_filenames = sorted([f'formpi2pistar/{all_formpi2pistar_files[i]}' for i in range(len(all_formpi2pistar_files)) if 'form_pi2pistar_gvptt_run001' in all_formpi2pistar_files[i]])
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

name_list = ["E desc","LM", "GVP", "targetExcited"]
color_list = ["red", "blue", "green", "black", "purple", "orange", "cyan", "pink", "yellow", "gray"]
jfirst_list = [False, False, False, False]
eV_factor = 27.2114

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

# Shrink data through averaging buckets of size n_ci
def shrink_data(all_data, n_ci):
    all_shrunk_data = []
    all_shrunk_errs = []
    counter1 = 0
    counter2 = 0
    for this_run_data in all_data:
        counter2 = 0
        counter1 += 1
        this_file_shrunk_data = []
        this_file_shrunk_err = []
        for dataset in this_run_data:
            counter2 += 1
            if len(dataset) % n_ci != 0 or len(dataset) == 0:
                return all_data
            shrunk_data = [sum(dataset[ n_ci*i : n_ci*(i+1) ]) / n_ci for i in range(int(len(dataset)/n_ci))]
            shrunk_err = [np.std(dataset[ n_ci*i : n_ci*(i+1) ]) / np.sqrt(n_ci) for i in range(int(len(dataset)/n_ci))]
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

# Plot energies
def plot_energies(all_energies, errbars=None, avgN=0, fig_title=None):
    plt.figure("Energies")
    ax = plt.gca()
    #ax.set_title(fig_title)
    for i, energies in enumerate(all_energies):
        plot_subplot_data(energies, name_list[i], color_list[i], jfirst_list[i], ax=ax, errbars=errbars[i], avgN=avgN, subplot_title=fig_title)
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

# Plot only the final energies for each state to compare the methods
def plot_avgN_finals(all_energies, N=20, ax=None, title=None, need_legend=False, p2p=False, n2p=False, h2o1b1=False):
    if ax == None:
        ax = plt.gca()
        need_legend = True
    markers_list = ['o', 'X', 's', 'p', '*', 'D', 'v', '1', 'P', '6']
    ax.set_title(title)
    y_vals = []
    #plt.figure("Energies, avg10")
    # compiled_file_list = []
    for i, method_energies in enumerate(all_energies):
        avg_N = np.average(all_energies[i][-1][-N:])
        err_N = np.std(all_energies[i][-1][-N:]) / np.sqrt(N)
        y_vals.append(avg_N)
        #plt.plot([j], avg_10, marker=markers_list[i], label=file, color=color_list[i])
        if need_legend:
            ax.errorbar([i], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i], label=name_list[i], color=color_list[i])
        elif p2p:
            ax.errorbar([i], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i+2], color=color_list[i+2])
        elif n2p or h2o1b1:
            ax.errorbar([i], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i+1], color=color_list[i+1])
        else:
            ax.errorbar([i], avg_N, yerr=err_N, capsize=5.0, marker=markers_list[i], color=color_list[i])
    ax.set(xlabel="Method", ylabel="Energy (Ha)")
    if (max(y_vals) - min(y_vals)) < 0.002:
       y_avg = round(np.average(y_vals),3)
       ax.set_ylim(y_avg - 0.0015, y_avg + 0.0015)
       ax.set_yticks([y_avg - 0.001, y_avg, y_avg + 0.001])
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    if p2p:
        x = np.array([0])
        ax.set_xticks(x)
        my_xticks = [name_list[2]]
        ax.set_xticklabels(my_xticks)
        ax.set_xlim(-0.5, 0.5)
    elif n2p or h2o1b1:
        x = np.array([0,1])
        ax.set_xticks(x)
        my_xticks = [name_list[1], name_list[2]]
        ax.set_xticklabels(my_xticks)
        ax.set_xlim(-0.5, 1.5)
    else:
        x = np.array([0,1,2])
        ax.set_xticks(x)
        my_xticks = [name_list[0], name_list[1], name_list[2]]
        ax.set_xticklabels(my_xticks)
        ax.set_xlim(-0.5, 2.5)
    # plt.ylabel("Energy (Ha)")
    # if need_legend:
    #     plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    #     plt.subplots_adjust(wspace=0.3, hspace=0.35)

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

# Plot a whole bunch of average 10 energies over macro iterations
def multiplot_avgN_finals(multi_all_energies, num_rows, num_cols, subplot_titles, N1=10, N2=10):
    fig, (ax_list) = plt.subplots(nrows=num_rows, ncols=num_cols, sharex=False)
    flat_ax_list = ax_list.flatten()
    num_blank_grids = len(flat_ax_list) - len(multi_all_energies)
    for j, all_energies in enumerate(multi_all_energies):
        if j == 0:
            plot_avgN_finals(all_energies, ax=flat_ax_list[j], title=subplot_titles[j], need_legend=True)
        elif j == 1:
            plot_avgN_finals(all_energies, ax=flat_ax_list[j], title=subplot_titles[j], n2p=True)
        elif j == 2:
            plot_avgN_finals(all_energies, ax=flat_ax_list[j], title=subplot_titles[j], p2p=True)
        elif j == 4:
            plot_avgN_finals(all_energies, ax=flat_ax_list[j], title=subplot_titles[j], h2o1b1=True)
        else:
            plot_avgN_finals(all_energies, ax=flat_ax_list[j], title=subplot_titles[j])
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

# Non-generalized way to plot the energy differences for my current data
def multiplot_avgN_differences_finals(multi_all_energies, units='Ha'):
    formgs_energies = multi_all_energies[0]
    formn2p_energies = multi_all_energies[1]
    formp2p_energies = multi_all_energies[2]
    h2ogs_energies = multi_all_energies[3]
    h2o1b1_energies = multi_all_energies[4]
    markers_list = ['o', 's', 'v', 'D', '*', 'P', 'p', 'v', '1', 'P', '6']
    fig, (ax_list) = plt.subplots(nrows=1, ncols=3, sharex=False)
    flat_ax_list = ax_list.flatten()
    # fig.suptitle('Energy Differences', fontsize=16)
    # Plot Form N2Pi*
    N = 20
    ax = flat_ax_list[0]
    ax.set_title('Formaldehyde N to Pi*')
    name_list = ['LM', 'GVP']
    for i in range(len(formn2p_energies)):
        formgs_avg_N = np.average(formgs_energies[i][-1][-N:])
        formgs_err_N = np.std(formgs_energies[i][-1][-N:]) / np.sqrt(N)
        formn2p_avg_N = np.average(formn2p_energies[i][-1][-N:])
        formn2p_err_N = np.std(formn2p_energies[i][-1][-N:]) / np.sqrt(N)
        formn2p_diff_avg_N = formn2p_avg_N - formgs_avg_N
        formn2p_diff_err_N = formn2p_err_N + formgs_err_N
        if units == 'eV':
            formn2p_diff_avg_N = formn2p_diff_avg_N * eV_factor
            formn2p_diff_err_N = formn2p_diff_err_N * eV_factor
        ax.errorbar([i], formn2p_diff_avg_N, yerr=formn2p_diff_err_N, capsize=5.0, marker=markers_list[i+1], label=name_list[i], color=color_list[i+1])
    if units == 'eV':
        ax.set(xlabel="Method", ylabel="Energy (eV)")
    else:
        ax.set(xlabel="Method", ylabel="Energy (Ha)")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    x = np.array([0,1])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 1.5)
    if units != 'eV':
        ax.set_ylim(0.1538, 0.1562)
        ax.set_yticks([0.154, 0.155, 0.156])
    # Plot Form Pi2Pi*
    N = 20
    ax = flat_ax_list[1]
    ax.set_title('Formaldehyde Pi to Pi*')
    name_list = ['GVP']
    for i in range(len(formp2p_energies)):
        formgs_avg_N = np.average(formgs_energies[i+2][-1][-N:])
        formgs_err_N = np.std(formgs_energies[i+2][-1][-N:]) / np.sqrt(N)
        formp2p_avg_N = np.average(formp2p_energies[i][-1][-N:])
        formp2p_err_N = np.std(formp2p_energies[i][-1][-N:]) / np.sqrt(N)
        formp2p_diff_avg_N = formp2p_avg_N - formgs_avg_N
        formp2p_diff_err_N = formp2p_err_N + formgs_err_N
        if units == 'eV':
            formp2p_diff_avg_N = formp2p_diff_avg_N * eV_factor
            formp2p_diff_err_N = formp2p_diff_err_N * eV_factor
        ax.errorbar([i], formp2p_diff_avg_N, yerr=formp2p_diff_err_N, capsize=5.0, marker=markers_list[i+2], color=color_list[i+2])
    ax.set(xlabel="Method")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    x = np.array([0])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 0.5)
    if units == 'eV':
        ax.set_ylim(10.564, 10.58)
    else:
        ax.set_ylim(0.3878, 0.3892)
        ax.set_yticks([0.388, 0.389])
    # Plot H2O 1B1
    N = 20
    ax = flat_ax_list[2]
    ax.set_title('H2O 1B1')
    name_list = ['LM', 'GVP']
    for i in range(len(h2o1b1_energies)):
        h2ogs_avg_N = np.average(h2ogs_energies[i+1][-1][-N:])
        h2ogs_err_N = np.std(h2ogs_energies[i+1][-1][-N:]) / np.sqrt(N)
        h2o1b1_avg_N = np.average(h2o1b1_energies[i][-1][-N:])
        h2o1b1_err_N = np.std(h2o1b1_energies[i][-1][-N:]) / np.sqrt(N)
        h2o1b1_diff_avg_N = h2o1b1_avg_N - h2ogs_avg_N
        h2o1b1_diff_err_N = h2o1b1_err_N + h2ogs_err_N
        if units == 'eV':
            h2o1b1_diff_avg_N = h2o1b1_diff_avg_N * eV_factor
            h2o1b1_diff_err_N = h2o1b1_diff_err_N * eV_factor
        ax.errorbar([i], h2o1b1_diff_avg_N, yerr=h2o1b1_diff_err_N, capsize=5.0, marker=markers_list[i+1], color=color_list[i+1])
    ax.set(xlabel="Method")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    x = np.array([0,1])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 1.5)
    if units != 'eV':
        ax.set_ylim(0.3098, 0.3112)
        ax.set_yticks([0.310, 0.311])

    plt.subplots_adjust(wspace=0.4, hspace=0.35, top=0.8, bottom=0.2)
    #fig.legend(loc='lower right', bbox_to_anchor=(.95, 1.0))
    fig.legend(loc='right')
    fig.set_size_inches(10,3,forward=True)

# Non-generalized way to plot the energy differences for my current data NO GRAD DESC E DESC
def multiplot_avgN_differences_finals_subset(multi_all_energies, units='Ha'):
    formgs_energies = multi_all_energies[0][1:] # LM, GVP, TE
    formn2p_energies = multi_all_energies[1]    # LM, GVP, TE
    formp2p_energies = multi_all_energies[2]    # GVP, TE
    h2ogs_energies = multi_all_energies[3][1:]  # LM, GVP, TE
    h2o1b1_energies = multi_all_energies[4]     # LM, GVP, TE
    markers_list = ['o', 's', 'v', 'D', '*', 'P', 'p', 'v', '1', 'P', '6']
    fig, (ax_list) = plt.subplots(nrows=1, ncols=3, sharex=False)
    flat_ax_list = ax_list.flatten()
    fig.suptitle('Energy Differences', fontsize=16)
    # Plot Form N2Pi*
    N = 20
    ax = flat_ax_list[0]
    ax.set_title('Formaldehyde N to Pi*')
    name_list = ['LM', 'GVP', 'Variance']
    for i in range(len(formgs_energies)):
        formgs_avg_N = np.average(formgs_energies[i][-1][-N:])
        formgs_err_N = np.std(formgs_energies[i][-1][-N:]) / np.sqrt(N)
        formn2p_avg_N = np.average(formn2p_energies[i][-1][-N:])
        formn2p_err_N = np.std(formn2p_energies[i][-1][-N:]) / np.sqrt(N)
        formn2p_diff_avg_N = formn2p_avg_N - formgs_avg_N
        formn2p_diff_err_N = formn2p_err_N + formgs_err_N
        if units == 'eV':
            formn2p_diff_avg_N = formn2p_diff_avg_N * eV_factor
            formn2p_diff_err_N = formn2p_diff_err_N * eV_factor
        ax.errorbar([i], formn2p_diff_avg_N, yerr=formn2p_diff_err_N, capsize=5.0, marker=markers_list[i+1], label=name_list[i], color=color_list[i+1])
    if units == 'eV':
        ax.set(xlabel="Method", ylabel="Energy (eV)")
    else:
        ax.set(xlabel="Method", ylabel="Energy (Ha)")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    x = np.array([0,1,2])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 2.5)
    # Plot Form Pi2Pi*
    N = 20
    ax = flat_ax_list[1]
    ax.set_title('Formaldehyde Pi to Pi*')
    name_list = ['GVP', 'Variance']
    for i in range(len(formp2p_energies)):
        formgs_avg_N = np.average(formgs_energies[i+1][-1][-N:])
        formgs_err_N = np.std(formgs_energies[i+1][-1][-N:]) / np.sqrt(N)
        formp2p_avg_N = np.average(formp2p_energies[i][-1][-N:])
        formp2p_err_N = np.std(formp2p_energies[i][-1][-N:]) / np.sqrt(N)
        formp2p_diff_avg_N = formp2p_avg_N - formgs_avg_N
        formp2p_diff_err_N = formp2p_err_N + formgs_err_N
        if units == 'eV':
            formp2p_diff_avg_N = formp2p_diff_avg_N * eV_factor
            formp2p_diff_err_N = formp2p_diff_err_N * eV_factor
        ax.errorbar([i], formp2p_diff_avg_N, yerr=formp2p_diff_err_N, capsize=5.0, marker=markers_list[i+2], color=color_list[i+2])
    ax.set(xlabel="Method")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    x = np.array([0,1])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 1.5)
    # Plot H2O 1B1
    N = 20
    ax = flat_ax_list[2]
    ax.set_title('H2O 1B1')
    name_list = ['LM', 'GVP', 'Variance']
    for i in range(len(h2ogs_energies)):
        h2ogs_avg_N = np.average(h2ogs_energies[i][-1][-N:])
        h2ogs_err_N = np.std(h2ogs_energies[i][-1][-N:]) / np.sqrt(N)
        h2o1b1_avg_N = np.average(h2o1b1_energies[i][-1][-N:])
        h2o1b1_err_N = np.std(h2o1b1_energies[i][-1][-N:]) / np.sqrt(N)
        h2o1b1_diff_avg_N = h2o1b1_avg_N - h2ogs_avg_N
        h2o1b1_diff_err_N = h2o1b1_err_N + h2ogs_err_N
        if units == 'eV':
            h2o1b1_diff_avg_N = h2o1b1_diff_avg_N * eV_factor
            h2o1b1_diff_err_N = h2o1b1_diff_err_N * eV_factor
        ax.errorbar([i], h2o1b1_diff_avg_N, yerr=h2o1b1_diff_err_N, capsize=5.0, marker=markers_list[i+1], color=color_list[i+1])
    ax.set(xlabel="Method")
    ax.yaxis.get_major_formatter().set_useOffset(False)
    x = np.array([0,1,2])
    ax.set_xticks(x)
    my_xticks = name_list
    ax.set_xticklabels(my_xticks)
    ax.set_xlim(-0.5, 2.5)

    plt.subplots_adjust(wspace=0.4, hspace=0.35, top=0.8, bottom=0.2)
    #fig.legend(loc='lower right', bbox_to_anchor=(.95, 1.0))
    fig.legend(loc='right')
    fig.set_size_inches(10,3,forward=True)

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

    formgs_energies = []
    formgs_variances = []
    formgs_uncertainties_of_variances = []
    formgs_standard_deviations = []
    formgs_standard_errors = []
    formgs_target_functions = []
    formgs_target_fn_standard_errors = []
    formgs_grad_norms = []
    formgs_all_iters_lderivs = []
    formgs_param_update_sizes = []
    formgs_largest_param_updates = []
    formgs_qmc_timing = []
    formgs_total_timing = []

    formn2p_energies = []
    formn2p_variances = []
    formn2p_uncertainties_of_variances = []
    formn2p_standard_deviations = []
    formn2p_standard_errors = []
    formn2p_target_functions = []
    formn2p_target_fn_standard_errors = []
    formn2p_grad_norms = []
    formn2p_all_iters_lderivs = []
    formn2p_param_update_sizes = []
    formn2p_largest_param_updates = []
    formn2p_qmc_timing = []
    formn2p_total_timing = []

    formp2p_energies = []
    formp2p_variances = []
    formp2p_uncertainties_of_variances = []
    formp2p_standard_deviations = []
    formp2p_standard_errors = []
    formp2p_target_functions = []
    formp2p_target_fn_standard_errors = []
    formp2p_grad_norms = []
    formp2p_all_iters_lderivs = []
    formp2p_param_update_sizes = []
    formp2p_largest_param_updates = []
    formp2p_qmc_timing = []
    formp2p_total_timing = []

    # Variables to tweak the plotting
    energy_shrink_amount = 10
    targetfn_shrink_amount = 10
    variance_shrink_amount = 10
    n = 20
    max_iter = 8

    ##########
    # H2O GS #
    ##########
    # Read the files
    # h2ogs_files = [edesc_h2ogs_filenames, 
    #                lm_h2ogs_filenames,
    #                gvp_h2ogs_filenames, 
    #                te_h2ogs_filenames]
    h2ogs_files = [edesc_h2ogs_filenames, 
                   lm_h2ogs_filenames,
                   gvp_h2ogs_filenames]
    target_state_used_list = [False, False, False, True]
    for (i, state_files) in enumerate(h2ogs_files):
        read_files(state_files, h2ogs_energies, h2ogs_variances, h2ogs_uncertainties_of_variances, h2ogs_standard_deviations, h2ogs_standard_errors, h2ogs_target_functions, h2ogs_target_fn_standard_errors, h2ogs_grad_norms, h2ogs_all_iters_lderivs, h2ogs_param_update_sizes, h2ogs_largest_param_updates, h2ogs_qmc_timing, h2ogs_total_timing, target_state_used=target_state_used_list[i])

    for j in range(len(h2ogs_energies)):    # Loop each method: LM, GVP...
        h2ogs_energies[j] = h2ogs_energies[j][:max_iter]  # Cut off files past the max_iter amount

    h2ogs_final = [np.average(h2ogs_energies[i][-1][-n:]) for i in range(len(h2ogs_energies))]

    # ###########
    # # H2O 1B1 #
    # ###########
    # # Read the files to get data
    # h2o1b1_files = [edesc_1b1_filenames, 
    #                lm_1b1_filenames,
    #                gvp_1b1_filenames, 
    #                te_1b1_filenames]
    h2o1b1_files = [lm_1b1_filenames,
                    gvp_1b1_filenames]
    for state_files in h2o1b1_files:
        read_files(state_files, h2o1b1_energies, h2o1b1_variances, h2o1b1_uncertainties_of_variances, h2o1b1_standard_deviations, h2o1b1_standard_errors, h2o1b1_target_functions, h2o1b1_target_fn_standard_errors, h2o1b1_grad_norms, h2o1b1_all_iters_lderivs, h2o1b1_param_update_sizes, h2o1b1_largest_param_updates, h2o1b1_qmc_timing, h2o1b1_total_timing)

    for j in range(len(h2o1b1_energies)):    # Loop each method: LM, GVP...
        h2o1b1_energies[j] = h2o1b1_energies[j][:max_iter]  # Cut off files past the max_iter amount

    h2o1b1_final = [np.average(h2o1b1_energies[i][-1][-n:]) for i in range(len(h2o1b1_energies))]

    ##########
    # FORM GS #
    ##########
    # Read the files to get data
    # formgs_files = [edesc_formgs_filenames, 
    #                 lm_formgs_filenames,
    #                 gvp_formgs_filenames, 
    #                 te_formgs_filenames]
    formgs_files = [edesc_formgs_filenames, 
                    lm_formgs_filenames,
                    gvp_formgs_filenames]
    for state_files in formgs_files:
        read_files(state_files, formgs_energies, formgs_variances, formgs_uncertainties_of_variances, formgs_standard_deviations, formgs_standard_errors, formgs_target_functions, formgs_target_fn_standard_errors, formgs_grad_norms, formgs_all_iters_lderivs, formgs_param_update_sizes, formgs_largest_param_updates, formgs_qmc_timing, formgs_total_timing)

    for j in range(len(formgs_energies)):    # Loop each method: LM, GVP...
        formgs_energies[j] = formgs_energies[j][:max_iter]  # Cut off files past the max_iter amount

    formgs_final = [np.average(formgs_energies[i][-1][-n:]) for i in range(len(formgs_energies))]

    #################
    # FORM N2PISTAR #
    #################
    # Read the files to get data
    # formn2pistar_files = [edesc_formn2pistar_filenames, 
    #                       lm_formn2pistar_filenames,
    #                       gvp_formn2pistar_filenames, 
    #                       te_formn2pistar_filenames]
    formn2pistar_files = [lm_formn2pistar_filenames,
                          gvp_formn2pistar_filenames]
    for state_files in formn2pistar_files:
        read_files(state_files, formn2p_energies, formn2p_variances, formn2p_uncertainties_of_variances, formn2p_standard_deviations, formn2p_standard_errors, formn2p_target_functions, formn2p_target_fn_standard_errors, formn2p_grad_norms, formn2p_all_iters_lderivs, formn2p_param_update_sizes, formn2p_largest_param_updates, formn2p_qmc_timing, formn2p_total_timing)

    for j in range(len(formn2p_energies)):    # Loop each method: LM, GVP...
        formn2p_energies[j] = formn2p_energies[j][:max_iter]  # Cut off files past the max_iter amount

    formn2p_final = [np.average(formn2p_energies[i][-1][-n:]) for i in range(len(formn2p_energies))]

    #################
    # FORM PI2PISTAR #
    #################
    # Read the files to get data
    # formp2pistar_files = [gvp_formpi2pistar_filenames, 
    #                       te_formpi2pistar_filenames]
    formp2pistar_files = [gvp_formpi2pistar_filenames]
    for state_files in formp2pistar_files:
        read_files(state_files, formp2p_energies, formp2p_variances, formp2p_uncertainties_of_variances, formp2p_standard_deviations, formp2p_standard_errors, formp2p_target_functions, formp2p_target_fn_standard_errors, formp2p_grad_norms, formp2p_all_iters_lderivs, formp2p_param_update_sizes, formp2p_largest_param_updates, formp2p_qmc_timing, formp2p_total_timing)
    
    for j in range(len(formp2p_energies)):    # Loop each method: LM, GVP...
        formp2p_energies[j] = formp2p_energies[j][:max_iter]  # Cut off files past the max_iter amount

    formp2p_final = [np.average(formp2p_energies[i][-1][-n:]) for i in range(len(formp2p_energies))]

    ############
    # MEGAPLOT #
    ############

    # fig, ax = plt.subplots()

    # plt.title('H2O Ground State Energy Results')
    # x = np.array([0,1,2])
    # my_xticks = name_list[:-1]
    # y = h2ogs_final
    # plt.xticks(x, my_xticks)
    # plt.bar(x[0], y[0])
    # plt.bar(x[1], y[1])
    # plt.bar(x[2], y[2])
    # plt.show()

    # plt.title('H2O 1B1 Energy Results')
    # x = np.array([0,1,2])
    # my_xticks = name_list[:-1]
    # y = h2o1b1_final
    # plt.xticks(x, my_xticks)
    # plt.bar(x[0], y[0])
    # plt.bar(x[1], y[1])
    # plt.bar(x[2], y[2])
    # plt.show()

    # plt.title('H2O 1B1 Relative Energy Results')
    # x = np.array([0,1,2,3])
    # my_xticks = name_list
    # y = [h2o1b1_final[i] - h2ogs_final[i] for i in range(len(h2ogs_final))]
    # plt.xticks(x, my_xticks)
    # plt.bar(x[0], y[0])
    # plt.bar(x[1], y[1])
    # plt.bar(x[2], y[2])
    # plt.bar(x[3], y[3])
    # plt.show()

    multi_all_energies = [formgs_energies, formn2p_energies, formp2p_energies, h2ogs_energies, h2o1b1_energies]
    multi_all_files = [formgs_files, formn2pistar_files, formp2pistar_files, h2ogs_files, h2o1b1_files]
    subplot_titles = ['Formaldehyde Ground State', 'Formaldehyde N to Pi* State', 'Formaldehyde Pi to Pi* State', 'H2O Ground State', 'H2O 1B1 State']

    multiplot_avgN_finals(multi_all_energies, 2, 3, subplot_titles=subplot_titles)
    plt.show()

    multiplot_avgN_differences_finals(multi_all_energies)
    plt.show()

    multiplot_avgN_differences_finals(multi_all_energies, units='eV')
    plt.show()

    multiplot_avgN_differences_finals_subset(multi_all_energies, units='eV')
    plt.show()


if __name__ == "__main__":
    main()
