from itertools import combinations as cm
import copy
import random

#-------------------------------------Generation of input----------------------------#

N = int(input("Enter the N (No. of variables): "))
K = int(input("Enter the K (No. of clauses): "))

print("\n#---------Application of Algorithms----------#\n")

Literals = []
clauses = []

for i in range(N):
    Literals.append(chr(97+i))
    Literals.append("~"+chr(97+i))

for i in range(K):
    Literal1 = random.choice(Literals)
    Literal2 = ""
    Literal3 = ""
    while True:
        literal2 = random.choice(Literals)
        if Literal1[0] == "~":
            if len(literal2) == 1:
                if Literal1[1] == literal2[0]:
                    continue
                else:
                    Literal2 = literal2
                    break
            else:
                if literal2 == Literal1:
                    continue
                else:
                    Literal2 = literal2
                    break
        else:
            if len(literal2) == 1:
                if literal2 == Literal1:
                    continue
                else:
                    Literal2 = literal2
                    break
            else:
                if Literal1[0] == literal2[1]:
                    continue
                else:
                    Literal2 = literal2
                    break
    flag1 = 0
    flag2 = 0
    while True:
        literal3 = random.choice(Literals)
        if Literal1[0] == "~":
            if len(literal3) == 1:
                if Literal1[1] == literal3[0]:
                    continue
                else:
                    flag1 = 1
            else:
                if literal3 == Literal1:
                    continue
                else:
                    flag1 = 1
        else:
            if len(literal3) == 1:
                if literal3 == Literal1:
                    continue
                else:
                    flag1 = 1
            else:
                if Literal1[0] == literal3[1]:
                    continue
                else:
                    flag1 = 1
        
        #----condition for flag2------#

        if Literal2[0] == "~":
            if len(literal3) == 1:
                if Literal2[1] == literal3[0]:
                    continue
                else:
                    flag2 = 1
            else:
                if literal3 == Literal2:
                    continue
                else:
                    flag2 = 1
        else:
            if len(literal3) == 1:
                if literal3 == Literal2:
                    continue
                else:
                    flag2 = 1
            else:
                if Literal2[0] == literal3[1]:
                    continue
                else:
                    flag2 = 1
        if flag1 == 1 and flag2 == 1:
            Literal3 = literal3
            break
        else:
            flag1 = 0
            flag2 = 0
    Clause = (Literal1 + " " + Literal2 + " " + Literal3)
    clauses.append(Clause)

fp = open("input.txt","w")
for i in clauses:
    fp.write(i)
    fp.write("\n")
fp.close()

#------------------------------End of input generation------------------------------------#

#------------------------------Application of algorithm-----------------------------------#

Clauses = []

class clause:
    def __init__(self,literals,value):
        self.literals = literals
        self.value = value


class state:
    def __init__(self):
        self.bool_value = {}
        self.h_value = 0

fp = open("input.txt","r")
for i in range(K):
    string = fp.readline()
    newString = string.replace("\n","")
    literals = newString.split(" ")
    Clauses.append(clause(literals,"False"))
fp.close()

start = state()
for i in range(N):
    start.bool_value[chr(97+i)] = "False" 

def cal_value_clauses(state):
    global Clauses
    for i in Clauses:
        output = ""
        count = 1
        for j in i.literals:
            if len(j) == 2:
                if count == 3:
                    output = output + " not " + state.bool_value[j[1]]
                    count = count + 1
                else:
                    output = output + " not " + state.bool_value[j[1]] + " or "
                    count = count + 1
            else:
                if count == 3:
                    output = output + " " + state.bool_value[j[0]]
                    count = count + 1
                else:
                    output = output + " " + state.bool_value[j[0]] + " or "
                    count = count + 1
        i.value = str(eval(output))


def heuristic():
    global Clauses
    h_value = 0
    for clause in Clauses:
        if clause.value == "True":
            h_value = h_value + 1
    return h_value

def moveGen(current_state,choice):
    global N
    comb = cm(range(0,N),choice)
    neighbours = []
    for i in comb:
        temp = copy.deepcopy(current_state)
        for j in i:
            temp.bool_value[chr(97+j)] = str(eval("not " + temp.bool_value[chr(97+j)] ))
        cal_value_clauses(temp)
        temp.h_value = heuristic()
        neighbours.append(temp)
    return neighbours


def goalTest():
    global Clauses
    for i in Clauses:
        if i.value == "False":
            return 0
    return 1

#-----------------------------------------VND---------------------------------#

