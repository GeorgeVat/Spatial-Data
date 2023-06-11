# Spatial-Data

Spatial data refers to any type of data that directly or indirectly references a specific geographical area or location. It can be referred to as geospatial data or geographic information. Spatial data can also represent a physical object numerically using a geographic coordinate system. The objective of this project is to develop indexing techniques and queries specifically designed for spatial data.

In this project, the sort-tile-recursive (STR) technique is implemented to read rectangles from a file and construct an R-tree in memory for efficient spatial indexing. The technique involves sorting all the rectangles based on their x-low value and then reading sections of the sorted list or file that correspond to the square root of the total number of leaves in the tree. These sections are further sorted based on the y-low value, gradually creating the leaves of the R-tree. Once the R-tree is built, range queries are implemented to perform spatial operations.

Three types of queries are addressed in this project:
1) Range intersection query: Given a rectangle (q) in space, the goal is to find the rectangles that intersect or have a common point with q.
2) Range inside query: Given a rectangle (q) in space, the goal is to find the rectangles contained entirely within q.
3) Containment query: Given a rectangle (q) in space, the goal is to find the rectangles that completely contain q.

For each of the above query types, a function is implemented that utilizes the R-tree to count the number of results and the number of R-node nodes accessed during the query evaluation. The query rectangles are provided in the query_rectangles.txt file, which includes the query ID, x-low, x-high, y-low, and y-high values for each rectangle.

Background
STR
Consider a fc-dimensional data set of r hyper-rectangles. A hyper-rectangle is defined by k intervals of the form [A, B] and is the locus of points whose i-th coordinate falls inside the 2-th interval, for all 1 < i < k. 
STR is best described recursively with k = 2 providing the base case. (The case k = 1 is already handled well by regular B-trees.) Accordingly, we first consider a set of rectangles in the plane. The basic idea is to "tile" the data space using (r/n) vertical slices so that each slice contains enough rectangles to pack roughly (r/n) nodes. Once again we assume coordinates are for the center points of the rectangles. Determine the number of leaf level pages P = r/n and let S = P. Sort the rectangles by x-coordinate and partition them into S vertical slices. A slice consists of a run of S *n consecutive rectangles from the sorted list. Note that 
the last slice may contain fewer than S *n rectangles. Now sort the rectangles of each slice by y-coordinate and pack them into nodes by grouping them into runs of length n (the first n rectangles into the first node, the next n into the second node, and so on). 
R-tree
An R-tree is a hierarchical data structure derived from the B-tree and designed for efficient execution of intersection queries. R-trees store a collection of rectangles which can change over time through insertions and deletions. Arbitrary geometric objects are handled by representing each object by its minimum bounding rectangle, i.e., the smallest upright rectangle which encloses the object. R-trees generalize easily to dimensions higher than two, but for notational simplicity we review only the two dimensional case. 
Each node of the R-tree stores a maximum of n entries. Each entry consists of a rectangle R and a pointer P. For nodes at the leaf level, R is the bounding box of an actual object pointed to by P. At internal nodes, R is the minimum bounding rectangle (MBR) of all rectangles stored in the subtree pointed to by P. Note that every path down through the tree corresponds to a sequence of nested rectangles, the last of which contains an actual data object. Note also that rectangles at any level may overlap and that an R-tree created from a particular set of objects is by no means unique. 
To perform a query Q, all rectangles that intersect the query region must be retrieved and examined (regardless of whether they are stored in an internal node or a leaf node). This retrieval is accomplished by using a simple recursive procedure that starts at the root node and which may follow several paths down through the tree. A node is processed by first retrieving all rectangles stored at that node which intersect Q. If the node is an internal node, the subtrees corresponding to the retrieved rectangles are searched recursively. Otherwise, the node is a leaf node and the retrieved rectangles (or the data objects themselves) are simply reported. 

For more about STR and R-Tree : Scott T. Leutenegger, J. M. Edgington, and Mario A. López. 1997. STR: A Simple and Efficient Algorithm for R-Tree Packing. In ICDE. 497–506. 
 https://apps.dtic.mil/sti/pdfs/ADA324493.pdf 
Part 1 (R-tree construction)

