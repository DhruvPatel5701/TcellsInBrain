import sys
import csv
import math
import numpy as np
from scipy.stats import genpareto
#Checks if input is float


def IsFloat(i):
    try:
        float(i)
        return True
    except ValueError:
        return False

#Checks if input is integer


def IsInt(i):
    try:
        int(i)
        return True
    except ValueError:
        return False

#Checks if input is string


def IsString(i):
    try:
        str(i)
        return True
    except ValueError:
        return False

#Get number of tracks in data


def GetUniqueIDs(data):
    IDs = []

    for dataPoint in data:
        trackID = dataPoint['track ID']
        #some time stamps are N/A so lets filter those IDs out
        time = dataPoint['time (s)']
        if (IsString(trackID) and IsFloat(time) and str(trackID) not in IDs):
            IDs.append(str(trackID))
    return len(IDs)

#Checks if ID is in the data


def IsIDInData(freeID, data):
    for dataPoint in data:
        trackID = dataPoint['track ID']
        if (trackID == freeID):
            return True
    return False

#Gets next available track ID for usage


def GetFreeID(data):
    freeID = 1

    while (IsIDInData(freeID, data) == True):
        freeID += 1

    return freeID


def GetUnitVector(vec):
    return vec/np.linalg.norm(vec)


def CalculateAngle(v1, v2):
    v1unitvec = GetUnitVector(v1)
    v2unitvec = GetUnitVector(v2)
    return math.degrees(np.arccos(np.clip(np.dot(v1unitvec, v2unitvec), -1.0, 1.0)))


def CalculateDistance(xi, x, yi, y, zi=0, z=0):
    return CalculateDistanceSquared(xi, x, yi, y, zi, z)**0.5


def CalculateDistanceSquared(xi, x, yi, y, zi=0, z=0):
    return ((x - xi)**2 + (y - yi)**2 + (z-zi)**2)


def CalculateDistPerCellPerTimeStamp(data):
    #Since IDs can't/shouldn't be -
    prevID = -1
    x1 = 0
    y1 = 0
    z1 = 0

    DistDict = []
    for cell in data:
        for dataPoint in cell:
            time = dataPoint['time (s)']
            trackID = dataPoint['track ID']
            x2 = dataPoint['x']
            y2 = dataPoint['y']
            z2 = dataPoint['z']
            currPathlengthXY = 0
            currPathlengthXYZ = 0
            #This is the turn angle of the velocity vectors
            AngleXY = 0
            AngleXYZ = 0

            if (IsFloat(time) and IsString(trackID) and IsFloat(x2) and IsFloat(y2) and IsFloat(z2)):
                if (str(trackID) == str(prevID)):

                    currPathlengthXY = CalculateDistance(
                        float(x1), float(x2), float(y1), float(y2), 0.0, 0.0)
                    currPathlengthXYZ = CalculateDistance(float(x1), float(
                        x2), float(y1), float(y2), float(z1), float(z2))
                else:
                    prevID = trackID
                    #Data should be in order so new ID means t = 0, which we can't calculate velocity for
                    currPathlengthXY = 'N/A'
                    currPathlengthXYZ = 'N/A'

                    x1 = x2
                    y1 = y2
                    z1 = z2

                DistDict.append({'track ID': trackID, 'time (s)': time,
                                 'DistXY': currPathlengthXY, 'DistXYZ': currPathlengthXYZ})
    return DistDict


def ReadDataFromFile(filename):
    with open(filename) as raw:
        reader = csv.DictReader(raw)
        data = [raw for raw in reader]
        return data


def LoadAllData(cleanedfilename):
    data = ReadDataFromFile(cleanedfilename)

    celldatafile = cleanedfilename.replace('cleaned', 'celldata')
    celldata = ReadDataFromFile(celldatafile)

    timedatafile = cleanedfilename.replace('cleaned', 'timedata')
    timedata = ReadDataFromFile(timedatafile)

    return data, celldata, timedata


