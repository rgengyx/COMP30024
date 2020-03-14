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
