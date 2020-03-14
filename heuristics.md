## Strategy
1. Identify connected components in undirected graph
    1. If no. of connected components <= no. of whites, move whites to the nearest
    components and explode
    2. If no. of connected components > no. of whites, identify explosion break points.


### Case 1
* Find squares that could make the black token explode (Any square in 3x3 of the black token)
* Move to the one with shortest path.

### Case 2
* Determine the break point of explosion series as a destination square
* Use breath-first-search to find the shortest path

### Case 3: 
* Same process as case 2 but with multiple destination squares

### Case 4:


