import sys
import graph
import graphutils
import matplotlib.pyplot as plt
import utils


def Characteristics(filename1, label1, filename2, label2):
    data1, celldata1, timedata1 = utils.LoadAllData(filename1)
    data2, celldata2, timedata2 = utils.LoadAllData(filename2)

    legendsize = 12
    fontsize = 18
    majorticksize = 5
    plt.rcParams.update({'font.size': legendsize, 'axes.titlesize': fontsize,
                         'axes.labelsize': fontsize, 'xtick.labelsize': fontsize, 'ytick.labelsize': fontsize, 'lines.markersize': 15})
    figure, axis = graph.Characterization(data1, data2, celldata1, celldata2,
                                          timedata1, timedata2, label1, label2)
    plt.savefig('characterization.pdf')
    plt.show()

    graph.ResetGraphs()
    Fits = []
    Fits.append(utils.FitDistribution(data1,
                                      label1))
    Fits.append(utils.FitDistribution(data2,
                                      label2))
    graph.Table(Fits)


Characteristics(sys.argv[1], sys.argv[2], sys.argv[3],
                sys.argv[4])
