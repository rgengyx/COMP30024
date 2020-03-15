import sys
import json
import collections
import itertools
from collections import deque

from search.util import print_move, print_boom, print_board


def generate_all_empty_squares(data):
    """ Return a list of square coordinates that white tokens can move to
    :param data: JSON input
    :type data: Dictionary
    """

    def check_if_coordinates_exist_in_tokens(tokens, coordinate):
        """Return True if a token is already in a coordinate False otherwise
        """

        for token in tokens:
            if token[1] == coordinate[0] and token[2] == coordinate[1]:
                return True
        return False

    squares = []
    for i in range(8):
        for j in range(8):
            coordinate = (i, j)
            blacks = data['black']
            if check_if_coordinates_exist_in_tokens(blacks, coordinate):
                continue
            else:
                squares.append(coordinate)

    return squares


def generate_adjacency_list(squares, direction_func):
    """Return a dictionary of adjacency list
    :param squares: list of square coordinates
    :type squares: list
    """

    adjacency_list = {}
    for current_square in squares:
        adjacency_list[current_square] = []
        for other_square in squares:
            if other_square != current_square and other_square in direction_func(current_square):
                adjacency_list[current_square].append(other_square)

    return adjacency_list


def find_adjacent_squares(coordinate):
    """Return a list of adjacent square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """

    # List of other coordinates in adjacent squares
    #
    #    ├───┼───┼───┼
    #    │   │{:}│   │
    #    ├───┼───┼───┼
    #    │{:}│   │{:}│
    #    ├───┼───┼───┼
    #    │   │{:}│   │
    #    ├───┼───┼───┼
    #

    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 1, x, x + 1] for j in [y - 1, y, y + 1] if
            i >= 0 and j >= 0 and (i, j) != (x, y) and (i == x or j == y)]


def find_3x3_surrounding_squares(coordinate):
    """Return a list of surrounding square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """

    # List of coordinates in surrounding 3x3 squares
    #
    #    ├───┼───┼───┼
    #    │{:}│{:}│{:}│
    #    ├───┼───┼───┼
    #    │{:}│   │{:}│
    #    ├───┼───┼───┼
    #    │{:}│{:}│{:}│
    #    ├───┼───┼───┼
    #

    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 1, x, x + 1] for j in [y - 1, y, y + 1] if i >= 0 and j >= 0 and (i, j) != (x, y)]


def find_5x5_surrounding_squares(coordinate):
    """Return a list of surrounding square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """

    # # List of coordinates in surrounding 5x5 squares
    #
    #    ├───┼───┼───┼───┼───┼
    #    │{:}│{:}│{:}│{:}│{:}│
    #    ├───┼───┼───┼───┼───┼
    #    │{:}│   │   │   │{:}│
    #    ├───┼───┼───┼───┼───┼
    #    │{:}│   │   │   │{:}│
    #    ├───┼───┼───┼───┼───┼
    #    │{:}│   │   │   │{:}│
    #    ├───┼───┼───┼───┼───┼
    #    │{:}│{:}│{:}│{:}│{:}│
    #    ├───┼───┼───┼───┼───┼

    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 2, x - 1, x, x + 1, x + 2] for j in [y - 2, y - 1, y, y + 1, y + 2] if
            i >= 0 and j >= 0 and
            (i, j) != (x, y) and ((i, j) not in find_3x3_surrounding_squares((x, y)))]


def bfs_shortest_path(graph, start, end):
    """Return shortest path from start to end in form of a list of coordinates
    :param graph: dictionary of adjacency list
    :param start: coordinate (x, y)
    :param end: coordinate (x, y)
    """

    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def connected_components(graph):
    """Return a list of connected black tokens. e.g. [[(0, 2), (1, 1), (2, 0)], [(4, 7)], [(7, 7)]]
    """
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


def find_explosion_break_point(components):
    """
    """
    black_coordinates = list(itertools.chain.from_iterable(components.values()))

    def find_index_of_list_coordinate_is_in(cps, coordinate):
        for l in cps.values():
            if coordinate in l:
                return list(cps.values()).index(l)

    explosion_break_points = set()
    exploded_components = set()
    for current in black_coordinates:
        for other in black_coordinates:
            if other not in components[
                find_index_of_list_coordinate_is_in(components, current)] and other in find_5x5_surrounding_squares(
                current):
                # The is an explosion break point
                x, y = int((other[0] + current[0]) / 2), int((other[1] + current[1]) / 2)
                explosion_break_points.add((x, y))

                exploded_components.add(find_index_of_list_coordinate_is_in(components, current))
                exploded_components.add(find_index_of_list_coordinate_is_in(components, other))

    return list(explosion_break_points), list(exploded_components)


def print_actions(white, path):
    """Print move and boom actions from a given path to standard output
    :param path: list of (x, y)
    :type path: list
    """

    for i in range(len(path) - 1):
        print_move(white[0], path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])

    print_boom(path[i + 1][0], path[i + 1][1])


def run_case(data):
    """ Run simulation
    :param data: JSON input
    :type data: Dictionary
    """

    whites, blacks = data['white'], data['black']

    # Initialise adjacency lists
    empty_squares = generate_all_empty_squares(data)
    whites_adjacency_list = generate_adjacency_list(empty_squares, find_adjacent_squares)
    black_coordinates = [tuple(black[1:]) for black in blacks]
    blacks_adjacency_list = generate_adjacency_list(black_coordinates,
                                                    find_3x3_surrounding_squares)

    # Find connected components of blacks
    components = dict(zip(itertools.count(), connected_components(blacks_adjacency_list)))

    # Start whites actions
    break_points, exploded_components = find_explosion_break_point(components)

    for exploded_component in exploded_components:
        del components[exploded_component]

    for i in range(len(break_points)):
        start = tuple(whites[i][1:])
        end = break_points[i]
        shortest_path = bfs_shortest_path(whites_adjacency_list, start, end)
        print_actions(whites[i], shortest_path)

    # This can be optimised as whites are selected in predetermined order.
    for i in range(len(components)):
        surrounding_coordinates = [surrounding_coordinate for coordinate in components[i] for
                                   surrounding_coordinate
                                   in
                                   find_3x3_surrounding_squares(coordinate) if
                                   surrounding_coordinate not in black_coordinates]

        # This can be optimised as the first surrounding coordinate is always selected.
        start = tuple(whites[i][1:])
        end = surrounding_coordinates[0]
        shortest_path = bfs_shortest_path(whites_adjacency_list, start, end)
        print_actions(whites[i], shortest_path)


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    run_case(data)


if __name__ == '__main__':
    main()
