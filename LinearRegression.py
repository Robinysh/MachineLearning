import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
#from pylab import *
import matplotlib.lines as lines
import math
import random

slope = 4
yIntercept = 20
randomness = 5
leastSquare = 10
numOfData = 200
dataSet = [[1]*numOfData,[],[]]
fig,ax = plt.subplots()

parameters = [0, 1]
learningRate = [.0005,.0000005]
leastSquareLimit = 20

for i in range (0,numOfData):
    dataSet[1].append(i + randomness*(random.random() - .5))
    dataSet[2].append(i*slope + yIntercept + randomness*(random.random() - .5))

p1 = ax.plot(dataSet[1], dataSet[2], '.', c="r")

plt.title('$y=%3.7sx+%3.7s$'%(parameters[1], parameters[0]))

line1, = ax.plot([0, numOfData], [parameters[0], 200*parameters[1] + parameters[0]], color='k', linestyle='-', linewidth=2)


class Index(object):

    ind = 0

    def next(self, event):
        global parameters
        self.ind += 1
        index = 0
        for k in dataSet[0:len(dataSet)-1]:
            summation = 0
            for i, j, m in zip(dataSet[1], dataSet[2], k):
                summation += (j - (i*parameters[1] + parameters[0]))*m
            parameters[index] += learningRate[index]*summation
            index+=1

        line1.set_ydata([parameters[0], numOfData*parameters[1] + parameters[0]])

        summation = 0
        for i, j in zip(dataSet[1], dataSet[2]):
            summation += ((i*parameters[1] + parameters[0])-j)**2
        leastSquare = summation/2/len(dataSet[1])
        print leastSquare

        ax.relim()
        ax.autoscale_view()
        ax.set_title('$y=%3.7sx+%3.7s$'%(parameters[1], parameters[0]))
        plt.draw()

    def  loop(self, event):
        global parameters
        while True:
            index = 0
            for k in dataSet[0:len(dataSet)-1]:
                #Loop Through parameters
                summation = 0
                for i, j, m in zip(dataSet[1], dataSet[2], k):
                    summation += (j - (i*parameters[1] + parameters[0]))*m
                parameters[index] += learningRate[index]*summation
                index+=1

            #Update Graph
            line1.set_ydata([parameters[0], numOfData*parameters[1] + parameters[0]])
            ax.relim()
            ax.autoscale_view()
            ax.set_title('$y=%3.7sx+%3.7s$'%(parameters[1], parameters[0]))
            plt.draw()

            #Least Square

            summation = 0
            for i, j in zip(dataSet[1], dataSet[2]):
                summation += ((i*parameters[1] + parameters[0])-j)**2
            leastSquare = summation/2/len(dataSet[1])
            print leastSquare
            if leastSquare < leastSquareLimit:
                break;



callback = Index()
axNext = plt.axes([0.8, 0.025, 0.1, 0.05])
bNext = Button(axNext, 'Next')
bNext.on_clicked(callback.next)
axLoop = plt.axes([0.65, 0.025, 0.1, 0.05])
bLoop = Button(axLoop, 'Loop')
bLoop.on_clicked(callback.loop)


plt.grid(True)
plt.show()
