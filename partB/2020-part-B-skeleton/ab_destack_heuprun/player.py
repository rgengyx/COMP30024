import random
from ab_destack_heuprun.square import *
from ab_destack_heuprun.graph import *


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

        # Minimax: For each white tokens on the board, there are 4 different directions to move to.
        colour = "blacks" if self.colour == "white" else "whites"
        eval, action = minimax(self.layout, 6, -13, 13, True, colour, self.colour + "s")
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

        self.layout = update_layout(action, self.layout, colour + 's')
