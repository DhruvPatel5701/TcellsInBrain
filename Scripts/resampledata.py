import sys
import csv
import utils


def WriteCSVFromDict(filename, data, interval):
    fieldnames = ['old track ID',
                  'old time (s)', 'track ID', 'time (s)', 'x', 'y', 'z', 'TimeDiff']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()
        lastTime = 0

        for dataPoint in data:
            time = dataPoint['time (s)']
            if (utils.IsFloat(time)):
                timeDiff = float(time) - float(lastTime)
                lastTime = time
                time = float(time)
                row = [dataPoint['old track ID'], dataPoint['old time (s)'], str(interval) + '.' + str(
                    dataPoint['track ID']), time, dataPoint['x'], dataPoint['y'], dataPoint['z'], timeDiff]
                writer.writerow(row)


def GetUniqueIDs(data):
    IDs = []

    for dataPoint in data:
        trackID = dataPoint['track ID']
        #some time stamps are N/A so lets filter those IDs out
        time = dataPoint['time (s)']
        if (utils.IsInt(trackID) and utils.IsFloat(time) and int(trackID) not in IDs):
            IDs.append(int(trackID))
    return len(IDs)


def ResampleData(filename, interval):
    with open(filename) as raw:
        reader = csv.DictReader(raw)
        data = [raw for raw in reader]
        prevID = '-1'
        prevTime = -1
        newData = []
        for dataPoint in data:
            time = dataPoint['time (s)']
            trackID = dataPoint['track ID']
            if (utils.IsFloat(time) and utils.IsString(trackID)):
                if (str(trackID) == prevID):
                    if (float(time) <= (float(prevTime) + float(interval)*1.4) and float(time) >= (float(prevTime) + float(interval)*0.6)):
                        newData.append(dataPoint)
                        prevTime = time
                        prevID = trackID
                else:
                    newData.append(dataPoint)
                    prevID = trackID
                    prevTime = time
        WriteCSVFromDict(filename.replace(
            '.csv', '') + 'resampled' + str(interval) + '.csv', newData)


ResampleData(sys.argv[1], sys.argv[2])
