import sys
import numpy as np
import random
from random import randint
import scipy as sc
import scipy.stats
from scipy.stats import pareto


def GetPauseLength(muPause, pattern='alternate', pausedLast='false'):
    if (muPause < 1):
        return 0
    if (pattern == 'alternate'):
        if (pausedLast is True):
            return 0
        return PauseLength(muPause)
    if (pattern == 'random'):
        if (pausedLast is True):
            return 0
        if (randint(0, 1) == 1):
            return PauseLength(muPause)
        return 0


def PauseLength(muPause):
    r = 3
    alpha = float(muPause) - 1
    if (alpha >= 1):
        #rmin = r*(alpha - 1)/alpha
        return random.choice(pareto.rvs(alpha, size=1))
    else:
        return random.choice(pareto.rvs(alpha, size=1))


def NextDisplacement(muRun):
    #4.5 micrometers per minute
    r = 0.75
    alpha = float(muRun) - 1
    if (alpha <= 0):
        return 0
    if (alpha > 1):
        #rmin = r*(alpha - 1)/alpha
        return random.choice(pareto.rvs(alpha, size=1))
    else:
        return random.choice(pareto.rvs(alpha, size=1))


def GetAngle(kappa):
    kappa = float(kappa)
    n = 1
    direction = np.array([0, 0, 1])
    direction = direction / np.linalg.norm(direction)

    res_sampling = rvMF(n, kappa * direction)

    vec = res_sampling / np.linalg.norm(res_sampling)
    return vec


def rW(n, kappa, m):
    dim = m-1
    b = dim / (np.sqrt(4*kappa*kappa + dim*dim) + 2*kappa)
    x = (1-b) / (1+b)
    c = kappa*x + dim*np.log(1-x*x)

    y = []
    for i in range(0, n):
        done = False
        while not done:
            z = sc.stats.beta.rvs(dim/2, dim/2)
            w = (1 - (1+b)*z) / (1 - (1-b)*z)
            u = sc.stats.uniform.rvs()
            if kappa*w + dim*np.log(1-x*w) - c >= np.log(u):
                done = True
        y.append(w)
    return y


def rvMF(n, theta):
    dim = len(theta)
    kappa = np.linalg.norm(theta)
    mu = theta / kappa
    result = []
    for sample in range(0, n):
        w = rW(n, kappa, dim)
        v = np.random.randn(dim)
        v = v / np.linalg.norm(v)
        result.append(np.sqrt(1-np.square(w))*v + w*mu)

    return result


def SimulateCell(trackID, steps, muRun, muPause, kappa, pausePattern='alternate'):
    SimulatedCell = []
    currentStep = 0
    currentx = 0
    currenty = 0
    currentz = 0
    pauseDuration = int(0)
    paused = False
    while (currentStep <= int(steps)):
        if (pauseDuration > 0):
            pauseDuration -= 1
        else:
            pauseLength = GetPauseLength(
                muPause, pattern=pausePattern, pausedLast=paused)
            if (pauseLength == 0):
                displacement = NextDisplacement(muRun)
                angle = GetAngle(kappa)
                currentx += (displacement * angle[0][0])
                currenty += (displacement * angle[0][1])
                currentz += (displacement * angle[0][2])
                paused = False
            else:
                pauseDuration = pauseLength
                paused = True
        celldata = dict()
        celldata['track ID'] = trackID
        celldata['time (s)'] = currentStep*10
        celldata['x'] = currentx
        celldata['y'] = currenty
        celldata['z'] = currentz

        SimulatedCell.append(celldata)
        currentStep += 1
    return SimulatedCell


def Simulate(cells, steps, muRun, muPause, kappa, pausePattern):
    i = 1
    Simulation = []
    while (i <= cells):
        Simulation.append(SimulateCell(
            i, steps, muRun, muPause, kappa, pausePattern))
        i += 1
    return Simulation
