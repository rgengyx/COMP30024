import sys
import json
import collections
import itertools
from collections import deque

from search.util import print_move, print_boom, print_board


def generate_all_squares_on_board():
    """ Return all squares on the board
    """
    return [(i, j) for i in range(8) for j in range(8)]


def generate_all_empty_squares(data):
    """ Return squares that white tokens can move to
    :param data: JSON input
    :type data: Dictionary
    """

    def token_exist_in_square(tokens, square):
        for token in tokens:
            if token[1] == square[0] and token[2] == square[1]:
                return True
        return False

    all_squares_on_board = generate_all_squares_on_board()
    blacks = data["black"]
    empty_squares = []
    for square in all_squares_on_board:
        if token_exist_in_square(blacks, square):
            continue
        empty_squares.append(square)

    return empty_squares


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


def print_actions(white, path):
    """Print move and boom actions from a given path to standard output
    :param path: list of (x, y)
    :type path: list
    """

    for i in range(len(path) - 1):
        print_move(white[0], path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])

    print_boom(path[i + 1][0], path[i + 1][1])


def board(data):
    whites, blacks = data['white'], data['black']

    board_dict = dict()

    for white in whites:
        if white[0] > 1:
            board_dict[tuple(white[1:])] = "W" + str(white[0])
        else:
            board_dict[tuple(white[1:])] = "W"

    for black in blacks:

        if black[0] > 1:
            board_dict[tuple(black[1:])] = "B" + str(black[0])
        else:
            board_dict[tuple(black[1:])] = "B"

    print_board(board_dict)


def get_3x3_surrounding_tokens(tokens, squares):
    _3x3_surrounding_tokens = []
    for square in squares:
        for token in tokens:
            if token[1] == square[0] and token[2] == square[1]:
                _3x3_surrounding_tokens.append(token)
                continue
    return _3x3_surrounding_tokens


def run_case(data):
    """ Run simulation
    :param data: JSON input
    :type data: Dictionary
    """

    whites, blacks = data['white'], data['black']

    empty_squares = generate_all_empty_squares(data)
    whites_adjacency_list = generate_adjacency_list(empty_squares, find_adjacent_squares)

    def get_exploded_tokens(coordinate, exploded_blacks):
        _3x3_surrounding_tokens = get_3x3_surrounding_tokens(blacks, find_3x3_surrounding_squares(coordinate))
        if not _3x3_surrounding_tokens:
            return

        for token in _3x3_surrounding_tokens:
            if token not in exploded_blacks:
                exploded_blacks.append(token)
                coordinate = tuple(token[1:])
                get_exploded_tokens(coordinate, exploded_blacks)

    # exploded_whites = []
    explode_dict = {}
    for empty_square in empty_squares:
        exploded_blacks = []
        get_exploded_tokens(empty_square, exploded_blacks)
        explode_dict[empty_square] = exploded_blacks
        # print(empty_square, exploded_blacks)

    # Recursively finding the destinations
    def rec(exploded_blacks, destinations, n, destinations_list):

        # if len(exploded_blacks) == len(blacks):
        #     print(destinations, n)
        #     return destinations

        if n >= 1:

            for empty_square in empty_squares:
                exploded_blacks_tmp = exploded_blacks.copy()
                for black in explode_dict[empty_square]:
                    if black not in exploded_blacks:
                        exploded_blacks_tmp.append(black)
                # if rec(exploded_blacks_tmp, destinations + [empty_square], n - 1) is not None:
                # print(len(rec(exploded_blacks_tmp, destinations + [empty_square], n - 1)) == len(blacks))
                if len(rec(exploded_blacks_tmp, destinations + [empty_square], n - 1, destinations_list)) == len(blacks):
                    destinations_list.append(destinations+[empty_square])
                    return destinations + [empty_square]
            return exploded_blacks
        else:
            return exploded_blacks

    destinations = []
    destinations_list = []
    rec([], destinations, len(whites), destinations_list)

    destinations = destinations_list[0]
    for i in range(len(destinations)):
        # This can be optimised as the first surrounding coordinate is always selected.
        start = tuple(whites[i][1:])
        end = destinations[i]
        shortest_path = bfs_shortest_path(whites_adjacency_list, start, end)
        print_actions(whites[i], shortest_path)


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    board(data)
    run_case(data)


if __name__ == '__main__':
    main()
