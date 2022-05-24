from re import L
import matplotlib.pyplot as plt
import sys
import time 
import random
import copy
  

class City:
    def __init__(self,value,x,y,distance,parent):
        self.value = value
        self.x = x
        self.y = y
        self.distance = distance
        self.parent = parent

cities = []

fp = open(sys.argv[1],"r")
check = fp.readline()
no_of_cities = int(fp.readline())
for i in range(no_of_cities):
    cord = fp.readline()
    cord = cord.replace("\n","")
    newcord = cord.split(" ")
    city = City(i,float(newcord[0]),float(newcord[1]),{},-1)
    cities.append(city)

for i in range(no_of_cities):
    distances = fp.readline()
    distances = distances.replace("\n","")
    distance_list = distances.split(" ")
    for j in range(len(distance_list)):
        if j != i:
            cities[i].distance[j] = float(distance_list[j])


#----------------------------------Greedy Approach---------------------------#

def greedy(start):
    global cities
    global no_of_cities
    closedlist = []
    closedlist.append(start)
    current = start
    travelled_dis = 0
    returnvalues = []
    while True:
        if len(closedlist) == no_of_cities:
            break
        short_dis = dict(sorted(cities[current].distance.items(), key=lambda item: item[1],))
        for i in short_dis:
            if i not in closedlist:
                closedlist.append(i)
                travelled_dis = travelled_dis + short_dis[i]
                cities[i].parent = current
                current = i
                break
    travelled_dis = travelled_dis + cities[current].distance[start]
    returnvalues.append(travelled_dis)
    returnvalues.append(current)
    return returnvalues

#finding bestnode in greedy approach
besttour = sys.maxsize
for i in range(no_of_cities):
    returnedvalues = greedy(i)
    if returnedvalues[0]<besttour:
        bestnode = i
        besttour = returnedvalues[0]

start = bestnode

for i in range(no_of_cities):
    cities[i].parent = -1
returnedvalues = greedy(bestnode)
last = returnedvalues[1]

#intial pheromone deposition
pheromoneDepo = []
for i in range(no_of_cities):
    tempDict = {}
    for j in range(no_of_cities):
        if i != j:
            tempDict[j] = 0.1
    pheromoneDepo.append(tempDict)

Curr = last
while True:
    if cities[Curr].parent == -1 :
        break
    pheromoneDepo[cities[Curr].parent][Curr] = pheromoneDepo[cities[Curr].parent][Curr] + 0.1
    Curr = cities[Curr].parent 

#-----------------------------------------Ant colony Pheromone------------------------------#
def TSPACO(start, ER, Q,a,b, m):
    global no_of_cities
    global cities
    global bestnode
    global pheromoneDepo

    minTour = sys.maxsize
    bestTour = []
    bestTourlastCity = -1
    count = 0
    while True:
        count = count + 1
        antTourLists = []
        antTourDistance = []
        lastcity = []

        #building tour for m ants
        for i in range(m):
            closedlist = []
            current = start
            tour = []
            for z in range(no_of_cities):
                city = copy.deepcopy(cities[z]) 
                tour.append(city)
            pathSum = 0
            while True:
                if len(closedlist) == no_of_cities-1:
                    break
                probability = {}
                validNeighbours = []
                for j in tour[current].distance:
                    if j not in closedlist:
                        probability[j] = (pheromoneDepo[current][j]**a)*((1/tour[current].distance[j])**(b))
                        validNeighbours.append(j)
                sum = 0
                for k in probability:
                    sum = sum + probability[k]
                w = []
                for k in probability:
                    probability[k] = probability[k]/sum
                    w.append(probability[k])
                randomBestEdge = random.choices(validNeighbours, weights = w, k=1)
                pathSum = pathSum + tour[current].distance[randomBestEdge[0]]
                closedlist.append(current)
                tour[randomBestEdge[0]].parent = current
                current = randomBestEdge[0]
            pathSum = pathSum + tour[current].distance[start]
            lastcity.append(current)
            antTourDistance.append(pathSum)
            antTourLists.append(tour)
        
        #pheromone update
        for i in range(no_of_cities):
            for j in pheromoneDepo[i]:
                pheromoneDepo[i][j] = (1-ER)*pheromoneDepo[i][j]
        
        for i in range(m):
            Curr = lastcity[i]
            while True:
                if antTourLists[i][Curr].parent == -1 :
                    break
                pheromoneDepo[antTourLists[i][Curr].parent][Curr] = pheromoneDepo[antTourLists[i][Curr].parent][Curr] + (Q/antTourDistance[i])
                Curr = antTourLists[i][Curr].parent 
            pheromoneDepo[lastcity[i]][Curr] = pheromoneDepo[lastcity[i]][Curr] + (Q/antTourDistance[i])
        
        if min(antTourDistance) < minTour:
            idx = antTourDistance.index(min(antTourDistance))
            bestTour = antTourLists[idx]
            bestTourlastCity = lastcity[idx]
            minTour = antTourDistance[idx]
            last = bestTourlastCity
            Citytour = []
            x_coordinates = []
            y_coordinates = []
            while True:
                Citytour.append(last)
                if bestTour[last].parent == -1:
                    break
                last = bestTour[last].parent
            # Increasing Pheromone on mintour
            Curr = bestTourlastCity
            while True:
                if cities[Curr].parent == -1 :
                    break
                pheromoneDepo[bestTour[Curr].parent][Curr] = pheromoneDepo[bestTour[Curr].parent][Curr] + (Q/minTour)
                Curr = bestTour[Curr].parent 
            pheromoneDepo[bestTourlastCity][Curr] = pheromoneDepo[bestTourlastCity][Curr] + (Q/minTour)
            print("Tour Length: ",minTour)
            Citytour.reverse()
            string = ""
            for x in Citytour:
                string = string + str(x)+" "
            print(string+"\n")
        
        if count % 50 == 0 and no_of_cities == 100:
            for i in range(no_of_cities):
                for j in range(no_of_cities):
                    if i != j:
                        pheromoneDepo[i][j] = 0.1
                        
            returnedvalues = greedy(bestnode)
            last = returnedvalues[1]
            lastcopy = last
            while True:
                if cities[lastcopy].parent == -1 :
                    break
                pheromoneDepo[cities[lastcopy].parent][lastcopy] = pheromoneDepo[cities[lastcopy].parent][lastcopy] + 0.01
                lastcopy = cities[lastcopy].parent 

if no_of_cities <= 100:
    TSPACO(start,0.3,8,1,5, 100)
elif no_of_cities > 100 and no_of_cities <= 250:
    TSPACO(start,0.3,8,1,5, 30)
elif no_of_cities>250:
    TSPACO(start,0.7,8,1,5, 20)
