def generate_all_squares_on_board():
    """ Return all squares on the board
    """
    return [(1, i, j) for i in range(8) for j in range(8)]


def generate_all_empty_squares(data):
    """ Return squares that white tokens can move to
    :param data: JSON input
    :type data: Dictionary
    """

    def helper(square, colors):
        for color in colors:
            if square[1] == color[1] and square[2] == color[2]:
                return False
        return True

    all_squares_on_board = generate_all_squares_on_board()
    whites = [tuple(white) for white in data["white"]]
    blacks = [tuple(black) for black in data["black"]]

    emptys = []
    colors = blacks + whites
    for square in all_squares_on_board:
        if helper(square, colors):
            emptys.append(square)

    return sorted(emptys)


def find_adjacent_squares(n, square, layout):
    """Return a list of adjacent square coordinates
    :param square: (x, y)
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

    x, y = square[1], square[2]
    adjacent_coordinates = [(i, j) for i in range(x - n, x + n + 1) for j in range(y - n, y + n + 1) if
                            i >= 0 and j >= 0 and (i == x or j == y)]
    non_black_squares = sorted(layout["emptys"] + layout["whites"])
    # if (x,y) == (3,4):
    #     print([token for token in non_black_squares if tuple(token[1:]) in adjacent_coordinates])
    return [token for token in non_black_squares if tuple(token[1:]) in adjacent_coordinates]


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
    return [(i, j) for i in [x - 1, x, x + 1] for j in [y - 1, y, y + 1] if i >= 0 and j >= 0]


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
