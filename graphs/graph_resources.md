## Glossary
1. **vertex (node):** used to represent a single data point
2. **edge:** a connection between a pair of vertices
3. **neighbor:** a neighbor node is a node that is directly connected to another node by an edge
4. **directed graph:** a graph in which all edges have direction
5. **undirected graph:** a graph in which all edges have no direction
6. **path:** a sequence of vertices connected by edges
7. **cycle:** a paththat begins and ends at the same vertex
8. **cyclic graph:** a graph which contains at least one cycle
9. **acyclic graph:** a graph whichdoes not contain a cycle
10. **adjacency list:** an approach to representing graphs in which each node stores a list of its adjacent vertices
11. **edge set/list:** an approach to representing graphs in which a graph is a collection of all its edges
12. **adjacency matrix:** an approach to representing graphs in which a graph with _n_ nodes is storeed as an _n_ by _n_ boolean matrix, where matrix\[_u_\]\[_v_\] is true if an edge exists between node _u_ to node _v_.
13. **breadth first search:** pick an arbitrary node as the root and explore each of its neighbors before visiting their children
14. **depth first search:** start with an arbitrary node as a root and explore each neighbor fully before exploring the root's next neighbor
15. **topological sort:** an ordering of nodes for a directed acyclic graph (DAG) such that for every directed edge _uv_ from vertex _u_ to vertex _v_, _u_ comes before _v_ in the ordering.
16. **sink nodes:** in a DAG, a sink node has no outgoing edges
17. **source nodes:** in a DAG, a source node only has outgoing edges
18. **directed acylic graph (DAG):** a directed graph in which there are *no* cycles


## Extra graph algorithms
**NOTE**: This section covers algorithms that will generally not come up in interviews.
### Union find, disjoint sets
* Guide: https://www.hackerearth.com/practice/notes/disjoint-set-union-union-find/
* Interview question bank: https://leetcode.com/tag/union-find/

### Shortest paths algorithms
* Guide: https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/tutorial/
* Interview question bank: https://www.hackerearth.com/practice/algorithms/graphs/shortest-path-algorithms/practice-problems/

### Minimum spanning tree algorithms
* Guide: https://www.hackerearth.com/practice/algorithms/graphs/minimum-spanning-tree/tutorial/
* Interview question bank: https://www.hackerearth.com/practice/algorithms/graphs/minimum-spanning-tree/practice-problems/
