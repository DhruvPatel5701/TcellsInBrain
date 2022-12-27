import sys
from collections import defaultdict
import csv
import utils


def CompileData(filename, interval):
    uncleaneddata = utils.ReadDataFromFile(filename)
    cleaneddata = utils.Clean(uncleaneddata, interval)
    datawithvel = utils.CalculateVelocity(cleaneddata)
    completedata = utils.CalculateAcceleration(datawithvel)
    percelldata = ComputeCellCharacteristics(completedata)
    timedata = ComputePopulationOverTimeCharacteristics(completedata, interval)
    WriteCSVFromCompleteData(filename.replace(
        '.csv', 'cleaned.csv'), completedata, interval)
    WriteCSVFromPerCellData(filename.replace(
        '.csv', 'celldata.csv'), percelldata, interval)
    WriteCSVFromTimeData(filename.replace(
        '.csv', 'timedata.csv'), timedata)


def WriteCSVFromCompleteData(filename, data, interval):
    fieldnames = ['movie',
                  'old track ID', 'original time (s)', 'old time (s)', 'track ID', 'time (s)', 'x', 'y', 'z', 'TimeDiff', 'DisplacementXYZ', 'VelXYZ', 'AngleXYZ', 'AccelXYZ', 'AngleAccelXYZ', 'DisplacementXY', 'VelXY', 'AngleXY', 'AccelXY', 'AngleAccelXY']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()

        for dataPoint in data:
            movie = 'N/A'
            try:
                movie = dataPoint['movie']
            except:
                'N/A'
            time = dataPoint['time (s)']
            originaltime = 'N/A'
            try:
                originaltime = dataPoint['original time (s)']
            except:
                originaltime = 'N/A'
            if (utils.IsString(movie) is False):
                movie = 'N/A'
            if (utils.IsFloat(originaltime) is False):
                originaltime = 'N/A'
            if (utils.IsFloat(time)):
                row = [movie, dataPoint['old track ID'], originaltime, dataPoint['old time (s)'], str(interval) + '.' + str(
                    dataPoint['track ID']), time, dataPoint['x'], dataPoint['y'], dataPoint['z'], dataPoint['TimeDiff'], dataPoint['DisplacementXYZ'], dataPoint['VelXYZ'], dataPoint['AngleXYZ'], dataPoint['AccelXYZ'], dataPoint['AngleAccelXYZ'], dataPoint['DisplacementXY'], dataPoint['VelXY'], dataPoint['AngleXY'], dataPoint['AccelXY'], dataPoint['AngleAccelXY']]
                writer.writerow(row)


def WriteCSVFromPerCellData(filename, data, interval):
    fieldnames = ['track ID', 'AvgVelXYZ', 'AvgAngleXYZ', 'AvgAccelXYZ', 'AvgAngleAccelXYZ', 'meanderingIndexXYZ',
                  'arrestCoefficientXYZ', 'AvgVelXY', 'AvgAngleXY', 'AvgAccelXY', 'AvgAngleAccelXY', 'meanderingIndexXY', 'arrestCoefficientXY', 'VelXYZStDev', 'VelXYZCV', 'AngleXYZStDev', 'AngleXYZCV', 'VelXYStDev', 'VelXYCV', 'AngleXYStDev', 'AngleXYCV']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()

        for dataPoint in data:
            trackID = dataPoint['track ID']
            if (utils.IsString(trackID)):
                row = [str(interval) + '.' + str(trackID), dataPoint['AvgVelXYZ'], dataPoint['AvgAngleXYZ'], dataPoint['AvgAccelXYZ'], dataPoint['AvgAngleAccelXYZ'], dataPoint['meanderingIndexXYZ'],
                       dataPoint['arrestCoefficientXYZ'], dataPoint['AvgVelXY'], dataPoint['AvgAngleXY'], dataPoint['AvgAccelXY'], dataPoint['AvgAngleAccelXY'], dataPoint['meanderingIndexXY'], dataPoint['arrestCoefficientXY'], dataPoint['VelXYZStDev'], dataPoint['VelXYZCV'], dataPoint['AngleXYZStDev'], dataPoint['AngleXYZCV'], dataPoint['VelXYStDev'], dataPoint['VelXYCV'], dataPoint['AngleXYStDev'], dataPoint['AngleXYCV']]
                writer.writerow(row)


def WriteCSVFromTimeData(filename, data):
    fieldnames = ['time (s)', 'Cells', 'MSDXYZ',
                  'VautoXYZ', 'MSDXY', 'VautoXY']
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()

        for dataPoint in data:
            time = dataPoint['time (s)']
            if (utils.IsFloat(time)):
                row = [dataPoint['time (s)'], dataPoint['Cells'], dataPoint['MSDXYZ'],
                       dataPoint['VautoXYZ'], dataPoint['MSDXY'], dataPoint['VautoXY']]
                writer.writerow(row)


def ComputeCellCharacteristics(data):
    meanderingIndexdata = utils.CalculateMeanderingIndex(data)
    arrestCoefficientdata = utils.CalculateArrestCoefficient(data)
    averagesData = utils.CalculateAverages(data)
    d = defaultdict(dict)
    for l in (meanderingIndexdata, arrestCoefficientdata, averagesData):
        for elem in l:
            d[elem['track ID']].update(elem)
    combineddata = d.values()
    return combineddata


def ComputePopulationOverTimeCharacteristics(data, interval):
    msdData = utils.CalculateMSD(data, interval)
    velautocorrData = utils.CalculateVelAutoCorrForPopulation(data, interval)
    d = defaultdict(dict)
    for l in (msdData, velautocorrData):
        for elem in l:
            d[elem['time (s)']].update(elem)
    combineddata = d.values()
    return combineddata


CompileData(sys.argv[1], sys.argv[2])
