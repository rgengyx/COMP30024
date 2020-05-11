import random
from aggressive2_sparse_ab2_destack_endgame_escape.square import *
from aggressive2_sparse_ab2_destack_endgame_escape.graph import *


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

        def find_nearby_opponents():
            nearby = {"whites":[],"blacks":[]}
            for our in self.layout[our_colour]:
                surroundings = find_nxn_surrounding_squares(our[1:], our[0])
                for surrounding in surroundings:
                    for opponent in self.layout[opponent_colour]:
                        if opponent[1] == surrounding[0] and opponent[2] == surrounding[1]:
                            nearby[our_colour].append(our)
                            nearby[opponent_colour].append(opponent)
            return nearby

        # def find_sparse_destination():
        #     destinations = find_adjacent_squares(token, self.layout, our_colour)
        #     destinations = [d for d in destinations if not (xa == d[1] and ya == d[2])]
        #     min_destination = None
        #     min_exploded_num = 13
        #
        #     # Find a destination that causes least explosion of our token and most explosion of opponent's token
        #     for destination in destinations:
        #         coord = destination[1:]
        #         layout = copy.deepcopy(self.layout)
        #         layout[our_colour].remove(token)
        #
        #         exist = False
        #         for our in layout[our_colour]:
        #             if our[1] == destination[1] and our[2] == destination[2]:
        #                 our[0] += token[0]
        #                 exist = True
        #                 break
        #
        #         if not exist:
        #             layout[our_colour].append([token[0], destination[1], destination[2]])
        #         exploded_token_dict = get_exploded_dict(coord, layout)
        #         our_exploded, opponent_exploded = exploded_token_dict[our_colour], exploded_token_dict[opponent_colour]
        #         if sum(t[0] for t in our_exploded) - sum(t[0] for t in opponent_exploded) < min_exploded_num:
        #             min_exploded_num = sum(t[0] for t in our_exploded) - sum(t[0] for t in opponent_exploded)
        #             min_destination = destination
        #     return min_destination

        def find_best_action(layout):
            action_layout_list = generate_all_layouts(layout, our_colour)

            max_action = None
            max_cc = 0
            max_sparse = -1
            min_dist = 17
            for t, a, l, exp in action_layout_list:

                adjacency_list = generate_adjacency_list(l, find_3x3_adjacent_squares, our_colour)

                ccs = list(connected_components(adjacency_list))

                if len(ccs) > max_cc:
                    max_cc = len(ccs)
                    max_action = a
                elif len(ccs) == max_cc and len(l[our_colour]) > max_sparse:
                    max_sparse = len(l[our_colour])
                    max_action = a
                elif len(ccs) == max_cc and len(l[our_colour]) == max_sparse:
                    closestOpponent = None
                    closestOpponentDist = 17
                    for w in layout[opponent_colour]:
                        dist = abs(t[1] - w[1]) + abs(t[2] - w[2])
                        if dist < closestOpponentDist:
                            closestOpponentDist = dist
                            closestOpponent = w

                    if a[0] == "MOVE":
                        new_dist = abs(a[3][0] - closestOpponent[1]) + abs(a[3][1] - closestOpponent[2])
                        old_dist = abs(a[2][0] - closestOpponent[1]) + abs(a[2][1] - closestOpponent[2])

                        if new_dist < old_dist and new_dist < min_dist:
                            min_dist = new_dist
                            max_action = a

            return max_action

        our_colour = self.colour + "s"
        opponent_colour = "blacks" if self.colour == "white" else "whites"

        nearby = find_nearby_opponents()
        action = None
        if not nearby[opponent_colour]:
            # Make sparse
            # token = random.choice(self.layout[our_colour])
            # n, xa, ya = token[0], token[1], token[2]

            # destination = find_sparse_destination()

            action = find_best_action(self.layout)

        else:
            # Minimax
            exp = {"whites": [], "blacks": []}

            eval, action, escape = minimax(self.layout, exp, 3, -13, 13, True, opponent_colour, our_colour, False)

            if eval <= 0 and escape == False:
                new_l = copy.deepcopy(self.layout)
                new_l["whites"] = [white for white in new_l["whites"] if
                                    white not in nearby["whites"]]
                new_l["blacks"] = [black for black in new_l["blacks"] if
                                    black not in nearby["blacks"]]
                action = find_best_action(new_l)

        return action

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

        self.layout, _ = update_layout(action, self.layout, colour + 's')
