import sys
import csv
import powerlaw
import simulatorutils
import utils


def GetPathlengths(simulations):
    PathlengthXYZ = []

    pathlengthdata = utils.CalculateDistPerCellPerTimeStamp(simulations)

    for dataPoint in pathlengthdata:
        ID = dataPoint['track ID']
        path_ = dataPoint['DistXYZ']
        if(utils.IsFloat(path_)):
            if (float(path_) > 0):
                PathlengthXYZ.append(float(path_))
    data = sorted(PathlengthXYZ)
    return data


def Compile(filename, pausePattern='alternate'):
    Data = []
    muRunMax = 3
    muPauseMax = 3
    muRunCurrent = 1.1
    muPauseCurrent = 1.1

    while (muRunCurrent <= muRunMax):
        muPauseCurrent = 1.1
        while (muPauseCurrent <= muPauseMax):
            print('muRun: ' + str(muRunCurrent)
                  + ' muPause: ' + str(muPauseCurrent))

            simulated = simulatorutils.Simulate(
                100, 100, float(muRunCurrent), float(muPauseCurrent), 0.01, pausePattern)

            pathlengthdata = GetPathlengths(simulated)
            fit = powerlaw.Fit(pathlengthdata)
            mu = fit.power_law.alpha
            #Double check to make sure it isn't an artifact of simulation
            if (mu > 3):
                simulated = simulatorutils.Simulate(
                    100, 500, float(muRunCurrent), float(muPauseCurrent), 0.01, pausePattern)
                pathlengthdata = GetPathlengths(simulated)
                fit = powerlaw.Fit(pathlengthdata)
                mu = fit.power_law.alpha
            print(mu)
            Data.append(
                {'muRun': muRunCurrent, 'muPause': muPauseCurrent, 'fit': mu})
            muPauseCurrent += 0.1
        muRunCurrent += 0.1
    WriteCSVFromDict(filename, Data)


def WriteCSVFromDict(filename, data):
    fieldnames = ['muRun', 'muPause', 'fit']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()
        lastTime = 0

        for dataPoint in data:
            row = [dataPoint['muRun'],
                   dataPoint['muPause'], dataPoint['fit']]
            writer.writerow(row)


Compile(sys.argv[1])