Assume that  each node has a capacity of 1024 bytes and that we use 4 bytes for each object-id or node-id and one double (8 bytes) for each coordinate. So each record needs 36 bytes to be saved.
In my implementation i read the data from the file, sort it and build the tree in memory. I will use an array structure to store the nodes. As i create the tree, i will add the nodes to the array and the node-id of a node will be its location in the array. In this way i  simulate a sequence of blocks on the disk that store the tree.
The program also, should print statistics for the tree: height (ie number of levels), number of nodes in each level, and average area of MBRs in each level.
It should also write the tree representation in an rtree.txt output text file. The first line will have only the node-id of the tree root. The second row will have only the number of levels of the tree. Each of the following lines in the file will contain the data of a node in the following format:
node-id, n, (ptr1, MBR1), (ptr2, MBR2), ..., (ptrn, MBRn)
The node-id is the id of the node, n is the number of entries in the node, followed by n entries in the node. In each record, ptr is either a node-id (if the record points to an intermediate node) or an object-id if the record points to an object. The MBR is a sequence of 4 doubles <x-low> <x-high> <y-low> <y-high>.
In a practical part, I have created the list of registries sorted by x low and then sliced it in S vertical slices, then I go to each slice and sort it by ylow. For each slice now, I pack the sorted registries per 28 packs. So I create the last level of the tree (ie the leaves), where it will have 4516 nodes (all nodes will have 28 entries except the last one). Also at this level I put another cell where it will have an ID to separate the nodes from the leaves (this will help me for part 2).
For the other levels I follow a different approach as the MBRs of the current leaves that we will calculate will be different, because from each node we take the max and min values from y and x as the new coordinates. So I implement a function (nextLevel ())  which returns a list from the next level with its new entries each time. This way i create the array levels [] which will have the following format: 
levels = [level0, level1, level2…], where levels[0] = [[node_id], [[ptr, MBR] * 28] * 4516], levels [1] = [[node_id], [ptr, MBR] * 28] * 162], level [2] = [[node_id], [ptr, MBR] * 28] * 6] etc .. 
The yHigh, yLow, xHigh, xLow functions are also used in this function where they return the appropriate x, y each time. These functions also take as an argument the epipedo (which is an index that shows every time the level), because the first time they are called they will have to search within levels [0] for values. Then the level increases by 1 and they look to the next level.
After the array levels [] is created then I bring it in the form of the tree. I create an array rTree [] where it will have the following format:
 rTree= [node_id=0,[ptr,[MBR]]*n], [node_id=1,[ptr,[MBR]]*n] …… [node_id=4684,[ptr,[MBR]]*n]
After I have created my tree then I implement the first tasks of the first part, I calculate the area of each level and calculate the height of the tree.

Part 2 (Queries)
Question 1 : Range intersection query: a rectangle q is given in space and the goal is to find the rectangles that intersect (for example, have a common point with) q.

Functions: intersectedNodes, doOverlap 
The first function starts with the node of the root and if it finds that one of its nodes overlaps (via the doOverlap function), then it returns a new value in the node_overlapping field (This value will essentially be the node of its children node that you check each time) and does the same thing until it reaches a leaf. When it reaches a leaf it appends its node_id and continues until the recursion ends. So in the end is returned an array where it contains the node_id of the leafs that intersect. The doOverlap function takes as an argument the index of the query rectangle and the values x, y min/max from each MBR that is checked each time. The logic is that it checks the cases that do not overlap and returns False if it enters these conditions, otherwise return True which means that it overlaps.

Question 2 : Range inside query: a rectangle q is given in space and the goal is to find the rectangles contained in q.
Functions: findLeafsFromNode, isInside,rectsInsideQuery
This function checks recursively the node you give it each time if it is nested (ie contained inside the query rectangle) and if it is a leaf or a node. In case it is not nested and not a leaf then it calls itself again but with a different node, more specifically with its child node (ie it goes down level until it finds a node or a leaf that is inside the query). If it finds a node that is nested then it gives this node to the findLeafsFromNode function which finds all the entries contained in this node (i.e. if I give as an argument to this function my root, it returns the total entries of the tree i.e. 126437) . Then after returning these records I append them one by one to leafsInsideQ. LeafsInsideQ will eventually contain the total records contained within the query rectangle.

Question 3 : Containment query: a rectangle q is given in space and the goal is to find the rectangles that contain q
Functions: queryContainment
For this question I create a function that starts from the leafs and checks linearly if they contain the query. When it finds a node that is not a leaf, it breaks.