def RenameDuplicates(data):
    trackIDs = []

    prevID = ''

    for dataPoint in data:
        if (IsString(dataPoint['track ID'])):
            trackID = dataPoint['track ID']
            newID = trackID
            if (str(trackID) == str(prevID)):
                continue
            else:
                if(str(trackID) in trackIDs):
                    #Need to find a cleaner way, but this does the job for now
                    newID = str(trackID) + 'a'
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'b')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'c')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'd')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'e')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'f')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'g')
                    if (str(newID) in trackIDs and str(prevID) != str(newID)):
                        newID = newID.replace(
                            newID, str(trackID) + 'h')
                    trackIDs.append(newID)
                    print('Duplicate: ' + str(trackID)
                          + ' --> ' + str(newID))
                    dataPoint['track ID'] = newID
                else:
                    trackIDs.append(trackID)
            prevID = newID
    return data


def Clean(uncleaneddata, interval):
    data = RenameDuplicates(uncleaneddata)
    lastTime = 0
    lastID = sys.float_info.max
    #Using -1 because IDs can't be negative
    oldID = -1
    newID = -1
    timeDiff = 0
    otime = 0
    IDsToCheck = []

    startingCount = GetUniqueIDs(data)
    for dataPoint in data:
        if (IsFloat(dataPoint['time (s)']) and IsString(dataPoint['track ID'])):
            time = float(dataPoint['time (s)'])
            trackID = str(dataPoint['track ID'])

            #Original values
            otime = dataPoint['time (s)']
            oID = dataPoint['track ID']
            dataPoint['old track ID'] = oID
            dataPoint['old time (s)'] = otime

            if (oldID == trackID):
                otime = dataPoint['time (s)']
                dataPoint['track ID'] = newID
                dataPoint['time (s)'] = float(dataPoint['time (s)']) - timeDiff
                time = float((dataPoint['time (s)']))
            #            print('Time Correction for ' + str(oldID) + ' - ' + str(newID) + 'from: ' + str(otime) + ' to: ' + str(dataPoint['time (s)']))

            #Added 1 to give some leeway
            if (time > float(lastTime) + float(interval)*1.4 or oldID != trackID):
                #    print(str(time) + ' - ' + str(int(lastTime)) + ' > ' + str(Cleaner.interval))
                oldID = trackID

                newID = GetFreeID(data)
                print(str(oldID) + ' --> ' + str(newID))
                dataPoint['track ID'] = newID
                timeDiff = float(otime)
                dataPoint['time (s)'] = 0
                time = 0

            olasttime = lastTime
            lastTime = float(dataPoint['time (s)'])
            #        if (olasttime != lastTime):
            #            print('Diff: ' + str(olasttime) + " != " + str(lastTime))

    endingCount = GetUniqueIDs(data)
    print('Starting Unique Track IDs: ' + str(startingCount))
    print('Ending Unique Track IDs: ' + str(endingCount))
    return data


