import sys
from lmfit import Model, Parameters
import math
import numpy as np
import powerlaw
from scipy import stats
from scipy.stats import mannwhitneyu
from scipy.optimize import curve_fit
import utils


def Linear(x, m, b):
    return m*x+b


def PRW3D(t, S, P):
    return 3*((S)**2)*((P)**2)*(np.exp(-t/P) + t/P - 1)


def PRW2D(t, Sp, Pp, Snp, Pnp):
    return ((Sp)**2) * ((Pp)**2) * (np.exp(t/Pp) + t/Pp - 1) + ((Snp)**2) * ((Pnp)**2) * (np.exp(t/Pnp) + t/Pnp - 1)


def ModelPRW2D(TimeS_, MSD_):
    Model_ = Model(PRW2D)
    Params = Parameters()
    Params.add('Sp', 0.1, min=0.0)
    Params.add('Pp', 1, min=0.0)
    Params.add('Snp', 0.1, min=0.0)
    Params.add('Pnp', 1, min=0.0)

    Function = Model_.fit(MSD_, t=TimeS_, params=Params)
    return [Function.params['Sp'].value, Function.params['Pp'].value, Function.params['Snp'].value, Function.params['Pnp'].value]


def ModelPRW3D(TimeS_, MSD_):
    Model_ = Model(PRW3D)
    Params = Parameters()
    Params.add('S', 0.11)
    Params.add('P', 20)
#    Function = minimize(CohortGrapher.HuEtAlFunction, Params, args=(TimeS, MSD), method='leastsq')
    Function = Model_.fit(MSD_, t=TimeS_, params=Params)
    return [Function.params['S'].value, Function.params['P'].value, Function.best_fit, TimeS_]


def Histogram(data1, data2, ax, key, keysymbol, xlabel, data1label, data2label, bins, data3=None, data3label=None):
    List1 = []
    List2 = []
    List3 = []
    for dataPoint in data1:
        data_ = dataPoint[str(key)]
        if (utils.IsFloat(data_) and math.isnan(float(data_)) is False):
            List1.append(float(data_))
    for dataPoint in data2:
        data_ = dataPoint[str(key)]
        if (utils.IsFloat(data_) and math.isnan(float(data_)) is False):
            List2.append(float(data_))
    if ('Toxoplasma' in data1label and key is 'VelXYZ'):
        ax.hist(List1, density=True, bins=100, edgecolor='black', histtype=u'step', label=data1label
                + '\n(n=' + str(len(List1)) + r', ' + keysymbol + '=' + '{:.3g}'.format(sum(List1)/len(List1)) + ')')
    else:
        ax.hist(List1, density=True, bins=bins, edgecolor='black', histtype=u'step', label=data1label
                + '\n(n=' + str(len(List1)) + r', ' + keysymbol + '=' + '{:.3g}'.format(sum(List1)/len(List1)) + ')')
    ax.hist(List2, density=True, bins=bins, edgecolor='red',
            histtype=u'step', linestyle='--', label=str(data2label) + str('\n(n=') + str(len(List2)) + r', ' + keysymbol + '=' + '{:.3g}'.format(sum(List2)/len(List2)) + ')')
    if (data3 == None):
        ax.hist([], color='white', label='p='
                + '{:.3g}'.format(mannwhitneyu(List1, List2)[1]))
    else:
        for dataPoint in data3:
            data_ = dataPoint[str(key)]
            if (utils.IsFloat(data_) and math.isnan(float(data_)) is False):
                List3.append(float(data_))
        ax.hist(List3, density=True, bins=bins, edgecolor='blue',
                histtype=u'step', linestyle='--', label=str(data3label) + str('\n(n=') + str(len(List3)) + r', ' + keysymbol + '=' + '{:.3g}'.format(sum(List3)/len(List3)) + ')')
    ax.legend()
    ax.set_ylabel('Frequency')
    ax.set_xlabel(xlabel)
    #ax.set_xlabel(r'Average velocity per track $\bar{v}$, μm/min')


def InstantaneousVelocityHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'VelXYZ'
    if XYZ is False:
        key = 'VelXY'
    Histogram(data1, data2, ax, key, r'$\bar{v}$',
              r'Instantaneous velocity v, μm/min', label1, label2, bins, data3, label3)
    ax.set_xlim(left=0)


def AvgVelocityHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AvgVelXYZ'
    if XYZ is False:
        key = 'AvgVelXY'
    Histogram(data1, data2, ax, key, r'$\bar{v}$',
              r'Average velocity per track $\bar{v}$, μm/min', label1, label2, bins, data3, label3)
    ax.set_xlim(left=0)


def InstantaneousTurningAngleHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AngleXYZ'
    if XYZ is False:
        key = 'AngleXY'
    Histogram(data1, data2, ax, key, r'$\bar{\theta}$',
              r'Instantaneous turning angle $\theta$, degrees', label1, label2, bins, data3, label3)
    angleticks = [0, 45, 90, 135, 180]
    ax.set_xticks(angleticks)
    ax.set_xlim(0, 180)


def AvgTurningAngleHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AvgAngleXYZ'
    if XYZ is False:
        key = 'AvgAngleXY'
    Histogram(data1, data2, ax, key, r'$\bar{\theta}$',
              r'Average turning angle per track $\bar{\theta}$, degrees', label1, label2, bins, data3, label3)
    angleticks = [0, 45, 90, 135, 180]
    ax.set_xticks(angleticks)
    ax.set_xlim(0, 180)


def InstantaneousAccelerationHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AccelXYZ'
    if XYZ is False:
        key = 'AccelXY'
    Histogram(data1, data2, ax, key, r'$\bar{a}$',
              r'Instantaneous acceleration a, μm/$min^2$', label1, label2, bins, data3, label3)
    ax.set_xlim(left=0)


def AvgAccelerationHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AvgAccelXYZ'
    if XYZ is False:
        key = 'AvgAccelXY'
    Histogram(data1, data2, ax, key, r'$\bar{a}$',
              r'Average acceleration per track $\bar{a}$, μm/$min^2$', label1, label2, bins, data3, label3)
    ax.set_xlim(left=0)


def InstantaneousAngleAccelHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AngleAccelXYZ'
    if XYZ is False:
        key = 'AngleAccelXY'
    Histogram(data1, data2, ax, key, r'$\bar{\theta}$',
              r'Instantaneous angle of acceleration $\theta$, degrees', label1, label2, bins, data3, label3)
    angleticks = [0, 45, 90, 135, 180]
    ax.set_xticks(angleticks)
    ax.set_xlim(0, 180)


def AvgAngleAccelHistogram(data1, data2, ax, label1, label2, XYZ=True, bins=15, data3=None, label3=None):
    key = 'AvgAngleAccelXYZ'
    if XYZ is False:
        key = 'AvgAngleAccelXY'
    Histogram(data1, data2, ax, key, r'$\bar{\theta}$',
              r'Average angle of acceleration per track $\theta$, degrees', label1, label2, bins, data3, label3)
    angleticks = [0, 45, 90, 135, 180]
    ax.set_xticks(angleticks)
    ax.set_xlim(0, 180)


