
import sys
from math import sqrt
from math import floor
from math import ceil


def intersectedNodes(node_overlaping,queryRectNum,nodes_accesed_query1):

    intersected_node_ids = []

    for child in node_overlaping[1]: 

        node_id = int(child[0]) 

        if len(child) == 3 : # to distinguish the registries from the nodes
            if child[2] ==1:
                isLeaf = True
        else:
            isLeaf = False

        xmin = child[1][0]
        xmax = child[1][1]

        ymin = child[1][2]
        ymax = child[1][3]


        intersect = doOverlap(queryRectNum,xmin,xmax,ymin,ymax) #check if overlaping with the query rect

        if intersect: # if intersected check if its a leaf, not a node

            if not isLeaf: # if its not a leaf and intersected check the children nodes
                nodes_accesed_query1.append(node_id)
                node_lower_level = rTree[node_id]

                intersected_node_ids += intersectedNodes(node_lower_level,queryRectNum,nodes_accesed_query1)

            else: #if its a leaf append the id

                intersected_node_ids.append(node_id)


    return intersected_node_ids

def doOverlap(queryRectNum,xmin,xmax,ymin,ymax):

    xLowQuery = query_rectangles[queryRectNum][1]
    xHighQuery = query_rectangles[queryRectNum][2]
    yLowQuery = query_rectangles[queryRectNum][3]
    yHighQuery = query_rectangles[queryRectNum][4]

    if xLowQuery > xmax or xmin > xHighQuery:
        return False
    if yHighQuery < ymin or ymax < yLowQuery:
        return False

    return True

def findLeafsFromNode(node):
    leafs=[]

    #---------------------
    # Find the leafs that are inside a node, example: 
    # if i got the top level node id must return 126437 reggistries 
    # (all the rectangles that are insinde)
    #---------------------

    for child in node[1]:

        node_id = int(child[0])
        if len(child) == 3 :
            if child[2] ==1:
                isLeaf = True
        else:
            isLeaf = False

        if not isLeaf:
            node_lower_level = rTree[node_id]

            leafs += findLeafsFromNode(node_lower_level)
        else:
            leafs.append(node_id)

    return leafs

def rectsInsideQuery(node,queryRectNum,leafsInsideQ,nodes_accesed_query2):

    for child in node[1]:
        node_id = int(child[0])


        if len(child) == 3 :
            if child[2] ==1:
                isLeaf = True
        else:
            isLeaf = False

        xmin = child[1][0]
        xmax = child[1][1]

        ymin = child[1][2]
        ymax = child[1][3]



        nested = isInside(queryRectNum,xmin,xmax,ymin,ymax)

        if nested == False: # if not nested then goes to the nodes childrens ( goes bellow)

            if not isLeaf:

                node_lower_level = rTree[node_id]
                nodes_accesed_query2.append(node_id) # total nodes that has been accesed
                rectsInsideQuery(node_lower_level,queryRectNum,leafsInsideQ,nodes_accesed_query2)  #recursion until it finds a node that is nested to the query rect


        else:
            if not isLeaf: # nested + leaf, then goes to findLeafsFromNode() and returns the total registries in that node
                node_lower_level = rTree[node_id] 

                leafsInsideThatNode = findLeafsFromNode(node_lower_level)
                for i in leafsInsideThatNode: 
                    leafsInsideQ.append(i)

            if isLeaf:
                leafsInsideQ.append(node_id)


def isInside(queryRectNum,xmin,xmax,ymin,ymax):

    
   
    xLowQuery = query_rectangles[queryRectNum][1]
    xHighQuery = query_rectangles[queryRectNum][2]

    yLowQuery = query_rectangles[queryRectNum][3]
    yHighQuery = query_rectangles[queryRectNum][4]
# check if the query rect has the MBR of the given node
    if ((xLowQuery<=xmin and xHighQuery>=xmax) and (yLowQuery<=ymin and yHighQuery>=ymax)):
        return True

    return False

