from collections import deque

def generate_adjacency_list(white, layout, adjacency_func):
    """Return a dictionary of adjacency list
    :param squares: list of square coordinates
    :type squares: list
    """

    non_black_squares = sorted(layout["emptys"] + layout["whites"])
    adjacency_list = {}
    for current_square in non_black_squares:
        adjacency_list[current_square] = []
        for other_square in non_black_squares:
            if other_square != current_square and other_square in adjacency_func(white[0], current_square,
                                                                                 layout):
                adjacency_list[current_square].append(other_square)

    return adjacency_list


def bfs_shortest_path(blacks, graph, start, end):
    """Return shortest path from start to end in form of a list of coordinates
    :param graph: dictionary of adjacency list
    :param start: coordinate (x, y)
    :param end: coordinate (x, y)
    """

    # https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])

    visited = []

    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in visited:
            visited.append(node)
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue

        for adjacent in graph.get(node, []):
            inbetween = []

            if adjacent[1] == node[1]:
                if adjacent[2] < node[2]:
                    for i in range(node[2] - adjacent[2] - 1):
                        inbetween.append((adjacent[1], adjacent[2] + i + 1))
                else:
                    for i in range(adjacent[2] - node[2] - 1):
                        inbetween.append((adjacent[1], node[2] + i + 1))

            else:
                if adjacent[1] < node[1]:
                    for i in range(node[1] - adjacent[1] - 1):
                        inbetween.append((adjacent[2], adjacent[1] + i + 1))
                else:
                    for i in range(adjacent[1] - node[1] - 1):
                        inbetween.append((adjacent[2], node[1] + i + 1))

            def helper():
                if inbetween == []:
                    return True

                for token in inbetween:
                    if token in [tuple(token[1:]) for token in blacks]:
                        return True
                return False

            if helper():
                new_path = list(path)
                if adjacent in new_path:
                    continue
                new_path.append(adjacent)
                if sorted(set(new_path), key=lambda k: (k[0], k[1])) == sorted(visited):
                    continue
                queue.append(new_path)


def dfs(graph, start):
    # https://github.com/TheAlgorithms/Python/blob/9eac17a4083ad08c4bb0520cb0b8e5ce385f9ce0/graphs/dfs.py
    explored, stack = set(), [start]
    while stack:
        v = (
            stack.pop()
        )  # one difference from BFS is to pop last element here instead of first one
        if v in explored:
            continue

        explored.add(v)

        for w in graph[v]:
            if w not in explored:
                stack.append(w)
    return explored


def bfs(graph, start):
    # https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/
    # keep track of all visited nodes
    explored = []
    # keep track of nodes to be checked
    queue = [start]

    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        if node not in explored:
            # add node to list of checked nodes
            explored.append(node)
            neighbours = graph[node]

            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)
    return explored


def connected_components(graph):
    """Return a list of connected black tokens. e.g. [[(0, 2), (1, 1), (2, 0)], [(4, 7)], [(7, 7)]]
    """

    # https://stackoverflow.com/questions/10301000/python-connected-components
    seen = set()

    for root in graph.keys():
        if root not in seen:
            seen.add(root)
            component = []
            queue = deque([root])
            while queue:
                node = queue.popleft()
                component.append(node)
                for neighbor in graph[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        queue.append(neighbor)
            yield component