def MeanderingIndexHistogram(data1, data2, ax, label1, label2, XYZ=True):
    key = 'meanderingIndexXYZ'
    if XYZ is False:
        key = 'meanderingIndexXY'
    Histogram(data1, data2, ax, key, r'Mean',
              r'Meandering index', label1, label2, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    ax.set_xlim(0, 1)
    ax.legend(loc='upper left')


def ArrestCoefficientHistogram(data1, data2, ax, label1, label2, XYZ=True):
    key = 'arrestCoefficientXYZ'
    if XYZ is False:
        key = 'arrestCoefficientXY'
    Histogram(data1, data2, ax, key, r'Mean',
              r'Arrest coefficient', label1, label2, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    ax.set_xlim(0, 1)


def PlotCorrelation(data, ax, key1, key1symbol, key1label, key2, key2symbol, key2label, populationlabel, color='red'):
    key1List = []
    key2List = []
    for dataPoint in data:
        key1_ = dataPoint[str(key1)]
        key2_ = dataPoint[str(key2)]
        if(utils.IsFloat(key1_) and math.isnan(float(key1_)) is False and utils.IsFloat(key2_) and math.isnan(float(key2_)) is False):
            key1List.append(float(key1_))
            key2List.append(float(key2_))
    fit = curve_fit(Linear, key1List, key2List)[0]
    spearmanr = stats.spearmanr(key1List, key2List)
    x = np.linspace(0.1, float(max(key1List)), 600)
    y = Linear(x, fit[0], fit[1])
    ax.plot(x, y, color=color)
    ax.scatter(key1List, key2List, marker="o", color='none', edgecolor=color, label=populationlabel + '\n' + key2symbol + '=' + str(
        round(sum(key2List)/len(key2List), 2)) + r', ' + key1symbol + '=' + str(round(sum(key1List)/len(key1List), 2)) + '\n' + r'm='
                + str(round(fit[0], 5)) + r', $\rho$=' + str(round(spearmanr[0], 2)))
    angleticks = [0, 45, 90, 135, 180]
    if ('AngleXYZ' is key1 or 'AvgAngleXYZ' is key1 or 'AngleXY' is key1 or 'AvgAngleXY' is key1):
        ax.set_xlim(0, 180)
        ax.set_xticks(angleticks)
    if ('AngleXYZ' is key2 or 'AvgAngleXYZ' is key2 or 'AngleXY' is key2 or 'AvgAngleXY' is key2):
        ax.set_ylim(0, 180)
        ax.set_yticks(angleticks)
    #ax.set_xscale('log')
    #ax.set_xlim(0, 250)
    #ax.set_ylim(0, 50)
#    ax.set_xlim(0.01, 100)
    ax.set_xlabel(key1label)
    ax.set_ylabel(key2label)
    #ax.set_xlabel(r'Mean acceleration per cell $\bar{a}$, (μm/$min^2$)')
    #ax.set_ylabel(r'Mean velocity per cell $\bar{v}$, (μm/min)')
    ax.legend()


def CDF(data, ax, xlabel, key, label, color, linestyle, marker):
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    Ids = []
    Values = []
    HistXYZ = []
    cleaned = False
    for dataPoint in data:
        value = dataPoint[str(key)]
        ID = dataPoint['track ID']
        if(utils.IsFloat(value)):
            if (float(value) > 0):
                Values.append(float(value))

                if(str(ID) not in Ids):
                    Ids.append(str(ID))

    data = sorted(Values)
    cutoff = 100
    if (data[-1] < 100):
        #To make sure no bins have no values and the last bin includes the maximum
        cutoff = data[-2]
    data_size = len(data)

    #Set bins edges
    data_set = sorted(set(data))
    bins = np.append(data_set, data_set[-1] + 1)

    #Find CDF
    counts, bin_edges = np.histogram(data, bins=np.logspace(
        np.log10(0.01), np.log10(cutoff), 25), density=False)
    counts = counts.astype(float)/data_size
    cdf = np.cumsum(counts)

    #Tail Analysis
    fit = powerlaw.Fit(data, fit_method='KS')

    #It looks like the package and pareto have different definitions of mu/alpha. We do not add 1 in this case.
    mu = float(fit.power_law.alpha)
    ax.axvline(x=float(fit.power_law.xmin),
               linestyle=linestyle, color=color)
    bintail = 5
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
    fit_ = curve_fit(Linear, np.log10(
        bin_centers[-bintail:]), np.log10(1-cdf[-bintail:]))[0]
    x2 = np.linspace(bin_centers[-bintail], bin_centers[-1], 100)
    y2 = (10 ** float(fit_[1])) * ((x2) ** float(fit_[0]))
#    ax.plot(x2, y2)
    label_ = label + '\n($n_d$=' + str(len([i for i in Values if i >= fit.power_law.xmin])) + ', μ=' + str(
        round(mu, 2)) + ', $r_{min}$=' + str(round(fit.power_law.xmin, 2)) + ')'

    ax.plot(bin_edges[0:-1], 1-cdf,
            marker=marker, color=color, label=label_, linestyle=linestyle)
    #fit.power_law.plot_ccdf(color=color, linestyle='-.', ax=ax)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim((0.00001, 1.1))
    ax.set_xlim(0.01, 100)
    ax.set_xlabel(xlabel, wrap=True)
    ax.set_ylabel('P(x>r)', wrap=True)
    ax.legend()


def GraphCDF(ax, data1, data2, label1, label2, xlabel, key):
    CDF(data1, ax, xlabel, key, label1, 'black', 'dashed', 'x')
    CDF(data2, ax, xlabel, key, label2, 'red', 'dotted', '+')
    #ax.hist([], color='white', label='p='
    #        + '{:.3g}'.format(ks_2samp((i[str(key)] for i in data1), (i[str(key)] for i in data2))))


def GraphRminRelationship(data, ax, label):
    Ids = []
    PathlengthXYZ = []
    HistXYZ = []
    cleaned = False
    Xmins = []
    Mus = []
    SampleSizes = []
    TableData = []
    for dataPoint in data:
        ID = dataPoint['track ID']
        path_ = dataPoint['DistXYZ']
        if(utils.IsFloat(path_)):
            if (float(path_) > 0):
                PathlengthXYZ.append(float(path_))

                if(str(ID) not in Ids):
                    Ids.append(str(ID))
    data = sorted(PathlengthXYZ)
    #Set bins edges
    data_set = sorted(set(data))
    bins = np.append(data_set, data_set[-1] + 1)

    #Find CDF
    cutoff = 100
    counts, bin_edges = np.histogram(data, bins=np.logspace(
        np.log10(0.01), np.log10(cutoff), 25), density=False)
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
    currentxmin = 0
    while (float(currentxmin) < float(bin_edges[-1])):
        samplesize = len([i for i in data if i >= float(currentxmin)])
        if (samplesize < 3):
            break
        Xmins.append(currentxmin)
        mu = powerlaw.Fit(data, xmin=float(currentxmin)).power_law.alpha + 1
        Mus.append(mu)
        samplesize = len([i for i in data if i >= float(currentxmin)])
        SampleSizes.append(float(samplesize))
        TableData.append([currentxmin, mu, samplesize])
        currentxmin += 0.5

    color = 'tab:red'
    ax.set_xlabel(
        'Minimum value of scaling \nrelationship $r_{min}$, μm', wrap=True, fontsize=16)
    ax.set_xlim(0.01, 100)
    ax.set_xscale('log')
    ax.set_ylabel('Pareto distribution \nshape parameter μ',
                  wrap=True, fontsize=16)
    ax.set_ylim(0, 10)
    ax.plot(Xmins, Mus, color=color, marker='o')
    ax.tick_params(axis='y', labelcolor=color)

    fit = powerlaw.Fit(data)
    if(cleaned):
        ax.text(10*10**-2.95, 5, label + '\n $n_t$=' + str(len(Ids)) + ' cleaned' + " \n $n_d$=" + str(len(PathlengthXYZ)) + ' \n μ='
                + str(round(fit.power_law.alpha-1, 2)) + ' $r_{min}$=' + str(round(fit.power_law.xmin, 2)) + ' μm', fontsize=16)
    else:
        ax.text(10*10**-2.95, 5, label + '\n $n_t$=' + str(len(Ids)) + ' uncleaned' + " \n $n_d$=" + str(len(PathlengthXYZ))
                + ' \n μ=' + str(round(fit.power_law.alpha-1, 2)) + ' $r_{min}$=' + str(round(fit.power_law.xmin, 2)) + ' μm', fontsize=16)
    ax.axvline(x=float(fit.power_law.xmin), linestyle='--', color='black')
    ax.axhline(y=3, linestyle='--', color=color)
    ax2 = ax.twinx()
    color = 'tab:blue'
    ax2.set_ylabel(
        'Number of movement \nlengths $n_d$, displacements', wrap=True, fontsize=16)
    ax2.set_yscale('log')
    ax2.set_ylim(1, 10**5)
    ax.set_ylim(0, 15)
    ax2.plot(Xmins, SampleSizes, color=color, marker='x')
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=15)


def GraphMSD(data, marker, color, axis1, label, XYZ=True):
    axis1.set_xscale('log')
    axis1.set_yscale('log')
    axis1.set_xlabel('Time t, min')
    axis1.set_ylabel('Mean square\ndisplacement, $μm^2$')
    key = 'MSDXYZ'
    if(XYZ is False):
        key = 'MSDXY'

    GammaTime = 3 * 60
    PRWTime = 5 * 60
    Time = []
    TimeS = []
    TimeMin = []
    MSD = []
    MSDGamma = []
    MSDHu = []
    Vmean = 0
    Gamma = []
    Cells = 0
    PRW = []

    for dataPoint in data:
        time_ = dataPoint['time (s)']
        msd_ = dataPoint[str(key)]
        if(utils.IsFloat(time_) and utils.IsFloat(msd_)):
            if (float(time_) > 0):
                if (Cells == 0):
                    Cells = int(dataPoint['Cells'])
                #Added 2 to account for some offset times, probably could add much less though but this won't do any harm
                if (float(time_) < (float(GammaTime) + 2)):
                    TimeS.append(float(time_))
                    MSDGamma.append(float(msd_))
                if (float(time_) < (float(PRWTime) + 2)):
                    TimeMin.append(float(time_)/60)
                    MSDHu.append(float(msd_))
                Time.append(float(time_)/60)
                MSD.append(float(msd_))

    Gamma = curve_fit(Linear, np.log10(TimeS[1:]), np.log10(MSDGamma[1:]))[0]
    #PRW = ModelPRW3D(TimeMin[1:], MSDHu[1:])
    #PRW2D = ModelPRW2D(TimeMin[1:], MSDHu[1:])

    x = np.linspace(0.1, float(GammaTime)/60, 600)
    y = (10 ** float(Gamma[1])) * ((x * 60) ** float(Gamma[0]))

    Hux = np.linspace(0.1, float(PRWTime)/60, 600)
    n = 0

    if (XYZ == True):
        n = 3
    else:
        n = 2
    #HuY2D = PRWFunction2D(
    #    60*Hux, PRW2D[0], PRW2D[1], PRW2D[2], PRW2D[3])
    #HuY = PRWFunction3D(60*Hux, PRW[0], PRW[1])
    label_ = label + ' (n=' + str(Cells) + ', γ = ' + \
        str(round(Gamma[0], 4)) + ')'
    axis1.scatter(Time, MSD, marker=marker, color=color,
                  edgecolor=color, label=label_)
    #axis1.plot(Hux, HuY, linestyle='dotted', color=color)
    axis1.set_ylim(bottom=1)
    axis1.plot(x, y, linestyle='dashed', color=color)
    axis1.legend(loc='lower right')


def TimeDiffHistogram(data, axis, interval, label):
    TimeDiff = []
    prevID = -1
    prevTime = -1
    timegaps = 0

    for dataPoint in data:
        trackID = dataPoint['track ID']
        time = dataPoint['time (s)']
        if (trackID == prevID and utils.IsFloat(time) and utils.IsFloat(prevTime)):
            timeDiff = float(time) - float(prevTime)
            TimeDiff.append(float(timeDiff))
            if (float(timeDiff) > interval + 3):
                timegaps += 1
        prevTime = time
        prevID = trackID
    #axis.plot([], [], ' ', 'n=' + str(len(TimeDiff)))
    axis.set_xticks(np.arange(0, max(TimeDiff)+1, float(interval*2)))
    axis.set_xlabel('Time between movements Δt, s')
    axis.set_ylabel('Number of\nMovements')
    axis.set_yscale('log')
    axis.hist(TimeDiff, bins=25, edgecolor='black', histtype=u'step',
              linestyle='--', label=label + '\n($n_d$=' + str(len(TimeDiff)) + ' $n_{gaps}$=' + str(timegaps) + ')')
    axis.legend()
