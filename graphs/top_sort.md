# Topological Sorting
Aside from DFS and BFS, the most common graph concept that interviews will test is topological sorting. The objective of this algorithm is to produce an ordering of nodes in a directed graph such that the direction of nodes is respected. 

A **topological sort** is an ordering of nodes for a directed acyclic graph (DAG) such that for every directed edge _uv_ from vertex _u_ to vertex _v_, _u_ comes before _v_ in the ordering.

## Example
An application of this algorithm would be trying to order a sequence of tasks given their dependencies on other tasks. In this application, there is an directed edge from _u_ to _v_ if task _u_ must be completed before task _v_ can start. For example, when cooking, we need to turn on the oven (task _u_) before we can bake the cookies (task _v_).

<img src="https://github.com/codepath/compsci_guides/blob/graphs/graphs/figures/top_sort_graph.png"/>

## Implementation:
The algorithm behind how to do this is simply a modification of DFS.

### Graph with no cycles
```python
from collections import deque

def top_sort(graph):
  sorted_nodes, visited = deque(), set()
  for node in graph.keys():
      if node not in visited:
        dfs(graph, node, visited, sorted_nodes)
  return list(sorted_nodes)
 

def dfs(graph, start_node, visited, sorted\_nodes):
  visited.add(start_node)
  if start_node in graph:
      neighbors = graph[start_node]
  for neighbor in neighbors:
      if neighbor not in visited:
          dfs(graph, neighbor, visited, sorted_nodes)
  sorted_nodes.appendleft(start_node)
```

