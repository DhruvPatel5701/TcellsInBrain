import sys
import graphutils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utils


def ResetGraphs():
    plt.clf()
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 18,
                         'axes.labelsize': 18, 'xtick.labelsize': 18, 'ytick.labelsize': 18, 'lines.markersize': 15})


def Table(Fits):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    df = pd.DataFrame(Fits, columns=[
            'Cell population', 'Shape, k', r'Location, $\theta$', r'Scale, $\sigma$', 'Mean', 'Variance'])

    table = ax.table(cellText=df.values,
                     colLabels=df.columns, loc='center')
    ax.set_title('Pathlength Distribution fit to Generalized Pareto',
                 fontsize=18, fontweight='bold', y=1.1)
    table.auto_set_font_size(False)
    table.auto_set_column_width(
            col=['Cell population', 'Shape', 'Location', 'Scale', 'Mean', 'Variance'])
    table.scale(1, 2)
    table.set_fontsize(16)
    fig.tight_layout()

    fig.set_size_inches((20, 11), forward=False)
    fig.savefig('GPTable.pdf', format='pdf', dpi=500)


def Basic(data1, data2, label1, label2):
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 18,
                         'axes.labelsize': 18, 'xtick.labelsize': 18, 'ytick.labelsize': 18, 'lines.markersize': 15})
    figure, axis = plt.subplots(2, 1, figsize=(9, 8))
    plt.subplots_adjust(wspace=0.2, hspace=0.3)
    graphutils.MeanderingIndexHistogram(data1, data2, axis[0], label1, label2)
    graphutils.ArrestCoefficientHistogram(
        data1, data2, axis[1], label1, label2)
    return figure, axis


def Characterization(data1, data2, celldata1, celldata2, timedata1, timedata2, label1, label2):
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 18,
                         'axes.labelsize': 18, 'xtick.labelsize': 18, 'ytick.labelsize': 18, 'lines.markersize': 15, 'lines.linewidth': 3})
    figure, axis = plt.subplots(3, 2, figsize=(15, 15))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    axis[0, 0].text(-0.2, 1.15, 'A', transform=axis[0, 0].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    axis[0, 1].text(-0.2, 1.15, 'B', transform=axis[0, 1].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    axis[1, 0].text(-0.2, 1.15, 'C', transform=axis[1, 0].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    axis[1, 1].text(-0.2, 1.15, 'D', transform=axis[1, 1].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    axis[2, 0].text(-0.2, 1.15, 'E', transform=axis[2, 0].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    axis[2, 1].text(-0.2, 1.15, 'F', transform=axis[2, 1].transAxes,
                    fontsize=16, fontweight='bold', va='top', ha='right')
    controlx = np.linspace(0.1, 3, 600)
    controly = (10 ** float(1)) * ((controlx * 60) ** float(1))
    axis[0, 0].plot(controlx, controly, linestyle='--',
                    label='γ = 1', color='green')
    graphutils.GraphMSD(timedata1, 'x', 'black', axis[0, 0], label1)
    graphutils.GraphMSD(timedata2, '+', 'red', axis[0, 0], label2)
    graphutils.GraphCDF(
        axis[0, 1], data1, data2, label1, label2, 'Movement length r, μm', 'DisplacementXYZ')
    graphutils.InstantaneousVelocityHistogram(
        data1, data2, axis[1, 0], label1, label2)
    graphutils.InstantaneousTurningAngleHistogram(
        data1, data2, axis[1, 1], label1, label2)
    graphutils.AvgVelocityHistogram(
        celldata1, celldata2, axis[2, 0], label1, label2)
    graphutils.AvgTurningAngleHistogram(
        celldata1, celldata2, axis[2, 1], label1, label2)
    axis[0, 0].legend(fontsize=10)
    axis[0, 1].legend(fontsize=9)
    return figure, axis


def ProduceGraphs(filename1, label1, filename2, label2, outputfilename):
    data1 = utils.ReadDataFromFile(filename1)
    data2 = utils.ReadDataFromFile(filename2)

    celldatafile1 = filename1.replace('cleaned', 'celldata')
    celldatafile2 = filename2.replace('cleaned', 'celldata')
    celldata1 = utils.ReadDataFromFile(celldatafile1)
    celldata2 = utils.ReadDataFromFile(celldatafile2)

    timedatafile1 = filename1.replace('cleaned', 'timedata')
    timedatafile2 = filename2.replace('cleaned', 'timedata')
    timedata1 = utils.ReadDataFromFile(timedatafile1)
    timedata2 = utils.ReadDataFromFile(timedatafile2)

    Basic(celldata1, celldata2, label1, label2)
    plt.savefig(outputfilename.replace('.csv', 'basic.pdf'), format='pdf')
    plt.show()
    ResetGraphs()

    Characterization(data1, data2, celldata1, celldata2,
                     timedata1, timedata2, label1, label2)
    plt.savefig(outputfilename.replace(
        '.csv', 'characterization.pdf'), format='pdf')
    plt.show()
    ResetGraphs()


if (len(sys.argv) > 5):
    ProduceGraphs(sys.argv[1], sys.argv[2],
                  sys.argv[3], sys.argv[4], sys.argv[5])
