import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from copy import deepcopy
import networkx as nx
import sys


def generateLap(x):
    for i in range(0,len(x)):
        for j in range(0,len(x[i])):
            x[i][j] = x[i][j]*-1
    for i in range(0,len(x)):
        s = sum(x[i])
        x[i][i] = -1*s
    return x

def debug(x, f):
    # print("lap")
    # for i in x:
    #     print(i)
    print("fiedler", f)

def debugs(x):
    print("lap")
    for i in x:
        print(i)

def genPairs(val, vec):
    pairs = []
    for i in range(0,len(val)):
        pairs.append((val[i],vec[:,i]))
    pairs.sort(key=lambda x : x[0])
    return pairs


def scale(x):
    scaler = 0
    for i in x:
        for j in i:
            scaler = max(scaler,j)
    x = [[j/scaler for j in i] for i in x]
    return x

def addEdge(x):
    val, vec = np.linalg.eig(x)
    pairs = genPairs(val,vec)
    fiedler = pairs[1][1] #2nd vec
    #debug(x,fiedler)

    sorter = deepcopy(fiedler)
    sorter = np.abs(sorter)

    prime = []
    secondary = []

    for i in range(0,len(fiedler)):
        prime.append(i)
        secondary.append(i)

    prime.sort(key = lambda x : sorter[x])
    secondary.sort(key = lambda x : sorter[x],reverse=True)

    for i in prime:
        for j in secondary:
            if(x[i][j] == 0):
                x[i][j] = -1
                x[j][i] = -1
                x[i][i] += 1
                x[j][j] += 1
                ret = str(i)+"-"+str(j)
                return x,ret
    return x,"none"


def getConn(x):
    val, vec = np.linalg.eig(x)
    val.sort()
    return val[1].real

def invert(x):
    return np.reciprocal(x)

np.set_printoptions(precision=2,suppress=True)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

fileadj = []

with open(os.path.join(__location__,'data.csv'),'r') as csvfile:
    data = csv.reader(csvfile,delimiter=',')
    for row in data:
        temp = []
        for i in row:
            temp.append(int(i))
        fileadj.append(temp)
    

k =  int(sys.argv[2]) 

scaled = scale(fileadj)
scaled = np.array(scaled)
lap = generateLap(scaled)

string = str(0)+","+str(getConn(lap))+",n/a"
print(string)


for i in range(1,k+1):
    lap,added = addEdge(lap)
    string = str(i)+","+str(getConn(lap))+","+added
    print(string)
    sys.stdout.flush()

finaladj = lap

for i in range(0,len(finaladj)):
    for j in range(0,len(finaladj[i])):
        finaladj[i][j] = -1*finaladj[i][j]
        if(i==j):
            finaladj[i][i] = 0



labeldict = {}
for i in range(0,len(finaladj)):
    labeldict[i] = i

colormap = []

val, vec = np.linalg.eig(lap)
pairsfinal = genPairs(val,vec)
fiedlerfinal = pairsfinal[1][1]

for i in fiedlerfinal:
    if(i > 0):
        colormap.append('blue')
    else:
        colormap.append('red')



G = nx.from_numpy_matrix(finaladj)
nx.draw(G,with_labels=True,node_color=colormap)
plt.savefig(os.path.join(__location__,'out.png'))
print("done")
sys.stdout.flush()