def queryContainment(rectNum):
    # checks if the query rect contained by a leaf

    xLowQuery = query_rectangles[rectNum][1]
    xHighQuery = query_rectangles[rectNum][2]

    yLowQuery = query_rectangles[rectNum][3]
    yHighQuery = query_rectangles[rectNum][4]

    leafs_that_containQ = 0
    nodes_accesed_query3 = 0

    for i in range(len(rTree)):

        for j in range(len(rTree[i][1])):


                xmin = rTree[i][1][j][1][0]
                xmax = rTree[i][1][j][1][1]

                ymin = rTree[i][1][j][1][2]
                ymax = rTree[i][1][j][1][3]

                if len(rTree[i][1][j]) == 3 :
                    isLeaf = True
                else:
                    isLeaf = False

                if ((xmin<=xLowQuery and xmax>=xHighQuery) and (ymin<=yLowQuery and ymax>=yHighQuery)):
                    if isLeaf:
                        leafs_that_containQ=leafs_that_containQ+1

        if not isLeaf:
                break
        nodes_accesed_query3 = nodes_accesed_query3 +1


    return (leafs_that_containQ ,nodes_accesed_query3) 


def query1():
    query1 = []
    nodes_accesed_query1=[]
    for i in range(len(query_rectangles)-1):
        intersectedRegisters = []

        node = rTree[len(rTree)-1] #top level of the tree
        queryRectNum = i #index querry rectangle
        intersectedRegisters = intersectedNodes(node,queryRectNum,nodes_accesed_query1)

        query1.append([len(intersectedRegisters),len(nodes_accesed_query1)]) #len(intersectedRegisters) total registries, len(nodes_accesed_query1) total nodes  accesed
        nodes_accesed_query1=[]
        intersectedRegisters=[]

    return query1

def query2():
    query2 =[]
    nodes_accesed_query2= []
    temp = 0
    for i in range(len(query_rectangles)-1): 
        node = rTree[len(rTree)-1]
        leafsInsideQ=[] 
        nodes_accesed_query2 = [] 
        rectsInsideQuery(node,i,leafsInsideQ,nodes_accesed_query2)
        query2.append([len(leafsInsideQ),len(nodes_accesed_query2)])

    return query2

def query3():
    query3 =[]
    for i in range(len(query_rectangles)-1):
        leafs_that_containQ = queryContainment(i)
        query3.append(leafs_that_containQ)

    return query3

#Finding the x-y low,high coordinates for each node in each level
def xLow(k,epipedo):

    xlow=float(levels[epipedo][k][1][0][1][0])

    for i in range(len(levels[epipedo][k][1])):


        temp = float(levels[epipedo][k][1][i][1][0])

        if xlow > temp:
            xlow = temp

    xlow=str(xlow)

    return xlow

def yLow(k,epipedo):

    ylow=float(levels[epipedo][k][1][0][1][2])

    for i in range(len(levels[epipedo][k][1])):

        temp = float(levels[epipedo][k][1][i][1][2])

        if ylow > temp:
            ylow = temp

    ylow=str(ylow)

    return ylow

def xHigh(k,epipedo):

    xHigh=float(levels[epipedo][k][1][0][1][1])

    for i in range(len(levels[epipedo][k][1])):

        temp = float(levels[epipedo][k][1][i][1][1])

        if xHigh < temp:
            xHigh = temp

    xHigh=str(xHigh)

    return xHigh

def yHigh(k,epipedo):

    yHigh=float(levels[epipedo][k][1][0][1][3])

    for i in range(len(levels[epipedo][k][1])):

        temp = float(levels[epipedo][k][1][i][1][3])

        if yHigh < temp:
            yHigh = temp

    yHigh=str(yHigh)

    return yHigh

#Constructing the next level
def nextLevel(newleafs,node,previousLevel,epipedo):
    MBR=[]
    k=0
    t=0
    temp=[]
    nextLevel=[] # new level [node_id,[ptr,MBR]*n]
    counter=0

    leafs = len(previousLevel)
    newleafs = newleafs//node # total number of registries on each level (first level(4516), second (4516//28=161), third 161//28=6)

    ptr = 0
    lastIndex = len(previousLevel) - 1
    node_id = previousLevel[lastIndex][0] #node index


    for i in range(len(previousLevel)):

        t=t+1
        a = xLow(k,epipedo)
        MBR.append(a)

        c = xHigh(k,epipedo)
        MBR.append(c)

        b = yLow(k,epipedo)
        MBR.append(b)

        p = yHigh(k,epipedo)
        MBR.append(p)

        ptr = previousLevel[i][0] #node registries index
        temp.append([ptr,MBR]) # node registries
        MBR=[]

        leafs = len(previousLevel)
        k=k+1


        if t==node: #when t=28, append the node reggistries in the new level

            node_id = node_id +1
            nextLevel.append([node_id,temp])
            temp=[]
            counter = counter +1
            t=0


        if counter==newleafs and i == leafs-1: #for the last node, because its size is not 28 reggistries
            node_id = node_id +1
            nextLevel.append([node_id,temp])



    return nextLevel

