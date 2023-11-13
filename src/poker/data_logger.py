import pickle

class Node:
    def __init__(self, game_data=None):
        self.game_data = game_data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __iter__(self):
        yield self.game_data
        for child in self.children:
            yield from child

class DataLogger:
    def __init__(self):
        self.current_node = None
        self.root = None
        self.filename = "trees.dat"
        self.hand_number = 0  # Attribute to track the hand number

    def add_game_state(self, game_data):
        """Add a game state (node) to the tree."""
        # Include the hand number in the game data
        game_data_with_hand = game_data.copy()
        game_data_with_hand['hand_number'] = self.hand_number

        new_node = Node(game_data_with_hand)
        if self.current_node is None:
            self.root = new_node
        else:
            self.current_node.add_child(new_node)
        self.current_node = new_node

    def next_hand(self):
        """Increment the hand number for the next hand."""
        self.hand_number += 1

    def reset(self):
        """Reset logger for a new game."""
        self.current_node = None
        self.hand_number = 0  # Reset hand number

    def store_tree(self):
        """Store the current game tree."""
        with open(self.filename, 'ab') as file:
            pickle.dump(self.root, file)
        self.root = None
        self.current_node = None  # Reset after storing

    def load_trees(self):
        """Load all game trees."""
        trees = []
        with open(self.filename, 'rb') as file:
            while True:
                try:
                    tree = pickle.load(file)
                    trees.append(tree)
                except EOFError:
                    break
        return trees