explored = 0
def VND(start,choice):
    global N
    if choice == N + 1:
        print("no")
        return
    current = start
    global explored
    cal_value_clauses(current)
    current.h_value = heuristic()
    explored = explored + 1
    if goalTest() == 1:
        print("\n=>> 3-CNF SAT is satisfied by Variable Neighbourhood Descent search")
        print("=>> Total Number of explored states is: " + str(explored))
        print("=>> The boolean values of the goal state for which the given SAT problem is satisfied is:")
        print(current.bool_value)
        return
    neighbours = moveGen(current,choice)
    neighbours.sort(key=lambda x: x.h_value)
    bestNode = neighbours.pop()
    if bestNode.h_value > current.h_value:
        current = bestNode
        if choice > 1:
            choice = 1
        VND(current,choice)
    else:
        explored = explored - 1
        VND(current,choice+1)

#-------------------------------------Beamsearch------------------------------#

openList = []
closeList = []  
def moveGenBeam(currentNode):
    global N
    comb = cm(range(0,N),1)
    neighbours = []
    for i in comb:
        temp = copy.deepcopy(currentNode)
        for j in i:
            temp.bool_value[chr(97+j)] = str(eval("not " + temp.bool_value[chr(97+j)] ))
        cal_value_clauses(temp)
        temp.h_value = heuristic()
        if closeList.count(temp) == 0:
            neighbours.append(temp)
    return neighbours

exploredBeam = 0
def beamSearch(B):
    global openList
    global closeList
    global start 
    global exploredBeam
    exploredBeam = exploredBeam+1
    cal_value_clauses(start)
    start.h_value = heuristic()
    if goalTest() == 1:
        print("\n=>> 3-CNF SAT is satisfied by Beam search")
        print("=>> Total Number of explored states is: " + str(exploredBeam))
        print("=>> The boolean values of the goal state for which the given SAT problem is satisfied is:")
        print(start.bool_value)
        return
    openList = moveGenBeam(start)
    closeList.append(start)
    openList.sort(key=lambda x: x.h_value)
    while True:
        bestNodes = []
        for i in range(B):
            bestNodes.append(openList.pop())
        for bestNode in bestNodes:
            exploredBeam = exploredBeam + 1
            cal_value_clauses(bestNode)
            if goalTest() == 1:
                print("\n=>> 3-CNF SAT is satisfied by Beam search")
                print("=>> Total Number of explored states is: " + str(exploredBeam))
                print("=>> The boolean values of the goal state for which the given SAT problem is satisfied is:")
                print(bestNode.bool_value)
                return
        openList = []
        for bestNode in bestNodes:
            tempList = moveGenBeam(bestNode)
            for neighbour in tempList:
                openList.append(neighbour)
        openList.sort(key = lambda x: x.h_value)
        for bestNode in bestNodes:
            closeList.append(bestNode)

#---------------------------------------Tabusearch----------------------------------#
        
tenure = {}
for i in range(N):
    tenure[chr(97+i)] = 0

exploredtabu = 0
def tabusearch(T):
    global tenure
    global start
    global exploredtabu
    current = start
    while True:
        cal_value_clauses(current)
        start.h_value = heuristic()
        exploredtabu = exploredtabu + 1
        if goalTest() == 1:
            print("\n=>> 3-CNF SAT is satisfied by Tabu search")
            print("=>> Total Number of explored states is: " + str(exploredtabu))
            print("=>> The boolean values of the goal state for which the given SAT problem is satisfied is:")
            print(current.bool_value)
            return
        neighbours = moveGen(current,1)
        finalneighbours = []
        for i in neighbours:
            for j in current.bool_value:
                if current.bool_value[j] != i.bool_value[j]:
                    if tenure[j] == 0:
                        finalneighbours.append(i)
                        break
                    else:
                        tenure[j] = tenure[j] - 1
                        break
        finalneighbours.sort(key=lambda x: x.h_value)
        bestnode = finalneighbours.pop()
        for i in current.bool_value:
            if current.bool_value[i] != bestnode.bool_value[i]:
                tenure[i] = T
        current = bestnode

#--------------------------------End of Algorithm-------------------------#

print("Choose option:")
print("1. Variable Neighbourhood Descent\n2. Beam Search\n3. Tabu Search\n")

run = int(input("Enter the option: "))

if run == 1:
    VND(start,1)
elif run == 2:
    B = int(input("Enter the Beam Width Value: "))
    beamSearch(B)
elif run == 3:
    T = int(input("Enter the Tabu Tenure Value: "))
    tabusearch(T)
else:
    print("Invalid option")

#-------------------------End of Code---------------------------------#