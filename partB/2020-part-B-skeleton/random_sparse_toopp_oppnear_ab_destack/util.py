from random_sparse_toopp_oppnear_ab_destack.square import *


def get_exploded_dict(coord, layout):
    def get_exploded_tokens(coordinate, exploded_tokens):

        _3x3_surrounding_white_tokens = get_3x3_surrounding_tokens(layout["whites"],
                                                                   find_3x3_surrounding_squares(coordinate))
        _3x3_surrounding_black_tokens = get_3x3_surrounding_tokens(layout["blacks"],
                                                                   find_3x3_surrounding_squares(coordinate))

        for token in _3x3_surrounding_black_tokens:
            if token not in exploded_tokens['blacks']:
                exploded_tokens['blacks'].append(token)
                coordinate = tuple(token[1:])
                get_exploded_tokens(coordinate, exploded_tokens)
        for token in _3x3_surrounding_white_tokens:
            if token not in exploded_tokens['whites']:
                exploded_tokens['whites'].append(token)
                coordinate = tuple(token[1:])
                get_exploded_tokens(coordinate, exploded_tokens)

    exploded_tokens = {"blacks": [], "whites": []}
    get_exploded_tokens(coord, exploded_tokens)

    return exploded_tokens
