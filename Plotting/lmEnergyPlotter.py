#! /usr/bin/env python

import optparse
import os
import sys

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import math

def extract_data(data_files):


    #Strings the script looks for when scraping the qmcpack output file

#    variance = 'Crude block analysis of variance gives:'
   # variance = 'Crude block analysis of variance gives:     variance =       '
    variance = 'le_variance = '   
    uncertainty_of_variance = 'uncertainty ='
    data_start_str = 'Start QMCFixedSampleLinearOptimize'
    energy_str = '  le_mean =  '
    std_err_str = '  stat err =  '
    target_str = '  target function =  '
    target_err_str = '  target stat err = '
    std_dev_str = '  std dev =  '
    data_end_str = 'Solving the linear method equations'

    have_data = False
    variances = {}
    uncertainties_of_variances = {}
    energies = {}
    std_err = {}
    target_fn = {}
    target_std_err = {}
    std_dev = {}
    iteration = 0

    for data_file in data_files:
      f = open(data_file)

      for line in f:
          
          if data_start_str in line:
              have_data = True

          if have_data:
              #print(line)
              if energy_str in line:
                  values = line.split()
                  energies[iteration] = float(values[2])
              elif uncertainty_of_variance in line:
                  values = line.split()
                  uncertainties_of_variances[iteration] = float(values[2])
              elif variance in line:
              #    print(line)
                  values = line.split()
                  print(values)
                  variances[iteration] = float(values[2])
                  #variances[iteration] = float(values[8])
              elif std_err_str in line:
                  values = line.split()
                  std_err[iteration] = float(values[3])
              elif target_str in line:
                  values = line.split()
                  if 'N/A' in values[3]:
                    target_fn[iteration] = 0.0
                  else:
                    target_fn[iteration] = float(values[3])
              elif target_err_str in line:
                  values = line.split()
                  target_std_err[iteration] = float(values[4])
              elif std_dev_str in line:
                  values = line.split()
                  std_dev[iteration] = float(values[3])
              elif data_end_str in line:
                  have_data = False
                  iteration += 1

          if data_start_str in line:
              have_data = True

      f.close()

    return energies, std_err, target_fn, target_std_err, std_dev, variances, uncertainties_of_variances

def parse_options(args):
    '''Parse arguments and files from the command line.'''

    parser = optparse.OptionParser(usage = __doc__)
    (options, filenames) = parser.parse_args(args)
    
    if len(filenames) == 0:
        parser.print_help()
        sys.exit(1)

    return (options, filenames)

if __name__ == '__main__':

    (options, data_files) = parse_options(sys.argv[1:])

    energies, std_err, target_fn, target_std_err, std_dev, variances, uncertainties_of_variances = extract_data(data_files)

    # Print the header.
    sys.stdout.write(' #1._Iteration')
    column_text = '2._Energy'
    sys.stdout.write('%22s' % column_text)
    column_text = '3._Error'
    sys.stdout.write('%22s' % column_text)
    column_text = '4._Target_function'
    sys.stdout.write('%22s' % column_text)
    if len(target_std_err) > 0:
      column_text = '5._Target_error'
      sys.stdout.write('%22s' % column_text)
    column_text = '6._Standard_deviation'
    sys.stdout.write('%22s' % column_text)
    if len(variances) > 0:
      column_text = '7._Crude:_Variance'
      sys.stdout.write('%22s' % column_text)
      column_text = '8._Crude:_uncertainty_of_Variance'
      sys.stdout.write('%22s' % column_text)
    sys.stdout.write('\n')



    # Extract and print information for each iteration.
    for iter in energies:
        sys.stdout.write('     %9d' % iter)
        sys.stdout.write('   %19.12e' % energies[iter])
        sys.stdout.write('   %19.12e' % std_err[iter])
        sys.stdout.write('   %19.12e' % target_fn[iter])
        if len(target_std_err) > 0:
          sys.stdout.write('   %19.12e' % target_std_err[iter])
        sys.stdout.write('   %19.12e' % std_dev[iter])
        if len(variances) > 0:
          sys.stdout.write('   %19.12e' % variances[iter])
          #sys.stdout.write('   %19.12e' % uncertainties_of_variances[iter])
        sys.stdout.write('\n')


    energies = list(energies.values())
    errors = list(std_err.values())
    stdDevs = list(std_dev.values())
    variances = list(variances.values())
    uncertainties_of_var = list(uncertainties_of_variances.values())

   
    #I typically take averages over the last 10 linear method iterations for the values I report
    #as the result of optimization

    numIter1 = len(energies)

    print("Linear Method Energy")
    linE = np.mean(energies[numIter1-11:numIter1-1])
    print(linE)
    
    print("Energy Uncertainty")
    linErr = np.mean(errors[numIter1-11:numIter1-1])
    print(linErr)
    
    print("Variance")
    linVar = np.mean(variances[numIter1-11:numIter1-1])
    print(linVar)

    print("Variance Uncertainty")
    varErr = np.mean(uncertainties_of_var[numIter1-11:numIter1-1])
    print(varErr)

    print("Standard Deviation")
    linSD = np.mean(stdDevs[numIter1-11:numIter1-1])
    print(linSD)

    #Code below is for plotting the energy vs linear method iterations
    resultsStr = '$Linear \ Energy:%.5f \pm %.5f$'%(linE,linErr)
    props = dict(boxstyle='square',facecolor='white')

    iters1 = range(1,numIter1+1)

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.plot(iters1,energies,marker='o',label='adaptive three shift LM')
    
    #Often helpful to zoom in on converged part of optimization
    #ax.set_ylim(linE-.01,linE+.01)


    ax.text(.05,-.25,resultsStr,transform=ax.transAxes,horizontalalignment='left',bbox=props)
    plt.xlabel('Iteration Number', horizontalalignment='right')
    plt.ylabel('Local Energy')
    
    plt.title('Local Energy Values')
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    box = ax.get_position()
    ax.set_position([box.x0,box.y0+box.height*.15,box.width,box.height*.85])
    ax.legend(loc = 'upper center',bbox_to_anchor=(.85,-0.05))

    
    plt.show()


