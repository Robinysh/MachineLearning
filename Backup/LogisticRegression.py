import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
#from pylab import *
import matplotlib.lines as lines
import math
import random

randomness = 0
randomness2 = 0
squareLimit = .9999
squareLimitNum = 0.1
numOfData = 200
dataSet = [[],[]] #X, Y
power = [0,1]
fig,ax = plt.subplots()

trueParameters = [-500,5]
parameters = [0,6] #Yintercept, Pheta
learningRate = [.001,.00001]
leastSquareLimit = 0.01

def func(para,x):
	summation = 0
	for i,j in zip(para,power):
		summation += i*(x**j)
	return 1/(1+math.exp(-summation))

def ran(up, low):
	return (up - low)*random.random() + low

#GENERATE
x=0
for i in range (0,numOfData):
	x = i + ran(-randomness,randomness)
	dataSet[0].append(x)
	dataSet[1].append(round(func([trueParameters[0],trueParameters[1]+ran(-randomness2, randomness2)],x)))
	#print(func(trueParameters,x))
#	print x[0]
#print(dataSet[0])
#print(dataSet[1])
p1 = ax.plot(dataSet[0], dataSet[1], '.', c="r")

plt.title('$y=%3.7sx'%(parameters[0]))




class Index(object):
    def next(self, event):
		global power, dataSet, parameters, learningRate
		index = 0
		for k in power:
			#Loop Through parameters
			summation = 0
			for i, j in zip(dataSet[0], dataSet[1]):
				summation += (j - func(parameters,i))*(i**k)
			parameters[index] += learningRate[index]*summation
			index+=1

		#Update Graph
		#line1.set_ydata([parameters[0], numOfData*parameters[1] + parameters[0]])
		ax.relim()
		ax.autoscale_view()
		plt.draw()

		#Least Square
		summation = 0
		for i, j in zip(dataSet[0], dataSet[1]):
			summation += (func(parameters,i)-j)**2
		leastSquare = summation/2/len(dataSet[1])
		line1, = ax.plot([i for i in range(0, numOfData)], [func(parameters, i) for i in range(0, numOfData)], color='k', linestyle='-', linewidth=2)
		ax.set_title('YInt:{} Slope:{}'.format(parameters[0],parameters[1]))
		print leastSquare

    def  loop(self, event):
		global power, dataSet, parameters, learningRate
		while True:
			index = 0
			for k in power:
                #Loop Through parameters
				summation = 0
				for i, j in zip(dataSet[0], dataSet[1]):
				    summation += (j - func(parameters,i))*(i**k)
				parameters[index] += learningRate[index]*summation
				index+=1

            #Update Graph
            #line1.set_ydata([parameters[0], numOfData*parameters[1] + parameters[0]])


            #Least Square
			summation = 0
			for i, j in zip(dataSet[0], dataSet[1]):
				summation += (func(parameters,i)-j)**2
			leastSquare = summation/2/len(dataSet[1])
			print leastSquare
			if leastSquare < leastSquareLimit:
				line1, = ax.plot([i for i in range(0, numOfData)], [func(parameters, i) for i in range(0, numOfData)], color='k', linestyle='-', linewidth=2)
				ax.set_title('YIntercept:{} Slope:{}'.format(parameters[0],parameters[1]))
				ax.relim()
				ax.autoscale_view()
				plt.draw()
				break;
				
				
lastSquare = 100
while True:
			index = 0
			for k in power:
                #Loop Through parameters
				summation = 0
				for i, j in zip(dataSet[0], dataSet[1]):
				    summation += (j - func(parameters,i))*(i**k)
				parameters[index] += learningRate[index]*summation
				index+=1

            #Update Graph
            #line1.set_ydata([parameters[0], numOfData*parameters[1] + parameters[0]])


            #Least Square
			summation = 0
			for i, j in zip(dataSet[0], dataSet[1]):
				summation += (func(parameters,i)-j)**2
			leastSquare = summation/2/len(dataSet[1])
						
			if leastSquare > lastSquare*squareLimit and  leastSquare<squareLimitNum:
				line1, = ax.plot([i for i in range(0, numOfData)], [func(parameters, i) for i in range(0, numOfData)], color='k', linestyle='-', linewidth=2)
				ax.set_title('YIntercept:{} Slope:{}'.format(parameters[0],parameters[1]))
				ax.relim()
				ax.autoscale_view()
				plt.draw()
				break;
			
			else:
				lastSquare = leastSquare
				
				
callback = Index()
axNext = plt.axes([0.8, 0.025, 0.1, 0.05])
bNext = Button(axNext, 'Next')
bNext.on_clicked(callback.next)
axLoop = plt.axes([0.65, 0.025, 0.1, 0.05])
bLoop = Button(axLoop, 'Loop')
bLoop.on_clicked(callback.loop)



plt.grid(True)
plt.show()