def CalculateVelocity(data):
    prevID = -1
    prevVel = 'N/A'
    prevX = 'N/A'
    prevY = 'N/A'
    prevZ = 'N/A'
    prevVelX = 'N/A'
    prevVelY = 'N/A'
    prevVelZ = 'N/A'
    prevTime = 0

    accelerationList = []
    index = 0
    for dataPoint in data:
        trackID = dataPoint['track ID']
        time = dataPoint['time (s)']
        x = dataPoint['x']
        y = dataPoint['y']
        z = dataPoint['z']
        if (str(trackID) == str(prevID) and IsFloat(time) and IsFloat(x) and IsFloat(prevX) and float(time) != 0 and float(time) != float(prevTime)):
            velx = 60 * (float(x) - float(prevX)) / \
                         (float(time) - float(prevTime))
            vely = 60 * (float(y) - float(prevY)) / \
                (float(time) - float(prevTime))
            velz = 60 * (float(z) - float(prevZ)) / \
                (float(time) - float(prevTime))

            #sqrt(accelx^2 + accely^2 + accelz^2)
            velxyz = (float(velx) ** 2 + float(vely)
                      ** 2 + float(velz) ** 2) ** 0.5
            velxy = (float(velx) ** 2 + float(vely) ** 2) ** 0.5
            anglexyz = 'N/A'
            anglexy = 'N/A'
            if (IsFloat(prevVelX)):
                anglexyz = CalculateAngle([velx, vely, velz], [
                                             prevVelX, prevVelY, prevVelZ])
                anglexy = CalculateAngle([velx, vely], [
                                             prevVelX, prevVelY])
            prevVelX = velx
            prevVelY = vely
            prevVelZ = velz
            dataPoint['VelX'] = velx
            dataPoint['VelY'] = vely
            dataPoint['VelZ'] = velz
            dataPoint['VelXYZ'] = float(velxyz)
            dataPoint['VelXY'] = float(velxy)
            dataPoint['TimeDiff'] = (float(time) - float(prevTime))
            dataPoint['DisplacementXYZ'] = ((float(x) - float(prevX))**2 + (
                float(y) - float(prevY))**2 + (float(z) - float(prevZ))**2) ** 0.5
            dataPoint['DisplacementXY'] = (
                (float(x) - float(prevX))**2 + (float(y) - float(prevY))**2) ** 0.5
            if (index > 0):
                data[index-1]['AngleXYZ'] = anglexyz
                data[index-1]['AngleXY'] = anglexy
        if(IsFloat(x) is False or IsFloat(prevX) is False or float(time) == 0 or float(time) == float(prevTime)):
            dataPoint['VelX'] = 'N/A'
            dataPoint['VelY'] = 'N/A'
            dataPoint['VelZ'] = 'N/A'
            dataPoint['VelXYZ'] = 'N/A'
            dataPoint['VelXY'] = 'N/A'
            data[index-1]['AngleXYZ'] = 'N/A'
            data[index-1]['AngleXY'] = 'N/A'
            dataPoint['TimeDiff'] = 'N/A'
            dataPoint['DisplacementXYZ'] = 'N/A'
            dataPoint['DisplacementXY'] = 'N/A'
            prevVelX = 'N/A'
            prevVelY = 'N/A'
            prevVelZ = 'N/A'
        prevID = trackID
        prevX = x
        prevY = y
        prevZ = z
        prevTime = time
        index += 1
    data[-1]['AngleXYZ'] = 'N/A'
    data[-1]['AngleXY'] = 'N/A'
    return data


def CalculateAcceleration(data):
    prevID = -1
    prevVel = 'N/A'
    prevVelX = 'N/A'
    prevVelY = 'N/A'
    prevVelZ = 'N/A'
    prevAccelX = 'N/A'
    prevAccelY = 'N/A'
    prevAccelZ = 'N/A'
    prevTime = 0
    index = 0
    for dataPoint in data:
        trackID = dataPoint['track ID']
        time = dataPoint['time (s)']
        vel = dataPoint['VelXYZ']
        velx = dataPoint['VelX']
        vely = dataPoint['VelY']
        velz = dataPoint['VelZ']
        if (str(trackID) == str(prevID) and IsFloat(time) and IsFloat(vel) and IsFloat(prevVel) and float(time) != 0):
            accelx = 60 * (float(velx) - float(prevVelX)) / \
                      (float(time) - float(prevTime))
            accely = 60 * (float(vely) - float(prevVelY)) / \
                (float(time) - float(prevTime))
            accelz = 60 * (float(velz) - float(prevVelZ)) / \
                (float(time) - float(prevTime))

            #sqrt(accelx^2 + accely^2 + accelz^2)
            accelxyz = (float(accelx) ** 2 + float(accely)
                        ** 2 + float(accelz) ** 2) ** 0.5
            accelxy = (float(accelx) ** 2 + float(accely) ** 2) ** 0.5
            angleaccelxyz = 'N/A'
            angleaccelxy = 'N/A'
            if (IsFloat(prevAccelX)):
                angleaccelxyz = CalculateAngle([accelx, accely, accelz], [
                                             prevAccelX, prevAccelY, prevAccelZ])
                angleaccelxy = CalculateAngle([accelx, accely], [
                                             prevAccelX, prevAccelY])
            prevAccelX = accelx
            prevAccelY = accely
            prevAccelZ = accelz

            dataPoint['AccelXYZ'] = accelxyz
            dataPoint['AccelXY'] = accelxy
            if (index > 0):
                data[index-1]['AngleAccelXYZ'] = angleaccelxyz
                data[index-1]['AngleAccelXY'] = angleaccelxy

        if(IsFloat(vel) is False or IsFloat(prevVel) is False):
            dataPoint['AccelXYZ'] = 'N/A'
            dataPoint['AccelXY'] = 'N/A'
            data[index-1]['AngleAccelXYZ'] = 'N/A'
            data[index-1]['AngleAccelXY'] = 'N/A'
            prevAccelX = 'N/A'
            prevAccelY = 'N/A'
            prevAccelZ = 'N/A'
        prevID = trackID
        prevVel = vel
        prevVelX = velx
        prevVelY = vely
        prevVelZ = velz
        prevTime = time
        index += 1
    data[-1]['AngleAccelXYZ'] = 'N/A'
    data[-1]['AngleAccelXY'] = 'N/A'
    return data