#volume for each level
def volume(levels):
    epipedo = 0
    volumes = []
    for i in range(len(levels)):
        k =0
        vol = 0
        temp= []
        #edw vriskw tis plevres gia na parw to emvado kathe egrafis
        for j in range(len(levels[i])):

            #kalw tis sinartisis low kai High gia na vrw tis max k min times se kathe 28ada wste na vrw tis euthies gia na vrw to emvado

            x1 = float(xLow(k,epipedo))
            x2 = float(xHigh(k,epipedo))

            y1 = float(yLow(k,epipedo))
            y2 = float(yHigh(k,epipedo))

            x = x2-x1
            y = y2-y1

            vol = x*y

            temp.append(vol)



            k = k+1

        volumes.append(temp) #edw krataw ola ta volumes se kathe epipedo
        epipedo = epipedo +1


    mesos_oros_vol = []

    # edw vriskw to meso oro twv volumes se kathe epipedo kai epistrefw mia lista me auta dld stin thesi 0 tha einai o mesos oros twn volumes tou epipedou 0 klp
    for i in range(len(volumes)):
        sum=0


        for j in range(len(volumes[i])):

            sum = sum + volumes[i][j]


        mesos_oros = sum/len(volumes[i])

        mesos_oros_vol.append(mesos_oros)

    return mesos_oros_vol



#Rectangles Data
file_name = sys.argv[1]
file = open(file_name,'r')


rectangles=[]
for row in file:
    temp = row.split()
    rectangles.append([temp[0],temp[1],temp[2],temp[3],temp[4]]) #[id,x-low,x-high,y-low,y-high]

file.close()


#-----------------------
# Assume that each node has a capacity of 
# 1024 bytes and 
# each record needs 36 bytes to be saved.
# So 1024/36= node registries
#-----------------------

