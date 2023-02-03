#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 17:02:05 2020

@author: nscho
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.offsetbox import AnchoredText
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

import sys
import os
sys.path.insert(0, os.path.join(os.environ['TOOLBOX_PATH'], 'python'))
import cfl

FS=20
MS=10
LW=4

DARK = 0 #dark layout?

if __name__ == "__main__":
    
    #Error if wrong number of parameters
    if( (len(sys.argv) < 4) or (1 == len(sys.argv)%2) ):
        print( "Files need to be passed in the cfl format and in pairs (see round brackets)!" )
        print( "Usage: plot_derivatives.py <savename> (<SA dR1> <finite dR1>) (<SA dR2> <finite dR2>) (<SA dB1> <finite dR1>)" )
        exit()
    
    sysargs = sys.argv

    filename = sysargs[1]

    # Import flexible number of files

    sa_data = []
    finite_data = []

    for i in range(2, len(sysargs), 2):

        print("Import file pair: "+sysargs[i]+", "+sysargs[i+1])

        # Information stored in imaginary part (due to definition of rotation in simulation)
        sa_data.append(np.imag(cfl.readcfl(sysargs[i]).squeeze()))

        finite_data.append(np.imag(cfl.readcfl(sysargs[i+1]).squeeze()))

    # Define data characteristics! Hard coded!
    para = ['$\partial M/\partial R_1$', '$\partial M/\partial R_2$', '$\partial M/\partial B_1$']

    """
    ------------------------------------
    ---------- Visualization -----------
    ------------------------------------
    """
    
    # plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    if(DARK):
        plt.style.use(['dark_background'])
    else:
        plt.style.use(['default'])
    
    
    fig = plt.figure(figsize=(10, 15), dpi=80, edgecolor='w')
    
    # Main Slice-Profile Visualization

    for f in range(0,len(sa_data)):

        ax1 = fig.add_subplot(3,1,f+1)

        ax1.plot(finite_data[f], '-', color='blue', alpha=1, linewidth=LW, label="$\\bf{DQ}$(h=1.00%)")
        ax1.plot(sa_data[f], '-', color='red', alpha=1, linewidth=LW, label="$\\bf{SAB}$")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
        ax1.yaxis.set_major_locator(plt.MaxNLocator(5))
        ax1.set_xlabel('Repetitions', fontsize=FS)
        ax1.set_ylabel(para[f], fontsize=FS)
        # ax1.legend(shadow=True, fancybox=True, loc='upper center', fontsize=FS-5)
        ax1.grid("on", color="black", alpha=.1, linewidth=.5)

        # Second y-axis
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'g'

        # Estimate maximal error
        max_error = np.max(np.abs(sa_data[f]-finite_data[f]))
        at = AnchoredText("x%.0f" % (1/max_error), loc='upper right', prop=dict(size=FS, color=color, weight='bold'), frameon=False)
        ax2.add_artist(at)

        ax2.plot(np.abs(sa_data[f]-finite_data[f])/max_error, '-', color=color, alpha=0.3, linewidth=LW, label="|$\\bf{DQ}-\\bf{SAB}$|")

        plt.xticks(fontsize=FS)
        plt.yticks(fontsize=FS)
        plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        # ax2.set_ylim(0,1E-3)
        # ax2.yaxis.get_offset_text().set_fontsize(FS)
        # ax2.yaxis.get_offset_text().set_weight('bold')
        ax2.locator_params(axis='y', nbins=5)
        ax2.set_ylabel('|$\\bf{DQ}-\\bf{SAB}$|', color=color, fontsize=FS)
        ax2.tick_params(axis='y', labelcolor=color)


        # ZOOM IN

        axin = ax1.inset_axes((.5,.45,.4,.2))

        # Plot num. diff. scaled to maximum value
        axin.plot(finite_data[f], '-', color='blue', alpha=1, linewidth=LW, label="$\\bf{DQ}$")
        axin.plot(sa_data[f], '-', color='red', alpha=1, linewidth=LW, label="$\\bf{SAB}$")

        x1, x2 = 810, 1010 # specify the limits
        y1 = np.min(np.array(sa_data[f][x1:x2]))*0.99
        y2 = np.max(np.array(sa_data[f][x1:x2]))*1.01

        axin.set_xlim(x1, x2) # apply the x-limits
        axin.set_ylim(y1, y2) # apply the y-limits
        axin.grid("on", color="black", alpha=.1, linewidth=.5)

        if (1 == f):
            mark_inset(ax1, axin, loc1=3, loc2=4, fc="none", ec="0.5")
        else:
            mark_inset(ax1, axin, loc1=1, loc2=2, fc="none", ec="0.5")
        
        # mark_inset(ax1, axin, loc1=3, loc2=4, fc="none", ec="0.5")

    # Add legend
    ax1Line, ax1Label = ax1.get_legend_handles_labels()
    ax2Line, ax2Label = ax2.get_legend_handles_labels()

    axLine = ax1Line + ax2Line
    axLabel = ax1Label + ax2Label
 
    fig.legend(axLine, axLabel, loc = 'lower center', bbox_to_anchor=(0.5, 0.98), fontsize=FS-5, fancybox=True, shadow=True, ncol=len(axLabel))


    plt.tight_layout(pad=5)
    # plt.show(block = False)

    fig.savefig(filename+".png", bbox_inches='tight', transparent=False)