def CalculateMeanderingIndex(data):
    prevID = -1

    initx = -1
    inity = -1
    initz = -1

    prevx = -1
    prevy = -1
    prevz = -1
    totaldistancexyz = 0
    totaldistancexy = 0
    meanderingindexList = []
    for dataPoint in data:
        trackID = dataPoint['track ID']
        x = dataPoint['x']
        y = dataPoint['y']
        z = dataPoint['z']
        if (str(trackID) == str(prevID)):
            distancexyz = CalculateDistance(
                float(x), float(prevx), float(y), float(prevy), float(z), float(prevz))
            distancexy = CalculateDistance(
                float(x), float(prevx), float(y), float(prevy))
            totaldistancexyz += distancexyz
            totaldistancexy += distancexy
        if (str(trackID) != str(prevID)):
            displacementxyz = CalculateDistance(
                float(prevx), float(initx), float(prevy), float(inity), float(prevz), float(initz))
            displacementxy = CalculateDistance(
                float(prevx), float(initx), float(prevy), float(inity))
            if (prevID != -1):
                if (totaldistancexy > 0):
                    meanderingindexxyz = displacementxyz/totaldistancexyz
                    meanderingindexxy = displacementxy/totaldistancexy
                    meanderingindexList.append(
                        {'track ID': prevID, 'meanderingIndexXYZ': meanderingindexxyz, 'meanderingIndexXY': meanderingindexxy})
                else:
                    meanderingindexList.append(
                        {'track ID': prevID, 'meanderingIndexXYZ': 'N/A', 'meanderingIndexXY': 'N/A'})
            totaldistancexyz = 0
            totaldistancexy = 0
            initx = x
            inity = y
            initz = z
        prevID = trackID
        prevx = x
        prevy = y
        prevz = z
    if (totaldistancexy > 0):
        displacementxyz = CalculateDistance(
                        float(x), float(initx), float(y), float(inity), float(z), float(initz))
        displacementxy = CalculateDistance(
                        float(x), float(initx), float(y), float(inity))
        meanderingindexxyz = displacementxyz/totaldistancexyz
        meanderingindexxy = displacementxy/totaldistancexy
        meanderingindexList.append(
                            {'track ID': trackID, 'meanderingIndexXYZ': meanderingindexxyz, 'meanderingIndexXY': meanderingindexxy})
    else:
        meanderingindexList.append(
            {'track ID': prevID, 'meanderingIndexXYZ': 'N/A', 'meanderingIndexXY': 'N/A'})
    return meanderingindexList


