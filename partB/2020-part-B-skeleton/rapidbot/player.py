import random
from rapidbot.square import *


class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.

        self.colour = colour
        # Initial layout
        self.layout = {
            "whites": [[1, 0, 1], [1, 1, 1], [1, 3, 1], [1, 4, 1], [1, 6, 1], [1, 7, 1],
                       [1, 0, 0], [1, 1, 0], [1, 3, 0], [1, 4, 0], [1, 6, 0], [1, 7, 0]],
            "blacks": [[1, 0, 7], [1, 1, 7], [1, 3, 7], [1, 4, 7], [1, 6, 7], [1, 7, 7],
                       [1, 0, 6], [1, 1, 6], [1, 3, 6], [1, 4, 6], [1, 6, 6], [1, 7, 6]]
        }

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it

        white = random.choice(self.layout["whites"])
        print("*****", white, self.layout["whites"])
        destination = random.choice(find_adjacent_squares(white, self.layout))

        n, xa, ya = white[0], white[1], white[2]
        xb, yb = destination[1], destination[2]
        if xa == xb and ya == yb:
            return ("BOOM", (xa, ya))
        return ("MOVE", n, (xa, ya), (xb, yb))

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.

        # Update board layout
        if action[0] == "MOVE":
            colour_tokens = self.layout[colour + "s"]

            # Remove n tokens from starting stack
            for i in range(len(colour_tokens)):
                n, start, end = action[1], action[2], action[3]
                token = colour_tokens[i]
                if token[1] == start[0] and token[2] == start[1]:
                    token[0] -= n
                    break

            # Remove token with 0
            self.layout[colour + "s"] = [token for token in colour_tokens if token[0] != 0]

            # Add n tokens to ending stack
            contained = False
            for j in range(len(colour_tokens)):
                n, start, end = action[1], action[2], action[3]
                token = colour_tokens[j]
                if token[1] == end[0] and token[2] == end[1]:
                    token[0] += n
                    contained = True
                    break

            print("j {}, colour_tokens {}".format(j, len(colour_tokens)))
            if contained == False:
                self.layout[colour + "s"].append([n, end[0], end[1]])
        elif action[0] == "BOOM":
            coord = action[1]
            print("------", coord, self.layout)
            exploded_token_dict = self.get_exploded_dict(coord, self.layout)

            self.layout["whites"] = [white for white in self.layout["whites"] if
                                     white not in exploded_token_dict["whites"]]
            self.layout["blacks"] = [black for black in self.layout["blacks"] if
                                     black not in exploded_token_dict["blacks"]]

        print("^^^^^^^^^^^^", self.layout)

    def get_exploded_dict(self, coord, layout):

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
