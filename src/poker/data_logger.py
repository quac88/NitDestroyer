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


class Data_Logger:

    def __init__(self):
        self.current_node = None
        self.root = None
        self.filename = "trees.dat"

    def add_game_state(self, game_data):
        """Add a game state (node) to the tree."""
        new_node = Node(game_data)
        if self.current_node is None:
            self.root = new_node
        else:
            self.current_node.add_child(new_node)
        self.current_node = new_node

    def reset(self):
        """Reset logger for a new game."""
        self.current_node = None

    def store_tree(self):
        """Store the current game tree."""
        with open(self.filename, 'ab') as file:
            pickle.dump(self.root, file)
        self.root = None

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