def CalculateArrestCoefficient(data):
    immobilestepsxyz = 0
    immobilestepsxy = 0
    totalsteps = 0
    cutoff = 2
    arrestcoefficientlist = []
    prevID = -1
    for dataPoint in data:
        trackID = dataPoint['track ID']
        velxyz = dataPoint['VelXYZ']
        velxy = dataPoint['VelXY']
        if (str(prevID) == str(trackID) and IsFloat(velxyz)):
            totalsteps += 1
            if (float(velxyz) < float(cutoff)):
                immobilestepsxyz += 1
            if (float(velxy) < float(cutoff)):
                immobilestepsxy += 1
        if (str(prevID) != str(trackID) and prevID != -1):
            if (totalsteps > 0):
                arrestcoefficientxyz = immobilestepsxyz/totalsteps
                arrestcoefficientxy = immobilestepsxy/totalsteps
                arrestcoefficientlist.append(
                    {'track ID': prevID, 'arrestCoefficientXYZ': arrestcoefficientxyz, 'arrestCoefficientXY': arrestcoefficientxy})
            else:
                arrestcoefficientlist.append(
                    {'track ID': prevID, 'arrestCoefficientXYZ': 'N/A', 'arrestCoefficientXY': 'N/A'})
            immobilestepsxyz = 0
            immobilestepsxy = 0
            totalsteps = 0
        prevID = trackID

    if (totalsteps > 0):
        arrestcoefficientxyz = immobilestepsxyz/totalsteps
        arrestcoefficientxy = immobilestepsxy/totalsteps
        arrestcoefficientlist.append(
            {'track ID': prevID, 'arrestCoefficientXYZ': arrestcoefficientxyz, 'arrestCoefficientXY': arrestcoefficientxy})
    else:
        arrestcoefficientlist.append(
            {'track ID': prevID, 'arrestCoefficientXYZ': 'N/A', 'arrestCoefficientXY': 'N/A'})
    return arrestcoefficientlist


