import sys
import json
import collections

from search.util import print_move, print_boom, print_board


def generate_all_available_squares(data):
    """ Return a list of squares that white tokens can move to
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


def generate_adjacency_list(squares):
    """Return a dictionary of adjacency list
    :param squares: list of square coordinates
    :type squares: list
    """

    adjacency_list = {}
    for current_square in squares:
        adjacency_list[current_square] = []
        for other_square in squares:
            if other_square != current_square and other_square in find_adjacent_squares(current_square):
                adjacency_list[current_square].append(other_square)

    return adjacency_list


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


def find_destination_square(white, blacks):
    """Return coordinate of square which is the optimal destination for white token to move to
    """

    for black in blacks:

        # List of other black tokens in surrounding 3x3 area of current black token
        #
        #    ├───┼───┼───┼
        #    │{:}│{:}│{:}│
        #    ├───┼───┼───┼
        #    │{:}│   │{:}│
        #    ├───┼───┼───┼
        #    │{:}│{:}│{:}│
        #    ├───┼───┼───┼
        #

        blacks_in_3x3_surrounding_squares = [black3 for black3 in blacks for square in
                                             find_3x3_surrounding_squares(black[1:])
                                             if
                                             black3[1] == square[0] and black3[2] == square[1]]
        if not blacks_in_3x3_surrounding_squares:

            # # List of other black tokens in surrounding 5x5 area of current black token
            #
            #    ├───┼───┼───┼───┼───┼
            #    │{:}│{:}│{:}│{:}│{:}│
            #    ├───┼───┼───┼───┼───┼
            #    │{:}│{:}│{:}│{:}│{:}│
            #    ├───┼───┼───┼───┼───┼
            #    │{:}│{:}│   │{:}│{:}│
            #    ├───┼───┼───┼───┼───┼
            #    │{:}│{:}│{:}│{:}│{:}│
            #    ├───┼───┼───┼───┼───┼
            #    │{:}│{:}│{:}│{:}│{:}│
            #    ├───┼───┼───┼───┼───┼

            blacks_in_5x5_surrounding_squares = [black5 for black5 in blacks for square in
                                                 find_5x5_surrounding_squares(black[1:]) if
                                                 black5[1] == square[0] and black5[2] == square[1]]
            if not blacks_in_5x5_surrounding_squares:
                # Case 1:
                dx, dy = black[1] - white[1], black[2] - white[2]

                # Sign function, return either 1, 0, or -1
                sign = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)

                return black[1] - sign(dx), black[2] - sign(dy)
            else:
                # Case 2:
                blacks_in_5x5_squares = blacks_in_5x5_surrounding_squares + [black]
                all_surrounding_squares = [square for b in blacks_in_5x5_squares for square in
                                           find_3x3_surrounding_squares(b[1:])]

                # Find tuple with most occurrence
                most_common_square = collections.Counter(all_surrounding_squares).most_common()[0][0]
                return most_common_square


def find_adjacent_squares(coordinate):
    """Return a list of adjacent square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """
    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 1, x, x + 1] for j in [y - 1, y, y + 1] if
            i >= 0 and j >= 0 and (i, j) != (x, y) and (i == x or j == y)]


def find_3x3_surrounding_squares(coordinate):
    """Return a list of surrounding square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """
    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 1, x, x + 1] for j in [y - 1, y, y + 1] if i >= 0 and j >= 0 and (i, j) != (x, y)]


def find_5x5_surrounding_squares(coordinate):
    """Return a list of surrounding square coordinates
    :param coordinate: (x, y)
    :type: tuple
    """
    x, y = coordinate[0], coordinate[1]
    return [(i, j) for i in [x - 2, x - 1, x, x + 1, x + 2] for j in [y - 2, y - 1, y, y + 1, y + 2] if
            i >= 0 and j >= 0 and
            (i, j) != (x, y)]


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

    white, blacks = data['white'][0], data['black']
    destination_square = find_destination_square(white, blacks)

    squares = generate_all_available_squares(data)
    adjacency_list = generate_adjacency_list(squares)

    start = tuple(white[1:])
    end = destination_square
    shortest_path = bfs_shortest_path(adjacency_list, start, end)
    print_actions(white, shortest_path)


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    run_case(data)


if __name__ == '__main__':
    main()
