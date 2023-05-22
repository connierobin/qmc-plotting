from asyncio import format_helpers
from json.tool import main
import os, sys
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import statistics

color_list = ["red", "blue", "green", "black", "purple", "orange"]
#name_list = ["0 tocks", "2 tocks", "20 tocks", "200 tocks", "20 tocks Jfirst", "200 tocks Jfirst"]
#jfirst_list = [False, False, False, False, True, True]
# name_list = ["lm-gvpj-0-tocks", "lm-gvp-100-tocks", "lm-gvpj-100-tocks"]
# jfirst_list = [True, True, True]
name_list = ["lm-gvp-100-tocks", "gs-lm-gvp-100-tocks"]
jfirst_list = [True, True]

# Go through the file to extract the ci values and tags
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

# Plot energies
def plot_energies(all_energies):
    plt.figure("Energies")
    for i, energies in enumerate(all_energies):
        plot_vector_data(energies, name_list[i], color_list[i], jfirst_list[i])
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("Energy (Ha)")
    plt.xlabel("Iteration")

# Plot target function
def plot_target_functions(all_target_functions):
    plt.figure("Target Functions")
    for i, target_function in enumerate(all_target_functions):
        plot_vector_data(target_function, name_list[i], color_list[i], jfirst_list[i])
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("Target Function")
    plt.xlabel("Iteration")

# Plot variance
def plot_variances(all_variances):
    plt.figure("Variances")
    for i, variances in enumerate(all_variances):
        plot_vector_data(variances, name_list[i], color_list[i], jfirst_list[i])
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("Variance")
    plt.xlabel("Iteration")

