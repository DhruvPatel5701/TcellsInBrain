import sys
import csv
import simulatorutils


def WriteCSVFromList(filename, list):
    fieldnames = ['track ID', 'time (s)', 'x', 'y', 'z']
    with open(filename, 'w', newline='') as file:
        csvwriter = csv.writer(file, fieldnames)
        csvwriter.writerow(fieldnames)

        for cell in list:
            for dataPoint in cell:
                row = [dataPoint['track ID'],
                       dataPoint['time (s)'], dataPoint['x'], dataPoint['y'], dataPoint['z']]
                csvwriter.writerow(row)


def RunSimulations(filename, cells, steps, muRun, muPause, kappa, pausePattern='alternate'):
    simulations = simulatorutils.Simulate(int(cells), int(
        steps), float(muRun), float(muPause), float(kappa), str(pausePattern))
    WriteCSVFromList(filename, simulations)


if (len(sys.argv) > 6):
    RunSimulations(sys.argv[1], sys.argv[2], sys.argv[3],
                   sys.argv[4], sys.argv[5], sys.argv[6])
else:
    RunSimulations(sys.argv[1], sys.argv[2],
                   sys.argv[3], sys.argv[4], sys.argv[5])
