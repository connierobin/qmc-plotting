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
import json

gvp_energy = -17.216586028557398
gvp_error = 0.0004050886085250584
lm_energy = -17.2167068599006
lm_error = 0.0002927751345805431

fig, ax = plt.subplots()

# Set y axis format
ax.ticklabel_format(useOffset=False)

# Set x axis labels
x = np.array([0,1])
my_xticks = ['GVP', 'LM']
plt.xticks(x, my_xticks)

# Set axis limits
plt.ylim((-17.216,-17.2175))
plt.xlim((-0.5, 1.5))

# Plot GVP data
plt.axhline(y=gvp_energy, xmin=-0.5, xmax=0.5, color='r', linestyle='-')
gvp_x = np.array([-0.5, 0.5])
ax.fill_between(gvp_x, gvp_energy-gvp_error, gvp_energy+gvp_error, color='r', alpha=0.2)

# Plot LM data
plt.axhline(y=lm_energy, xmin=0.5, xmax=1.5, color='g', linestyle='-', alpha=0.2)
lm_x = np.array([0.5, 1.5])
ax.fill_between(lm_x, lm_energy-lm_error, lm_energy+lm_error, color='g', alpha=0.2)


plt.show()

