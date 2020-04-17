def generate_all_squares_on_board():
    """ Return all squares on the board
    """
    return [[1, i, j] for i in range(8) for j in range(8)]


def generate_all_empty_squares(layout):
    """ Return squares that white tokens can move to
    :param layout: JSON input
    :type layout: Dictionary
    """

    def helper(square, colors):
        for color in colors:
            if square[1] == color[1] and square[2] == color[2]:
                return False
        return True

    all_squares_on_board = generate_all_squares_on_board()
    whites = [white for white in layout["whites"]]
    blacks = [black for black in layout["blacks"]]

    emptys = []
    colors = blacks + whites
    for square in all_squares_on_board:
        if helper(square, colors):
            emptys.append(square)

    return emptys


def find_adjacent_squares(square, layout):
    """Return a list of adjacent square coordinates
    :param square: (x, y)
    :type: tuple
    """

    n, x, y = square[0], square[1], square[2]
    adjacent_coordinates = [(i, j) for i in range(x - n, x + n + 1) for j in range(y - n, y + 1) if
                            0 <= i <= 7 and 0 <= j <= 7 and (i == x or j == y)]

    emptys = generate_all_empty_squares(layout)
    non_white_squares = emptys + layout["blacks"]
    return [token for token in non_white_squares if tuple(token[1:]) in adjacent_coordinates]


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


def get_3x3_surrounding_tokens(tokens, squares):
    _3x3_surrounding_tokens = []
    for square in squares:
        for token in tokens:
            if token[1] == square[0] and token[2] == square[1]:
                _3x3_surrounding_tokens.append(token)
                continue
    return _3x3_surrounding_tokens
