import csv
import sys
import utils


def WriteCSVFromDict(filename, data):
    fieldnames = ['movie', 'track ID',
                  'original time (s)', 'time (s)', 'x', 'y', 'z']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        csvwriter = csv.DictWriter(file, fieldnames)
        csvwriter.writeheader()
        lastTime = 0

        for dataPoint in data:
            time = dataPoint['time (s)']
            if (utils.IsFloat(time)):
                originaltime = dataPoint['original time (s)']
                timeDiff = float(time) - float(lastTime)
                lastTime = time
                time = float(time)
                movie = dataPoint['movie']
                if (utils.IsString(movie) is False):
                    movie = 'N/A'
                row = [movie, str(dataPoint['track ID']), originaltime, time,
                       dataPoint['x'], dataPoint['y'], dataPoint['z']]
                writer.writerow(row)


def Reformat(filename, interval, newInterval):
    with open(filename) as raw:
        reader = csv.DictReader(raw)
        data = [raw for raw in reader]
        currentTimeStamp = 0
        n = 0
        maxTimeStamp = utils.GetMaxTimeStamp(data)
        print('Original Max Time: ' + str(maxTimeStamp))
        while float(currentTimeStamp) <= float(maxTimeStamp) + float(interval):

            for dataPoint in data:
                time = dataPoint['time (s)']
                if (utils.IsFloat(time) and float(time) <= float(currentTimeStamp) + 0.4*float(interval) and float(time) >= (float(currentTimeStamp) - 0.4*float(interval))):
                    #    print('bye')
                    Reformatted = False
                    try:
                        Reformatted = bool(dataPoint['Reformatted'])
                    except:
                        Reformatted = False

                    if (Reformatted is False):
                        dataPoint['original time (s)'] = time
                        dataPoint['time (s)'] = float(newInterval) * n
                        dataPoint['Reformatted'] = True
            currentTimeStamp = utils.GetNextTimeStamp(
                    data, currentTimeStamp, interval, False)
            n += 1
        print('New Max Time: ' + str(utils.GetMaxTimeStamp(data)))
        WriteCSVFromDict(str(filename.replace(
                'checked', '').replace('.csv', '') + 'reformatted.csv'), data)


Reformat(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
