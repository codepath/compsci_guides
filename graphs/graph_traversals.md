# Graph traversals
These traversal algorithms are conceptually the same as the ones introduced in the tree section.

## Depth first search
In a **depth first search**, we start with an arbitrary node as a root and explore each neighbor fully before exploring the next one. 

<img src="https://github.com/codepath/compsci_guides/blob/graphs/graphs/figures/dfs_graph.png" width="544" height="350"/>

**Implementation:**
```python
'''
Assuming we have a directed graph represented with an adjacency list.

Example:
graph = {'A': ['B', 'C'],  
 'B': ['D', 'E'],  
 'C': ['F'],  
 'E': ['F']}
'''
  
def depth_first_search(graph, start):  
    visited, stack = set(), [start] 
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            # If a node with no outgoing edges won't be 
            # included in the adjacency list, we need to check
            if vertex in graph:
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        stack.append(neighbor)
    return visited
```

**Runtime:** O(V + E)

**Example interview question using DFS:**
* [Detect a cycle in a graph](https://www.geeksforgeeks.org/detect-cycle-in-a-graph/) 

## Breadth first search
In **breadth first search**, we pick an arbitrary node as the root and explore each of its neighbors before visiting their children. Breadth first search is the better of the two algorithms at finding the shortest path between two nodes.

<img src="https://github.com/codepath/compsci_guides/blob/graphs/graphs/figures/bfs_graph.png" width="679" height="350"/>

**Implementation:**
```python
from collections import deque

'''
Assuming we have a directed graph represented with an adjacency list.

Example:
graph = {'A': ['B', 'C'],  
 'B': ['D', 'E'],  
 'C': ['F'],  
 'E': ['F']}
'''
  
def breadth_first_search(graph, start):  
    visited, queue = set(), deque(start)
    while queue:
        vertex = queue.popLeft()
            visited.add(vertex)
            # If a node with no outgoing edges won't be 
            # included in the adjacency list, we need to check
            if vertex in graph:
                for neighbor in graph[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
    return visited
```


**Example interview question using BFS:**


**Runtime**: O(V + E)
