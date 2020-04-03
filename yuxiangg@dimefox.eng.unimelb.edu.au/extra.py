def find_nearest_square(white, squares):
    """ Return nearest square to a given white token using Manhattan distance

    :param white: white token information
    :type white: list
    :param squares: list of tuples of coordinates (x, y)
    :type squares: list
    :return: nearest square
    """
    min_manhattan_distance = 16  # 8+8=16
    index_of_nearest_square = 0
    for i in range(len(squares)):
        dx, dy = white[1] - squares[i][0], white[2] - squares[i][1]
        manhattan_distance = abs(dx) + abs(dy)
        if manhattan_distance < min_manhattan_distance:
            min_manhattan_distance = manhattan_distance
            index_of_nearest_square = i

    return squares[index_of_nearest_square]


def find_destination_squares(white, blacks):
    """Return coordinate of square which is the optimal destination for white token to move to
    """

    destination_squares = []
    possible_destination_squares = []

    for black in blacks:

        blacks_in_3x3_surrounding_squares = [black3 for black3 in blacks for square in
                                             find_3x3_surrounding_squares(black[1:])
                                             if
                                             black3[1] == square[0] and black3[2] == square[1]]

        if not blacks_in_3x3_surrounding_squares:
            blacks_in_5x5_surrounding_squares = [black5 for black5 in blacks for square in
                                                 find_5x5_surrounding_squares(black[1:]) if
                                                 black5[1] == square[0] and black5[2] == square[1]]
            if not blacks_in_5x5_surrounding_squares:
                # Single black in 5x5 which needs to be exploded individually.
                #
                #    ├───┼───┼───┼
                #    │   │   │{:}│
                #    ├───┼───┼───┼
                #    │   │   │   │
                #    ├───┼───┼───┼
                #    │   │   │   │
                #    ├───┼───┼───┼
                #
                dx, dy = black[1] - white[1], black[2] - white[2]

                # Sign function, return either 1, 0, or -1
                sign = lambda x: 1 if x > 0 else (-1 if x < 0 else 0)
                destination_squares.append((black[1] - sign(dx), black[2] - sign(dy)))
            else:
                # There must be a break point which must be one of the destinations.
                #
                #    ├───┼───┼───┼
                #    │   │   │{:}│
                #    ├───┼───┼───┼
                #    │   │   │   │
                #    ├───┼───┼───┼
                #    │{:}│   │   │
                #    ├───┼───┼───┼
                #

                blacks_in_5x5_squares = blacks_in_5x5_surrounding_squares + [black]
                all_surrounding_squares = [square for b in blacks_in_5x5_squares for square in
                                           find_3x3_surrounding_squares(b[1:])]

                # Find tuple with most occurrence
                most_common_square = collections.Counter(all_surrounding_squares).most_common()[0][0]
                destination_squares.append(most_common_square)

        else:
            # There must be at least one black in explosion area of another.
            #
            #    ├───┼───┼───┼
            #    │   │   │{:}│
            #    ├───┼───┼───┼
            #    │   │{:}│   │
            #    ├───┼───┼───┼
            #    │   │   │   │
            #    ├───┼───┼───┼
            #

            possible_destination_squares += [black3 for black3 in blacks for square in
                                             find_3x3_surrounding_squares(black[1:])
                                             if not (black3[1] == square[0] and black3[2] == square[1])]

    return destination_squares