def CalculateAverages(data):
    prevID = -1
    VelXYZ = []
    VelXY = []
    AngleXYZ = []
    AngleXY = []
    accelxyztotal = 0
    accelxytotal = 0
    angleaccelxyztotal = 0
    angleaccelxytotal = 0

    velcount = 0
    anglecount = 0
    accelcount = 0
    angleaccelcount = 0

    avgList = []

    for dataPoint in data:
        trackID = dataPoint['track ID']

        velxyz = dataPoint['VelXYZ']
        anglexyz = dataPoint['AngleXYZ']
        accelxyz = dataPoint['AccelXYZ']
        angleaccelxyz = dataPoint['AngleAccelXYZ']

        velxy = dataPoint['VelXY']
        anglexy = dataPoint['AngleXY']
        accelxy = dataPoint['AccelXY']
        angleaccelxy = dataPoint['AngleAccelXY']
        if (str(prevID) == str(trackID)):
            if(IsFloat(velxy) and math.isnan(velxy) is False):
                velcount += 1
                VelXYZ.append(float(velxyz))
                VelXY.append(float(velxy))

            if(IsFloat(anglexy) and math.isnan(anglexy) is False):
                anglecount += 1
                AngleXYZ.append(float(anglexyz))
                AngleXY.append(float(anglexy))

            if(IsFloat(accelxy) and math.isnan(accelxy) is False):
                accelcount += 1
                accelxyztotal += float(accelxyz)
                accelxytotal += float(accelxy)

            if(IsFloat(angleaccelxy) and math.isnan(angleaccelxy) is False):
                angleaccelcount += 1
                angleaccelxyztotal += float(angleaccelxyz)
                angleaccelxytotal += float(angleaccelxy)

        if (str(prevID) != str(trackID) and prevID != -1):
            avgvelxy = 'N/A'
            avgvelxyz = 'N/A'
            avganglexy = 'N/A'
            avganglexyz = 'N/A'
            avgaccelxy = 'N/A'
            avgaccelxyz = 'N/A'
            avgangleaccelxyz = 'N/A'
            avgangleaccelxy = 'N/A'

            velstdevxyz = 'N/A'
            velcvxyz = 'N/A'

            velstdevxy = 'N/A'
            velcvxy = 'N/A'

            anglestdevxyz = 'N/A'
            anglecvxyz = 'N/A'

            anglestdevxy = 'N/A'
            anglecvxy = 'N/A'
            if(velcount > 0):
                avgvelxyz = sum(VelXYZ)/len(VelXYZ)
                velstdevxyz = float(np.std(VelXYZ))
                if(avgvelxyz != 0):
                    velcvxyz = velstdevxyz/avgvelxyz

                avgvelxy = sum(VelXY)/len(VelXY)
                velstdevxy = float(np.std(VelXY))
                if (avgvelxy != 0):
                    velcvxy = velstdevxy/avgvelxy

            if(anglecount > 0):
                avganglexyz = sum(AngleXYZ)/len(AngleXYZ)
                anglestdevxyz = float(np.std(AngleXYZ))
                if(avganglexyz != 0):
                    anglecvxyz = anglestdevxyz/avganglexyz

                avganglexy = sum(AngleXY)/len(AngleXY)
                anglestdevxy = float(np.std(AngleXY))
                if(avganglexy != 0):
                    anglecvxy = anglestdevxy/avganglexy

            if(accelcount > 0):
                avgaccelxyz = float(accelxyztotal)/float(accelcount)
                avgaccelxy = float(accelxytotal)/float(accelcount)
            if(angleaccelcount > 0):
                avgangleaccelxyz = float(
                    angleaccelxyztotal)/float(angleaccelcount)
                avgangleaccelxy = float(accelxytotal)/float(angleaccelcount)

            VelXYZ = []
            VelXY = []
            AngleXYZ = []
            AngleXY = []
            accelxyztotal = 0
            accelxytotal = 0
            angleaccelxyztotal = 0
            angleaccelxytotal = 0

            velcount = 0
            anglecount = 0
            accelcount = 0
            angleaccelcount = 0
            avgList.append({'track ID': prevID, 'AvgVelXYZ': avgvelxyz, 'AvgAngleXYZ': avganglexyz,
                           'AvgAccelXYZ': avgaccelxyz, 'AvgAngleAccelXYZ': avgangleaccelxyz, 'AvgVelXY': avgvelxy, 'AvgAngleXY': avganglexy, 'AvgAccelXY': avgaccelxy, 'AvgAngleAccelXY': avgangleaccelxy, 'VelXYZStDev': velstdevxyz, 'VelXYZCV': velcvxyz, 'AngleXYZStDev': anglestdevxyz, 'AngleXYZCV': anglecvxyz, 'VelXYStDev': velstdevxy, 'VelXYCV': velcvxy, 'AngleXYStDev': anglestdevxy, 'AngleXYCV': anglecvxy})
        prevID = trackID
    avgvelxy = 'N/A'
    avgvelxyz = 'N/A'
    avganglexy = 'N/A'
    avganglexyz = 'N/A'
    avgaccelxy = 'N/A'
    avgaccelxyz = 'N/A'
    avgangleaccelxyz = 'N/A'
    avgangleaccelxy = 'N/A'
    velstdevxyz = 'N/A'
    velcvxyz = 'N/A'

    velstdevxy = 'N/A'
    velcvxy = 'N/A'

    anglestdevxyz = 'N/A'
    anglecvxyz = 'N/A'

    anglestdevxy = 'N/A'
    anglecvxy = 'N/A'
    if(velcount > 0):
        avgvelxyz = sum(VelXYZ)/len(VelXYZ)
        velstdevxyz = float(np.std(VelXYZ))
        velcvxyz = velstdevxyz/avgvelxyz

        avgvelxy = sum(VelXY)/len(VelXY)
        velstdevxy = float(np.std(VelXY))
        velcvxy = velstdevxy/avgvelxy

    if(anglecount > 0):
        avganglexyz = sum(AngleXYZ)/len(AngleXYZ)
        anglestdevxyz = float(np.std(AngleXYZ))
        anglecvxyz = anglestdevxyz/avganglexyz

        avganglexy = sum(AngleXY)/len(AngleXY)
        anglestdevxy = float(np.std(AngleXY))
        anglecvxy = anglestdevxy/avganglexy

    if(accelcount > 0):
        avgaccelxyz = float(accelxyztotal)/float(accelcount)
        avgvelxy = float(accelxytotal)/float(accelcount)
    if(angleaccelcount > 0):
        avgangleaccelxyz = float(angleaccelxyztotal)/float(angleaccelcount)
        avgangleaccelxy = float(angleaccelxytotal)/float(angleaccelcount)

    avgList.append({'track ID': prevID, 'AvgVelXYZ': avgvelxyz, 'AvgAngleXYZ': avganglexyz,
                   'AvgAccelXYZ': avgaccelxyz, 'AvgAngleAccelXYZ': avgangleaccelxyz, 'AvgVelXY': avgvelxy, 'AvgAngleXY': avganglexy, 'AvgAccelXY': avgaccelxy, 'AvgAngleAccelXY': avgangleaccelxy, 'VelXYZStDev': velstdevxyz, 'VelXYZCV': velcvxyz, 'AngleXYZStDev': anglestdevxyz, 'AngleXYZCV': anglecvxyz, 'VelXYStDev': velstdevxy, 'VelXYCV': velcvxy, 'AngleXYStDev': anglestdevxy, 'AngleXYCV': anglecvxy})
    return avgList


