import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math
import random

"""
#Bugs:
	Math range error with sigmoid() or log(hxj)
	when initial value is too off
"""
dataX = []
dataY = []
fig,ax = plt.subplots()

randomness = [0,0,0]
numOfData = 500
numRange = [10, 10]
trueParameters = np.array([0,-0.01,0.01]) #0=a+b*x1+c*x2
parameters = np.array([2.,.1,.01])
learningRate = [.5,.5,.5]
llLimit = 0.0001

def sigmoid(x):
	return 1/(1+math.exp(-x))

def ran(low, up):
	return (up - low)*random.random() + low

#GENERATE
for i in range (0,numOfData):
	set = [1] #Set x to first parameter as constant 1

	#Gen X value
	for j in numRange:
		set.append(ran(0, j))
	dataX.append(set[:]) #[:] appends a copy instead of reference

	#Gen Y value with randomness
	for j,k in zip(range(0,len(set)), randomness):
		set[j] += ran(-k,k)
	dataY.append(round(sigmoid(np.dot(np.asarray(set), np.transpose(trueParameters))))) #1 if wx > 0.5 else 0

dataX = np.asarray(dataX)
dataY = np.asarray(dataY)

p1 = ax.scatter(dataX[:,1], dataX[:,2], c=dataY, s=20, cmap="gray") #cmap gives gray color gradient wrt c=dataY [0,1]

#Button Class
class Index(object):
    def next(self, event):
		#H += -hxj*(1-hxj)*X.T*X
		#grad += hxj.T*(Y-hxj)
		#ll += Y*log(hxj) + (1-Y)log(1-hxj)
		#w += (inv(H)*grad).T
		global parameters
		ll=0
		H = np.zeros((3,3))
		grad = np.zeros((3,1))
		for j in range(0,len(dataX)):
			dataSet = dataX[j,:][None, :]
			hxj = sigmoid(np.dot(dataSet, parameters.T))
			H -= hxj*(1-hxj)*np.dot(dataSet.T, dataSet)
			grad += np.dot(dataSet.T,(dataY[j]-hxj))
			ll += math.log(hxj) if (dataY[j]==1) else math.log(1-hxj)
		parameters -= np.multiply(np.dot(np.linalg.inv(H),grad).T[0],learningRate)

		print "ll:",ll
		line1.set_ydata([-parameters[0]/parameters[2], -parameters[0]/parameters[2]-numRange[0]*parameters[1]/parameters[2]],)
		ax.relim() #recalculate axis limit
		ax.autoscale_view() #show new axis limit
		plt.draw()


callback = Index()
axNext = plt.axes([0.8, 0.025, 0.1, 0.05])

bNext = Button(axNext, 'Next')
bNext.on_clicked(callback.next)

#y = -c/a - x*b/a
line1, = ax.plot([0, numRange[0]], [-parameters[0]/parameters[2], -parameters[0]/parameters[2]-numRange[0]*parameters[1]/parameters[2]], color='k', linestyle='-', linewidth=2)
line2, = ax.plot([0, numRange[0]], [-trueParameters[0]/trueParameters[2], -trueParameters[0]/trueParameters[2]-numRange[0]*trueParameters[1]/trueParameters[2]], color='#FF0000', linestyle='-', linewidth=2)

print parameters

ax.grid(True)
plt.show()