# Plot one set of energy data
def plot_vector_data(vector_data, data_label, data_color, jfirst):
    current_x = 0
    plotting_jastrows = jfirst
    first = True
    for data in vector_data:
        # print(f"Data size: {len(data)}")
        x = np.arange(current_x, current_x + len(data))
        current_x = current_x + len(data)
        if first:
            if plotting_jastrows:
                plt.plot(x, data, marker='x', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                plt.plot(x, data, marker='o', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            first = False
        else:
            if plotting_jastrows:
                plt.plot(x, data, marker='x', color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                plt.plot(x, data, marker='o', color=data_color)
                plotting_jastrows = not plotting_jastrows

# Plot lderivs
def plot_lderivs(all_lderivs, num_lderivs_plots):
    for i in range(num_lderivs_plots):
        plt.figure("Lagrangian Derivative %s" % (i))
        for j, lderivs in enumerate(all_lderivs):
            plot_lderiv_data(lderivs, name_list[j], color_list[j], jfirst_list[j], i)
        plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
        plt.ylabel("Derivative {i}")
        plt.xlabel("Iteration")

# Plot one set of lderiv data
def plot_lderiv_data(lderiv_data, data_label, data_color, jfirst, i):
    current_x = 0
    plotting_jastrows = jfirst
    first = True
    for lderivs in lderiv_data:
        x = np.arange(current_x, current_x + len(lderivs))
        current_x = current_x + len(lderivs)
        this_deriv_lderivs = [lderivs[j][i] for j in range(len(lderivs))]
        if first:
            if plotting_jastrows:
                plt.plot(x, this_deriv_lderivs, marker='x', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                plt.plot(x, this_deriv_lderivs, marker='o', label=data_label, color=data_color)
                plotting_jastrows = not plotting_jastrows
            first = False
        else:
            if plotting_jastrows:
                plt.plot(x, this_deriv_lderivs, marker='x', color=data_color)
                plotting_jastrows = not plotting_jastrows
            else:
                plt.plot(x, this_deriv_lderivs, marker='o', color=data_color)
                plotting_jastrows = not plotting_jastrows

def plot_timings(all_qmc_timings, all_total_timings):
    qmc_timing_0_tock = all_qmc_timings[0]
    qmc_timing_2_tock = all_qmc_timings[1]
    qmc_timing_20_tock = all_qmc_timings[2]
    qmc_timing_200_tock = all_qmc_timings[3]
    qmc_timing_20_tock_Jfirst = all_qmc_timings[4]
    qmc_timing_200_tock_Jfirst = all_qmc_timings[5]
    total_timing_0_tock = all_total_timings[0]
    total_timing_2_tock = all_total_timings[1]
    total_timing_20_tock = all_total_timings[2]
    total_timing_200_tock = all_total_timings[3]
    total_timing_20_tock_Jfirst = all_total_timings[4]
    total_timing_200_tock_Jfirst = all_total_timings[5]
    # Calculate cumulative timing info
    qmc_timing_0_tock = np.cumsum(qmc_timing_0_tock)
    qmc_timing_2_tock = np.cumsum(qmc_timing_2_tock)
    qmc_timing_20_tock = np.cumsum(qmc_timing_20_tock)
    qmc_timing_200_tock = np.cumsum(qmc_timing_200_tock)
    qmc_timing_20_tock_Jfirst = np.cumsum(qmc_timing_20_tock_Jfirst)
    qmc_timing_200_tock_Jfirst = np.cumsum(qmc_timing_200_tock_Jfirst)
    total_timing_0_tock = np.cumsum(total_timing_0_tock)
    total_timing_2_tock = np.cumsum(total_timing_2_tock)
    total_timing_20_tock = np.cumsum(total_timing_20_tock)
    total_timing_200_tock = np.cumsum(total_timing_200_tock)
    total_timing_20_tock_Jfirst = np.cumsum(total_timing_20_tock_Jfirst)
    total_timing_200_tock_Jfirst = np.cumsum(total_timing_200_tock_Jfirst)
    # Plot the cumulative timings
    x_0_tock = np.arange(300, 300 * (len(qmc_timing_0_tock) + 1), 300)
    x_2_tock = np.arange(2, 2 * (len(qmc_timing_2_tock) + 1), 2)
    x_20_tock = np.arange(20, 20 * (len(qmc_timing_20_tock) + 1), 20)
    x_200_tock = np.arange(200, 200 * (len(qmc_timing_200_tock) + 1), 200)
    x_20_tock_Jfirst = np.arange(20, 20 * (len(qmc_timing_20_tock_Jfirst) + 1), 20)
    x_200_tock_Jfirst = np.arange(200, 200 * (len(qmc_timing_200_tock_Jfirst) + 1), 200)
    plt.figure("QMC Timing")
    plt.plot(x_0_tock, qmc_timing_0_tock, marker='o', label='0 tock', color='red')
    plt.plot(x_2_tock, qmc_timing_2_tock, marker='o', label='2 tock', color='blue')
    plt.plot(x_20_tock, qmc_timing_20_tock, marker='o', label='20 tock', color='green')
    plt.plot(x_200_tock, qmc_timing_200_tock, marker='o', label='200 tock', color='black')
    plt.plot(x_20_tock_Jfirst, qmc_timing_20_tock_Jfirst, marker='o', label='20 tock Jfirst', color='purple')
    plt.plot(x_200_tock_Jfirst, qmc_timing_200_tock_Jfirst, marker='o', label='200 tock Jfirst', color='orange')
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("Time (s)")
    plt.xlabel("Iteration")
    plt.figure("Total Timing")
    plt.plot(x_0_tock, total_timing_0_tock, marker='o', label='0 tock', color='red')
    plt.plot(x_2_tock, total_timing_2_tock, marker='o', label='2 tock', color='blue')
    plt.plot(x_20_tock, total_timing_20_tock, marker='o', label='20 tock', color='green')
    plt.plot(x_200_tock, total_timing_200_tock, marker='o', label='200 tock', color='black')
    plt.plot(x_20_tock_Jfirst, total_timing_20_tock_Jfirst, marker='o', label='20 tock Jfirst', color='purple')
    plt.plot(x_200_tock_Jfirst, total_timing_200_tock_Jfirst, marker='o', label='200 tock Jfirst', color='orange')
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))
    plt.ylabel("Time (s)")
    plt.xlabel("Iteration")

def read_files(file_names, all_energies, all_variances, all_target_functions, all_lderivs, all_qmc_timings, all_total_timings):
    current_energies = []
    current_variances = []
    current_target_functions = []
    current_lderivs = []
    current_qmc_timing = []
    current_total_timing = []

    for file in file_names:
        print("Reading in %s" % (file))
        (energies, variances, target_functions, lderivs, qmc_timing, total_timing) = process_file(file)
        current_energies.append(energies)
        current_variances.append(variances)
        current_target_functions.append(target_functions)
        current_lderivs.append(lderivs)
        current_qmc_timing.append(qmc_timing)
        current_total_timing.append(total_timing)
    all_energies.append(current_energies)
    all_variances.append(current_variances)
    all_target_functions.append(current_target_functions)
    all_lderivs.append(current_lderivs)
    all_qmc_timings.append(current_qmc_timing)
    all_total_timings.append(current_total_timing)

def plot_avg10(all_files, all_energies):
    markers_list = ['o', 'x', '.']
    plt.figure("Energies, avg10")
    compiled_file_list = []
    avg_10_list = []
    for i, files_list in enumerate(all_files):
        for j, file in enumerate(files_list):
            avg_10 = np.average(all_energies[i][j][-10:])
            avg_10_list.append(avg_10)
            compiled_file_list.append(file)
            plt.plot([j], avg_10, marker=markers_list[i], label=file, color=color_list[i])    
        print(f"{file}: {avg_10}")
    plt.ylabel("Energy (Ha)")
    plt.legend(loc='upper right', bbox_to_anchor=(.95, 1.0))

    # plt.figure("Energies, avg10")
    # for i in range(len(avg_10_list)):
    #     plt.plot([1], avg_10_list[i], marker='o', label=compiled_file_list[i])
    # plt.ylabel("Energy (Ha)")    

    # avg_10_list = []
    # for energy_file in all_energies:
    #     for energy_list in energy_file:
    #         avg_10_list.append(np.average(energy_list[-10:]))
    # i = 0
    # for fileset in all_files:
    #     for file in fileset:
    #         print(f"{file}: {avg_10_list[i]}")
    #         i += 1

def main():
    # Number of files for each tock test
    # H2O
    num_0_tock = 1
    num_2_tock = 20
    num_20_tock = 10
    num_200_tock = 2
    num_20_tock_Jfirst = 10
    num_200_tock_Jfirst = 2
    num_lm_gvpj_0_tock = 2
    num_lm_gvp_100_tock = 4
    num_lm_gvpj_100_tock = 4
    num_lm_gvpj_100_tock_2 = 4
    num_gs_lm_gvp_100_tock = 4
    # formaldehyde
    num_form_gs = 4
    num_form_11b1 = 4
    #########################################
    # File names including enclosing folder #
    #########################################
    # H2O
    tock_files_0 = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/0-tock/h2onosym-gvpj-0tock-{i}.out" for i in range(1, num_0_tock + 1)]
    tock_files_2 = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/2-tock/h2onosym-gvpj-2tock-{i}.out" for i in range(1, num_2_tock + 1)]
    tock_files_20 = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/20-tock/h2onosym-gvpj-20tock-{i}.out" for i in range(1, num_20_tock + 1)]
    tock_files_200 = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/200-tock/h2onosym-gvpj-200tock-{i}.out" for i in range(1, num_200_tock + 1)]
    tock_files_20_Jfirst = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/20-tock-Jfirst/h2onosym-jgvp-20tock-{i}.out" for i in range(1, num_20_tock_Jfirst + 1)]
    tock_files_200_Jfirst = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/200-tock-Jfirst/h2onosym-jgvp-200tock-{i}.out" for i in range(1, num_200_tock_Jfirst + 1)]
    tock_files_LM_GVPJ_0_tock = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/LM-GVPJ-0-tock/h2onosym-lm-gvpj-0tock-{i}.out" for i in range(1, num_lm_gvpj_0_tock + 1)]
    tock_files_LM_GVP_100_tock = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/LM-GVP-100-tock/h2onosym-lm-gvp-100tock-{i}.out" for i in range(1, num_lm_gvp_100_tock + 1)]
    tock_files_LM_GVPJ_100_tock = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/LM-GVPJ-100-tock/h2onosym-lm-gvpj-100tock-{i}.out" for i in range(1, num_lm_gvpj_100_tock + 1)]
    tock_files_LM_GVPJ_100_tock_2 = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_and_Jastrows/LM-GVPJ-100-tock-2/h2onosym-lm-gvpj-100tock-{i}.out" for i in range(1, num_lm_gvpj_100_tock_2 + 1)]
    tock_files_gs_LM_GVP_100_tock = [f"~/qmc-scripts/Plotting/H2OsymmetryTests/GVP_gs/LM-GVP-100-tock/h2onosym-gs-lm-gvp-100tock-{i}.out" for i in range(1, num_gs_lm_gvp_100_tock + 1)]
    # Formaldehyde
    # ~/qmc-runs/formaldehyde/Savio_SCRATCH_copy/formaldehyde/LM-GVP-100-tock-gs
    form_gs_files = [f"/home/connie/qmc-runs/formaldehyde/Savio_SCRATCH_copy/formaldehyde/LM-GVP-100-tock-gs/661-dets/formaldehyde-gs-{i}.out" for i in range(1, num_form_gs)]
    form_11b1_files = [f"/home/connie/qmc-runs/formaldehyde/Savio_SCRATCH_copy/formaldehyde/11B1/LM-GVP-100-tock/661-dets/formaldehyde-11B1-{i}.out" for i in range(1, num_form_11b1)]
    ###################
    # USER PARAMETERS #
    ###################

    # SET THIS VARIABLE to determine which files to plot
    # H2O
    # all_files = [tock_files_0, tock_files_2, tock_files_20, tock_files_200, tock_files_20_Jfirst, tock_files_200_Jfirst]
    # all_files = [tock_files_LM_GVPJ_0_tock, tock_files_LM_GVP_100_tock, tock_files_LM_GVPJ_100_tock]
    # all_files = [tock_files_LM_GVPJ_0_tock, tock_files_LM_GVP_100_tock, tock_files_LM_GVPJ_100_tock_2]
    # all_files = [tock_files_LM_GVP_100_tock, tock_files_gs_LM_GVP_100_tock]
    # formaldehdye
    all_files = [form_gs_files, form_11b1_files]
    # SET THIS VARIABLE Number of variables to plot for lderivs. There is one plot per variable.
    num_lderivs_plots = 0

    # Arrays to hold the resulting data
    all_energies = []
    all_variances = []
    all_target_functions = []
    all_lderivs = []
    all_qmc_timing = []
    all_total_timing = []

    # Read in the data
    for tock_files in all_files:
        read_files(tock_files, all_energies, all_variances, all_target_functions, all_lderivs, all_qmc_timing, all_total_timing)
    
    # Plot the data
    # NEW WAY
    plot_energies(all_energies)
    plot_variances(all_variances)
    plot_target_functions(all_target_functions)
    plot_lderivs(all_lderivs, num_lderivs_plots)
    plot_avg10(all_files, all_energies)
    # plot_timings(all_qmc_timing, all_total_timing)
    # OLD WAY
    # plot_variances(variances_0_tock, variances_2_tock, variances_20_tock, variances_200_tock, variances_20_tock_Jfirst, variances_200_tock_Jfirst)
    # plot_target_functions(target_functions_0_tock, target_functions_2_tock, target_functions_20_tock, target_functions_200_tock, target_functions_20_tock_Jfirst, target_functions_200_tock_Jfirst)
    # plot_lderivs(lderivs_0_tock, lderivs_2_tock, lderivs_20_tock, lderivs_200_tock, lderivs_20_tock_Jfirst, lderivs_200_tock_Jfirst, num_lderivs_plots)
    # plot_timings(qmc_timing_0_tock, qmc_timing_2_tock, qmc_timing_20_tock, qmc_timing_200_tock, qmc_timing_20_tock_Jfirst, qmc_timing_200_tock_Jfirst, total_timing_0_tock, total_timing_2_tock, total_timing_20_tock, total_timing_200_tock, total_timing_20_tock_Jfirst, total_timing_200_tock_Jfirst)
    plt.show()

if __name__ == "__main__":
    main()
