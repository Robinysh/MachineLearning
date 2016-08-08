import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math
import random

"""
#Bugs:

"""
dataX = []
dataY = []
fig,ax = plt.subplots()

randomness = [0,0,0]
numOfData = 10
numRange = [100, 100]
trueW = np.array([-1,1]) #0=a+b*x1+c*x2
trueB = 0
w = np.array([.1,.01])
b = 0

learningRate = [.5,.5,.5]
llLimit = 0.0001

def sigmoid(x):
	return 1/(1+math.exp(-x))

def lin(x, m, b):
	return np.dot(m,x) + b

def ran(low, up):
	return (up - low)*random.random() + low

#GENERATE
for i in range (0,numOfData):
	#Gen X value
	set=[]
	for j in numRange:
		set.append(ran(0, j))
	dataX.append(set[:]) #[:] appends a copy instead of reference

	#Gen Y value with randomness
	for j,k in zip(range(0,len(set)), randomness):
		set[j] += ran(-k,k)
	dataY.append(1 if trueB + np.dot(np.asarray(set), np.transpose(trueW))> 0 else -1) #1 if wx > 0.5 else 0

dataX = np.asarray(dataX)
dataY = np.asarray(dataY)
a = np.ones((len(dataY),1))

p1 = ax.scatter(dataX[:,len(w)-2], dataX[:,len(w)-1], c=dataY, s=20, cmap="gray") #cmap gives gray color gradient wrt c=dataY [0,1]

#Button Class
class Index(object):
    def next(self, event):
		k = 0
		while (k < 10):
			#zeta -= a_i*y_i
			#a_n = (zeta-a_m*y_m)*y_n
			#a_m += (1+y_m*y_n)*(sum of 2a -1)
			#w = sum a_i*y_i*x_i


			global w, b
			ll= 0
			#SMO find a
			for i in range(0, len(a)-1):
				zeta = -np.sum(a.T*dataY)
				eta = 2*np.dot(dataX[i],dataX[i+1])-np.dot(dataX[i+1],dataX[i+1])-np.dot(dataX[i],dataX[i])
				oldai = a[i]
				a[i] -= dataY[i]*((lin(dataX[i+1], w, b)-dataY[i+1])-(lin(dataX[i], w, b)-dataY[i]))/eta
				a[i+1] += dataY[i]*dataY[i+1]*(oldai-a[i])
			print "a", a

			#Find w
			w = np.zeros(len(dataX[0]))
			for i in range(0, len(dataX)):
				#print np.multiply(a[i]*dataY[i],dataX[i])
				w += np.multiply(a[i]*dataY[i],dataX[i])
			w = np.multiply(w, 1/w[1]) #Normalize
			print "w2", w

			#Find b
			setMax = []
			setMin = []
			for i in range(0, len(dataX)):
				if(dataY[i] == -1):
					setMax.append(np.dot(w.T,dataX[i]))
				else:
					setMin.append(np.dot(w.T,dataX[i]))
			b = (max(setMax)+min(setMin))/-2
			k+=1

		#Update Graph
		line1.set_ydata([-b/w[1], -b/w[1]-numRange[0]*w[0]/w[1]],)
		ax.relim() #recalculate axis limit
		ax.autoscale_view() #show new axis limit
		plt.draw()


callback = Index()
axNext = plt.axes([0.8, 0.025, 0.1, 0.05])

bNext = Button(axNext, 'Next')
bNext.on_clicked(callback.next)

#y = -c/a - x*b/a
line1, = ax.plot([0, numRange[0]], [-b/w[1], -b/w[1]-numRange[0]*w[0]/w[1]], color='k', linestyle='-', linewidth=2)
line2, = ax.plot([0, numRange[0]], [-trueB/trueW[1], -trueB/trueW[1]-numRange[0]*trueW[0]/trueW[1]], color='#FF0000', linestyle='-', linewidth=2)

ax.grid(True)
plt.show()