r_number = len(rectangles) # total rectangles (126437)
node_capacity = 1024
r_single = 36
node = floor(node_capacity//r_single) # each node has 28 registries

#-----------------------
# STR technique
#-----------------------

leafs = ceil(r_number/node) # Determine the number of leaf level pages (4516) 
S = int(sqrt(leafs))  # S vertical slices (67)
rectanglesSortedXlow = sorted(rectangles,key=lambda x: x[1]) # sort the rectangles by x-low coordinate

rectsOnSlices = S * node # A slice consists of a run of S*n consecutive rectangles from the sorted list (1876) 


slicedArray=[]
temp=[]
temp2=[]

t=0
counter = 0 # for knowing when is the last registry

#partion the rectangles in S vertical slices
for line in rectanglesSortedXlow:

    temp.append([line[0],line[1],line[2],line[3],line[4]])
    t=t+1
    if t==rectsOnSlices: #when it reaches S*n rectangles parse the temp list in the slicedArray
         t=0
         slicedArray.append(temp)
         temp=[]

    if counter ==len(rectanglesSortedXlow)-1: # for the last slice, beacause may contain fewer than S*n rectangles, so we parse the last rectangles
        slicedArray.append(temp)
        temp=[]

    counter=counter + 1


slicedArrayYsorted = []
# sort the rectangles from each slice by y-low coordinate
for i in range(len(slicedArray)):

    temp = sorted(slicedArray[i],key=lambda x: x[3])

    slicedArrayYsorted.append(temp)


#-----------------------
# pack the rectangles into nodes by 
# grouping them into runs 
# of length n=28 (the first n rectangles 
# into the first node, the next n 
# into the second node, and so on).
#-----------------------
temp=[]
arrayEpipedo0 = []
t=0
k=0
counter=0
temp2 = []
#for the last level of the R-tree,the leafs
for i in range(len(slicedArrayYsorted)):
    for j in range(len(slicedArrayYsorted[i])):

        t=t+1

         #seperate the object id from the MBR(rectangle coordinates)
        temp2.append(slicedArrayYsorted[i][j][1])
        temp2.append(slicedArrayYsorted[i][j][2])
        temp2.append(slicedArrayYsorted[i][j][3])
        temp2.append(slicedArrayYsorted[i][j][4])


        #the number 1, in the end of the list, is a flag to distinguish the registries from the nodes
        temp.append([slicedArrayYsorted[i][j][0],temp2,1])  
    
        temp2=[]

        if t==node: #creating the nodes, each node has 28 registries

            arrayEpipedo0.append(temp)
            temp=[]
            k=k+1
            t=0

        if counter == r_number -1: #the last node will have the remaining rectangles

            arrayEpipedo0.append(temp)
            temp=[]

        counter = counter + 1


level0=[]
node_id = 0

#make ids for each node
for i in range(len(arrayEpipedo0)):

    level0.append([node_id,arrayEpipedo0[i]])
    node_id = node_id +1


levels=[]
levels.append(level0) #this array will contain all the levels of the R-tree, we start by putting the level 0, which are the reggistries (leafs)
leafs = len(level0)
previousLevel = levels[0].copy() # temp array 

#---------------------
#We start building the rest of the tree
#---------------------

i=0
epipedo = 0

while leafs > node:
    i=i+1
    temp=[]

    temp = nextLevel(leafs,node,previousLevel,epipedo) #creating the next level
    epipedo = epipedo + 1

    levels.append(temp)

    leafs = len(levels[i]) #for creating a level we take the length of the previous level and we use it as leafs

    previousLevel = levels[i].copy()


#levels array explain :
#levels= [level0,level1,level2] ==> level0=[[node_id],[[ptr,MBR]*28]*4516], level1= [[node_id],[ptr,MBR]*28]*162], level2= [[node_id],[ptr,MBR]*28]*6]


if leafs<node: # For the last level

    temp = nextLevel(leafs,node,previousLevel,epipedo)

    levels.append(temp)


# rTree = [[node_id,MBR],[node_id,MBR],[node_id,MBR]...]

rTree = []

for i in range(len(levels)):
    for j in range(len(levels[i])):

        rTree.append(levels[i][j])



#calculate the volume of each level
volumes = []
volumes = volume(levels)

tree_size = str(len(levels))

node_id_rizas = str(len(rTree)-1) #node id of the top level of the rtree


with open("rtree.txt", "w") as file_output:

    file_output.write(node_id_rizas+ "\n")
    file_output.write(tree_size+ "\n")



    for i in range(len(rTree)):

        node_id = str(rTree[i][0])
        lists = str(rTree[i][1])

        node = str(len(rTree[i][1]))
        file_output.write(node_id + ' ' + node+ ' ' + lists+ "\n")
        file_output.write("\n")

file_output.close()


#-----------------------------------------------------------------------------------
#QUERIES
#-----------------------------------------------------------------------------------


#Queries file

file = open("query rectangles.txt",'r')
query_rectangles=[]
for row in file:
    temp = row.split()
    query_rectangles.append([temp[0],temp[1],temp[2],temp[3],temp[4]])




print("-------------------------------------------")
print("\n")

print("tree heigth:  ",len(levels))
print("\n")

for i in range(len(levels)):
    print("level  ",i,"         ",len(levels[i]),"  nodes")

print("\n")
print("Average volume for each level:")
print("\n")

for i in range(len(volumes)):
    print("level  ",i,"         ",volumes[i])




print("\n")


question1=[]
question1 = query1()
print("-------------------------------------------")
print("Registers That Intersect For Each Query Rectangle :")
print("column 1 = Total Registries, column 2 = Total nodes accesed")
print("\n")

print(question1)
print("\n")

question2=[]
question2=query2()
print("-------------------------------------------")
print("Registers That Are Inside in Each Query Rectangle :")
print("column 1 = Total Registries, column 2 = Total nodes accesed")
print("\n")

print(question2)
print("\n")

question3=[]
question3=query3()
print("-------------------------------------------")
print("Registers Tha Contain Eash Query Rectangle :")
print("column 1 = Total Registries, column 2 = Total nodes accesed")
print("\n")

print(question3)
print("\n")
print("-------------------------------------------")
