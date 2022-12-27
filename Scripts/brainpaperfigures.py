import utils
import csv
import matplotlib.pyplot as plt
from scipy.stats import genpareto
import graphutils
import graph
import pandas as pd


def FitDistribution(data, label):
    PathlengthXYZ = []
    Ids = []
    for dataPoint in data:
        ID = dataPoint['track ID']
        path_ = dataPoint['DisplacementXYZ']
        if(utils.IsFloat(path_)):
            if (float(path_) > 0):
                PathlengthXYZ.append(float(path_))
                if(str(ID) not in Ids):
                    Ids.append(str(ID))

    b, loc, scale = genpareto.fit(PathlengthXYZ)
    mean, var = genpareto.stats(
        b, loc=loc, scale=scale, moments='mv')
    b = round(float(b), 2)
    loc = round(float(loc), 2)
    scale = round(float(scale), 2)
    mean = round(float(mean), 2)
    var = round(float(var), 2)
    return [label, b, loc, scale, mean, var]


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
    fig.savefig('BrainPaperSuppFig4.pdf', format='pdf', dpi=500)


def ProduceGraphs():
    harrislabel = 'Toxoplasma-specific\nCD8 T cells'
    heathcd4label = 'Plasmodium-specific\nCD4 T cells'
    heathcd8label = 'Plasmodium-specific\nCD8 T cells'
    heathcd465label = 'CD4 T cells after 6.5 days'
    heathcd47label = 'CD4 T cells after 7 days'
    heathcd865label = 'CD8 T cells after 6.5 days'
    heathcd87label = 'CD8 T cells after 7 days'

    harrisdata, harriscelldata, harristimedata = utils.LoadAllData(
        'BrainPaper/Harris/Analysis/20/harrisdata20cleaned.csv')

    heathcd4data, heathcd4celldata, heathcd4timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD4/Analysis/30/heathdatacd4cleaned.csv')

    heathcd8data, heathcd8celldata, heathcd8timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD8/Analysis/30/heathdatacd8cleaned.csv')

    heathcd465data, heathcd465celldata, heathcd465timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD4/Analysis/6.5d/30/heathdata6.5cd4cleaned.csv')

    heathcd47data, heathcd47celldata, heathcd47timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD4/Analysis/7d/30/heathdata7cd4cleaned.csv')

    heathcd865data, heathcd865celldata, heathcd865timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD8/Analysis/6.5d/30/heathdata6.5cd8cleaned.csv')

    heathcd87data, heathcd87celldata, heathcd87timedata = utils.LoadAllData(
        'BrainPaper/HeathLabCD8/Analysis/7d/30/heathdata7cd8cleaned.csv')

    simulatedbrowniandata, simulatedbrowniancelldata, simulatedbrowniantimedata = utils.LoadAllData(
        'BrainPaper/Simulations/Brownian/simulatedbrowniancleaned.csv')
    simulatedcrwdata, simulatedcrwcelldata, simulatedcrwtimedata = utils.LoadAllData(
        'BrainPaper/Simulations/CRW/simulatedcrwcleaned.csv')
    simulatedlevydata, simulatedlevycelldata, simulatedlevytimedata = utils.LoadAllData(
        'BrainPaper/Simulations/Levy/simulatedlevycleaned.csv')
    simulatedgenlevydata, simulatedgenlevycelldata, simulatedgenlevytimedata = utils.LoadAllData(
        'BrainPaper/Simulations/GenLevy/simulatedgenlevycleaned.csv')
    simulatedbulletdata, simulatedbulletcelldata, simulatedbullettimedata = utils.LoadAllData(
        'BrainPaper/Simulations/Bullet/simulatedbulletcleaned.csv')
    graph.Basic(heathcd4celldata, heathcd8celldata,
                heathcd4label, heathcd8label)
    plt.savefig('BrainPaperFig2.pdf', format='pdf')
    graph.ResetGraphs()

    figure, axis = graph.Characterization(heathcd4data, heathcd8data, heathcd4celldata, heathcd8celldata,
                                          heathcd4timedata, heathcd8timedata, heathcd4label, heathcd8label)
    axis[1, 0].set_xlim(0, 60)
    axis[1, 1].set_ylim(0, 0.02)
    axis[2, 0].set_xlim(0, 60)
    axis[2, 1].set_ylim(0, 0.02)
    plt.savefig('BrainPaperFig3.pdf', format='pdf')
    graph.ResetGraphs()

    figure, axis = graph.Characterization(harrisdata, heathcd8data, harriscelldata, heathcd8celldata,
                                          harristimedata, heathcd8timedata, harrislabel, heathcd8label)
    axis[1, 0].set_xlim(0, 60)
    axis[1, 1].set_ylim(0, 0.02)
    axis[2, 0].set_xlim(0, 60)
    axis[2, 1].set_ylim(0, 0.02)
    plt.savefig('BrainPaperFig4.pdf', format='pdf')
    graph.ResetGraphs()

    figure, axis = graph.Characterization(heathcd465data, heathcd47data, heathcd465celldata, heathcd47celldata,
                                          heathcd465timedata, heathcd47timedata, heathcd465label, heathcd47label)
    axis[1, 0].set_xlim(0, 60)
    axis[1, 1].set_ylim(0, 0.02)
    axis[2, 0].set_xlim(0, 60)
    axis[2, 1].set_ylim(0, 0.02)
    plt.savefig('BrainPaperSuppFig1.pdf', format='pdf')
    graph.ResetGraphs()

    figure, axis = graph.Characterization(heathcd865data, heathcd87data, heathcd865celldata, heathcd87celldata,
                                          heathcd865timedata, heathcd87timedata, heathcd865label, heathcd87label)
    axis[1, 0].set_xlim(0, 60)
    axis[1, 1].set_ylim(0, 0.02)
    axis[2, 0].set_xlim(0, 60)
    axis[2, 1].set_ylim(0, 0.02)
    plt.savefig('BrainPaperSuppFig2.pdf', format='pdf')
    graph.ResetGraphs()
    Fits = []
    Fits.append(FitDistribution(
        heathcd4data, 'All Plasmodium-specific\nCD4 T cells'))
    Fits.append(FitDistribution(
        heathcd8data, 'All Plasmodium-specific\nCD8 T cells'))
    Fits.append(FitDistribution(heathcd465data,
                                'Plasmodium-specific\nCD4 T cells at 6.5 days'))
    Fits.append(FitDistribution(heathcd47data,
                                'Plasmodium-specific\nCD4 T cells at 7 days'))
    Fits.append(FitDistribution(heathcd865data,
                                'Plasmodium-specific\nCD8 T cells at 6.5 days'))
    Fits.append(FitDistribution(heathcd87data,
                                'Plasmodium-specific\nCD8 T cells at 7 days'))
    Fits.append(FitDistribution(
        harrisdata, 'All Toxoplasma-specific\nCD8 T cells'))
    Fits.append(FitDistribution(
        simulatedbrowniandata, 'Simulated Brownian\nwalkers'))
    Fits.append(FitDistribution(
        simulatedbrowniandata, 'Simulated CRW walkers'))
    Fits.append(FitDistribution(
        simulatedlevydata, 'Simulated Levy walkers'))
    Fits.append(FitDistribution(simulatedgenlevydata,
                'Simulated Generalized\nLevy walkers'))
    Fits.append(FitDistribution(simulatedbulletdata,
                'Simulated Bullet\nmotion walkers'))
    Table(Fits)


ProduceGraphs()