def GetMaxTimeStamp(data):
    maxTime = 0
    for dataPoint in data:
        time = dataPoint['time (s)']
        if (IsFloat(time) and float(time) > float(maxTime)):
            maxTime = time
    return maxTime


def GetNextTimeStamp(data, currentTimeStamp, interval, includeMax=True):
    nextTime = float(currentTimeStamp) + float(interval)
    maxTimeStamp = GetMaxTimeStamp(data)
    if (float(nextTime) > float(maxTimeStamp) and includeMax is True):
        nextTime = maxTimeStamp
    return nextTime


def FindInitialPosition(data, targetID):
    initialX = 0
    initialY = 0
    initialZ = 0
    initialTime = sys.float_info.max

    for dataPoint in data:
        time = dataPoint['time (s)']
        trackID = dataPoint['track ID']
        x = dataPoint['x']
        y = dataPoint['y']
        z = dataPoint['z']

        if (IsString(trackID)):
            if (str(trackID) == str(targetID)):
                if (IsFloat(time) and IsFloat(x) and IsFloat(y) and IsFloat(z)):
                    if (float(time) < float(initialTime)):
                        initialTime = time
                        initialX = x
                        initialY = y
                        initialZ = z
    return {'x': initialX, 'y': initialY, 'z': initialZ}


def FindInitialVelocity(data, targetID):
    initialVel = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A']
    initialAngle = 'N/A'
    initialTime = sys.float_info.max

    for dataPoint in data:
        time = dataPoint['time (s)']
        trackID = dataPoint['track ID']
        velxyz = dataPoint['VelXYZ']
        velxy = dataPoint['VelXY']
        velx = dataPoint['VelX']
        vely = dataPoint['VelY']
        velz = dataPoint['VelZ']
        anglexyz = dataPoint['AngleXYZ']
        anglexy = dataPoint['AngleXY']
        if (IsString(trackID)):
            if (str(trackID) == str(targetID)):
                if (IsFloat(time) and IsFloat(velxyz)):
                    if (float(time) < float(initialTime)):
                        initialTime = time
                        initialVel = [velxyz, velx, vely, velz, velxy]
                        initialAngle = [anglexyz, anglexy]
    return [initialVel, initialAngle]


def CalculateMSDPerTimeStamp(data, currentTimeStamp, interval):
    currentTrackID = '0'
    summationXY = 0
    summationXYZ = 0
    count = 0
    MSDXY = 0
    MSDXYZ = 0

    for dataPoint in data:
        time = dataPoint['time (s)']
        #+/- 3 for leeway
        if (IsFloat(time) and float(time) <= float(currentTimeStamp) + 0.4*float(interval) and float(time) >= (float(currentTimeStamp) - 0.4*float(interval))):
            trackID = dataPoint['track ID']
            x = dataPoint['x']
            y = dataPoint['y']
            z = dataPoint['z']

            if (IsString(trackID) and IsFloat(x) and IsFloat(y) and IsFloat(z)):
                if (str(trackID) != currentTrackID):
                    currentTrackID = str(trackID)
                    initialPosition = FindInitialPosition(data, currentTrackID)
                summationXY += CalculateDistanceSquared(
                        float(initialPosition['x']), float(x), float(initialPosition['y']), float(y))

                msd_ = CalculateDistanceSquared(float(initialPosition['x']), float(x), float(
                    initialPosition['y']), float(y), float(initialPosition['z']), float(z))

                #Check if data needs cleaning
                if (currentTimeStamp == 0 and msd_ != 0):
                    print('########################')
                    print('Track ID '
                          + str(dataPoint['track ID']) + ' needs manual fixing')
                    print('########################')

                summationXYZ += msd_

                count += 1

    MSDXY = summationXY/count
    MSDXYZ = summationXYZ/count

    print(str(currentTimeStamp) + ": " + str(MSDXYZ))
    return {'time (s)': currentTimeStamp, 'MSDXY': MSDXY, 'MSDXYZ': MSDXYZ, 'Cells': count}


