# Spatial Data Indexing and Querying

## Overview

Spatial data refers to data that directly or indirectly references a specific geographical location or area. It can also represent physical objects numerically using a geographic coordinate system. The goal of this project is to develop efficient **indexing techniques** and implement various **spatial queries** tailored for spatial data, using a specialized data structure called the **R-tree**.

In this project, the **Sort-Tile-Recursive (STR)** technique is used to build an R-tree in memory from a set of rectangles stored in a file. This tree structure is then used to efficiently answer spatial queries such as range intersections, range containment, and containment queries. 

## Methodology

### Sort-Tile-Recursive (STR) Technique

The **STR technique** is employed to efficiently build the R-tree by sorting and tiling rectangles based on their spatial properties:
1. **Sorting by x-coordinate:** The rectangles are sorted by their `x-low` value.
2. **Vertical Slices:** The sorted list is partitioned into vertical slices, each containing roughly the square root of the total number of leaves.
3. **Sorting by y-coordinate:** Each slice is further sorted by its `y-low` value, allowing the creation of R-tree leaf nodes.
4. **Node Creation:** The rectangles are grouped into nodes, forming the **leaf level** of the R-tree.
5. **R-tree Construction:** The internal nodes are built recursively by combining the leaf nodes, using the minimum bounding rectangles (MBRs) of the child nodes.

### R-tree

An **R-tree** is a hierarchical data structure optimized for spatial indexing, designed to efficiently handle spatial queries such as intersections, containment, and range queries. The key concept is that the objects are represented by their **Minimum Bounding Rectangles (MBRs)**, which are stored in nodes at different levels of the tree.

- **Leaf Nodes:** Store actual data objects and their MBRs.
- **Internal Nodes:** Store MBRs that enclose child nodes.
- **Root Node:** The root of the tree encloses all other nodes, and paths down the tree correspond to nested MBRs.

### Queries Implemented

This project implements three types of spatial queries using the R-tree:

1. **Range Intersection Query:** Given a query rectangle `q`, this query identifies all rectangles that intersect or have a common point with `q`.
2. **Range Containment Query:** Given a query rectangle `q`, this query identifies all rectangles that are entirely contained within `q`.
3. **Containment Query:** Given a query rectangle `q`, this query finds all rectangles that completely enclose `q`.

Each query type uses a recursive approach to traverse the R-tree, identifying relevant rectangles based on the MBRs stored in the nodes.

## Implementation Details

### Part 1: R-tree Construction

The R-tree is constructed by reading the spatial data from a file, organizing it in memory, and recursively building the tree.

#### Key Steps:
- **Node Capacity:** Each node can hold 1024 bytes, with 36 bytes per object entry (including coordinates and IDs).
- **Tree Representation:** Nodes are stored in an array-based structure where each node's ID is its index in the array. This simulates a sequence of blocks on disk, where the R-tree is stored.
- **Output File:** The constructed R-tree is written to a file (`rtree.txt`). This file contains:
  - **Node ID of the root.**
  - **Number of levels** in the tree.
  - **Nodes** represented by their IDs, the number of entries they contain, and the MBRs and pointers to either child nodes or objects.
  
#### Example Node Representation:
```
node-id, n, (ptr1, MBR1), (ptr2, MBR2), ..., (ptrn, MBRn)
```

Where `ptr` is a node ID (for internal nodes) or an object ID (for leaf nodes), and `MBR` contains the coordinates of the rectangle.

### Part 2: Query Implementation

1. **Range Intersection Query:**
   - **Functions:** `intersectedNodes`, `doOverlap`
   - **Process:** Starts at the root, recursively traversing nodes whose MBRs overlap with the query rectangle `q`. Once it reaches the leaf nodes, it reports the rectangles that intersect with `q`.

2. **Range Containment Query:**
   - **Functions:** `findLeafsFromNode`, `isInside`, `rectsInsideQuery`
   - **Process:** Recursively checks whether nodes and their MBRs are contained within the query rectangle `q`. If a node is fully contained, all its child rectangles are retrieved.

3. **Containment Query:**
   - **Functions:** `queryContainment`
   - **Process:** Starts from the leaf nodes and checks whether any of the rectangles fully contain the query rectangle `q`. Stops when an internal node does not contain the query.

### Tree Statistics

The program computes and prints various statistics about the constructed R-tree, including:
- **Tree Height:** The number of levels in the R-tree.
- **Number of Nodes per Level:** The distribution of nodes across different levels.
- **Average MBR Area:** The average area of MBRs at each level.

### Example of Tree Building

1. **Level Creation:**
   - The lowest level (leaf nodes) contains **4516 nodes**, each holding up to 28 entries, except the last node.
   - Internal nodes are created by recursively grouping the lower-level nodes based on their MBRs.

2. **Array Representation:**
   - The R-tree is represented as an array `rTree`, where each entry corresponds to a node and contains its ID, pointers, and MBRs.

## Query Execution

Each query is designed to minimize the number of nodes accessed and the number of rectangles processed. After constructing the R-tree, the queries can be efficiently evaluated using the MBR information stored in the internal nodes.

## Conclusion

This project demonstrates an efficient approach to spatial data indexing using R-trees, with a focus on range queries, containment, and intersection queries. The **Sort-Tile-Recursive (STR)** technique provides an efficient way to build the R-tree, and the hierarchical structure of the R-tree allows for rapid spatial query processing. This structure is particularly useful for large-scale spatial datasets where direct search methods would be too slow.

For more details on STR and R-tree construction, see:  
- Scott T. Leutenegger, J. M. Edgington, and Mario A. López. 1997. "STR: A Simple and Efficient Algorithm for R-Tree Packing." In ICDE. 497–506.  
  [Link to paper](https://apps.dtic.mil/sti/pdfs/ADA324493.pdf).
