from collections import deque
import random
from random_sparse_toopp_oppnear_ab_destack.square import *
from random_sparse_toopp_oppnear_ab_destack.util import *
import copy


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


def minimax(layout, depth, alpha, beta, maximizing_player, colour, our_colour):
    colour = "blacks" if colour == "whites" else "whites"

    opponent_colour = "blacks" if our_colour == "whites" else "whites"
    if depth == 0 or sum(t[0] for t in layout[opponent_colour]) == 0 or sum(t[0] for t in layout[our_colour]) == 0:
        if our_colour == "whites":
            return sum(t[0] for t in layout["whites"]) - sum(t[0] for t in layout["blacks"]), sum(
                t[0] for t in layout["blacks"]), None
        elif our_colour == "blacks":
            return sum(t[0] for t in layout["blacks"]) - sum(t[0] for t in layout["whites"]), sum(
                t[0] for t in layout["whites"]), None
    if maximizing_player:
        max_eval = -13
        max_opp_remain = 13
        max_action = None
        action_layout_list = generate_all_layouts(layout, colour, our_colour)

        for a, l, e in action_layout_list:

            eval, opp_remain, _ = minimax(l, depth - 1, alpha, beta, False, colour, our_colour)

            # Prioritize action that removes more.
            # if eval == max_eval:
            #     if opp_remain < max_opp_remain:
            #         max_action = a

            if eval > max_eval:
                max_eval = eval
                max_action = a

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, opp_remain, max_action
    else:
        min_eval = 13
        min_action = None
        action_layout_list = generate_all_layouts(layout, colour, our_colour)

        for a, l, e in action_layout_list:
            eval, opp_remain, _ = minimax(l, depth - 1, alpha, beta, True, colour, our_colour)
            if eval < min_eval:
                min_eval = eval
                min_action = a
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, opp_remain, min_action


def generate_all_layouts(layout, colour, our_colour):
    action_layout_list = []

    for token in layout[colour]:
        destinations = find_adjacent_squares(token, layout, colour)
        for destination in destinations:
            for numToken in range(token[0]):
                n = numToken + 1
                xa, ya = token[1], token[2]
                xb, yb = destination[1], destination[2]
                if xa == xb and ya == yb:
                    action = ("BOOM", (xa, ya))
                else:
                    action = ("MOVE", n, (xa, ya), (xb, yb))
                layout_copy = copy.deepcopy(layout)
                next_layout = update_layout(action, layout_copy, colour)

                current_eval = 0
                if our_colour == "whites":
                    current_eval = sum(t[0] for t in next_layout["whites"]) - sum(t[0] for t in next_layout["blacks"])
                elif our_colour == "blacks":
                    current_eval = sum(t[0] for t in next_layout["blacks"]) - sum(t[0] for t in next_layout["whites"])

                action_layout_list.append((action, next_layout, current_eval))

    return action_layout_list


def update_layout(action, layout, colour):
    # Update board layout
    if action[0] == "MOVE":
        colour_tokens = layout[colour]

        # Remove n tokens from starting stack
        n, start, end = action[1], action[2], action[3]
        for i in range(len(colour_tokens)):
            token = colour_tokens[i]
            if token[1] == start[0] and token[2] == start[1]:
                token[0] -= n
                break

        # Remove token with 0
        layout[colour] = [token for token in colour_tokens if token[0] != 0]

        # Add n tokens to ending stack
        contained = False
        n, start, end = action[1], action[2], action[3]
        for j in range(len(colour_tokens)):
            token = colour_tokens[j]
            if token[1] == end[0] and token[2] == end[1]:
                token[0] += n
                contained = True
                break

        if contained == False:
            layout[colour].append([n, end[0], end[1]])
    elif action[0] == "BOOM":
        coord = action[1]
        exploded_token_dict = get_exploded_dict(coord, layout)

        layout["whites"] = [white for white in layout["whites"] if
                            white not in exploded_token_dict["whites"]]
        layout["blacks"] = [black for black in layout["blacks"] if
                            black not in exploded_token_dict["blacks"]]

    return layout