def CalculateMSD(data, interval):
    currentTimeStamp = 0
    maxTimeStamp = GetMaxTimeStamp(data)
    MSDdata = []
    while float(currentTimeStamp) <= float(maxTimeStamp):
        MSD = CalculateMSDPerTimeStamp(data, currentTimeStamp, interval)

        print(str(MSD['time (s)']) + 's / ' + str(maxTimeStamp) + 's')

        MSDdata.append({'time (s)': MSD['time (s)'], 'MSDXYZ': MSD['MSDXYZ'],
                       'MSDXY': MSD['MSDXYZ'], 'Cells': MSD['Cells']})

        if (float(currentTimeStamp) == float(maxTimeStamp)):
            break
        currentTimeStamp = GetNextTimeStamp(
            data, currentTimeStamp, interval)
    return MSDdata


def CalculateVelAutoCorrPerTimeStamp(data, currentTimeStamp, interval):
    currentTrackID = '0'
    summationxy = 0
    summationxyz = 0
    count = 0
    autocorrxyz = 'N/A'
    autocorrxy = 'N/A'
    if (currentTimeStamp == 0):
        return {'time (s)': currentTimeStamp, 'VautoXYZ': '1', 'VautoXY': 1}
    for dataPoint in data:
        time = dataPoint['time (s)']
        #+/- 3 for leeway
        if (IsFloat(time) and float(time) <= float(currentTimeStamp) + 0.4*float(interval) and float(time) >= (float(currentTimeStamp) - 0.4*float(interval))):
            trackID = dataPoint['track ID']
            currVelXYZ = dataPoint['VelXYZ']
            currVelXY = dataPoint['VelXY']
            currAngXYZ = dataPoint['AngleXYZ']
            currAngleXY = dataPoint['AngleXY']
            prevTime = float(time) - float(interval)

            initialVel = FindInitialVelocity(data, trackID)
        #    print(str(trackID) + ' ' + str(prevTime) + ' ' + str(prevVel))
            if (IsString(trackID) and IsFloat(currVelXY) and IsFloat(initialVel[0][0])):
                if(float(currVelXY) != 0 and float(initialVel[0][0]) != 0):
                    summationxyz += np.dot([float(dataPoint['VelX']), float(dataPoint['VelY']), float(dataPoint['VelZ'])],
                                           [float(initialVel[0][1]), float(initialVel[0][2]), float(initialVel[0][3])]) / (abs(float(currVelXYZ) * float(initialVel[0][0])))
                    summationxy += np.dot([float(dataPoint['VelX']), float(dataPoint['VelY'])],
                                          [float(initialVel[0][1]), float(initialVel[0][2])]) / (abs(float(currVelXY) * float(initialVel[0][4])))
                    count += 1
    if(count != 0):
        autocorrxyz = summationxyz/count
        autocorrxy = summationxy/count

    return {'time (s)': currentTimeStamp, 'VautoXYZ': autocorrxyz, 'VautoXY': autocorrxy}


def CalculateVelAutoCorrForPopulation(data, interval):
    currentTimeStamp = 0
    maxTimeStamp = GetMaxTimeStamp(data)
    Vauto = []
    while float(currentTimeStamp) <= float(maxTimeStamp):
        vauto_ = CalculateVelAutoCorrPerTimeStamp(
            data, float(currentTimeStamp), interval)
        Vauto.append(vauto_)
        print(str(vauto_['time (s)']) + 's: '
              + str(vauto_['VautoXYZ']))
        if (float(currentTimeStamp) == float(maxTimeStamp)):
            break
        currentTimeStamp = GetNextTimeStamp(
                    data, currentTimeStamp, interval)
    return Vauto


def FitDistribution(data, label):
    PathlengthXYZ = []
    Ids = []
    for dataPoint in data:
        ID = dataPoint['track ID']
        path_ = dataPoint['DisplacementXYZ']
        if(IsFloat(path_)):
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
    return [label, b, loc, scale, mean, var]
