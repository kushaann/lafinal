import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from copy import deepcopy
import networkx as nx
import sys
import math


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

def reverseLap(a):
    x = deepcopy(a)
    for i in range(0,len(x)):
        for j in range(0,len(x[i])):
            x[i][j] = -1*x[i][j]
            if(i==j):
                x[i][i] = 0
    
    for i in range(0,len(x)):
        for j in range(0,len(x[i])):
            if(x[i][j] == 0):
                x[i][j] = math.inf
        x[i][i] = 0
    return x



def genDist(start, x):
    G = reverseLap(x)
    v = len(G)
    dist = deepcopy(G)
    for k in range(0,v):
        for i in range(0,v):
            for j in range(0,v):
                if (dist[i][k] + dist[k][j] < dist[i][j]):  
                    dist[i][j] = dist[i][k] + dist[k][j]
    ret = []
    for i in range(0,v):
        ret.append(dist[start][i])
    return ret


def addEdge(x):
    val, vec = np.linalg.eig(x)
    pairs = genPairs(val,vec)
    fiedler = pairs[1][1] #2nd vec
    #debug(x,fiedler)
    pos = []
    neg = []
    for i in range(0,len(fiedler)):
        if(fiedler[i] > 0):
            pos.append(i)
        else:
            neg.append(i)
    neg.sort(key=lambda x : fiedler[x])
    pos.sort(key = lambda x : fiedler[x], reverse=True)
  
    if(abs(neg[0]) > pos[0]): #negative has larger magnitude
        first = neg
        second = pos
    else:
        first = pos
        second = neg
    for i in first:
        dist = genDist(i,x)
        options = []
        for j in range(0,len(x)):
            if(j!=i):
                options.append(j)
        options.sort(key = lambda x : dist[x],reverse=True)
        for j in options:
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


G = nx.from_numpy_matrix(finaladj)

val, vec = np.linalg.eig(lap)
pairsfinal = genPairs(val,vec)
fiedlerfinal = pairsfinal[1][1]
colormap = []
for i in fiedlerfinal:
    if(i > 0):
        colormap.append('blue')
    else:
        colormap.append('red')

nx.draw(G,with_labels=True,node_color=colormap)


plt.savefig(os.path.join(__location__,'out.png'))
print("done")
sys.stdout.flush()