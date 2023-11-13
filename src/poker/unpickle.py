from data_logger import Data_Logger, Node


def print_tree(tree, depth=0):
    """Recursively print the tree."""
    if tree:
        print("  " * depth + str(tree.game_data))
        for child in tree.children:
            print_tree(child, depth + 1)


def main():
    logger = Data_Logger()
    trees = logger.load_trees()
    for i, tree in enumerate(trees):
        print(f"Tree {i + 1}:")
        print_tree(tree)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()

# from anytree import Node, RenderTree

# def build_game_state_tree(game_state) -> None:
#     """Builds and returns a tree representation of the game state."""
#     # Root node
#     root = Node("Game State")

#     # Add board and current bet as child nodes
#     Node(f"Board: {game_state['board']}", parent=root)
#     Node(f"Current Bet: {game_state['current_bet']}", parent=root)

#     # Add each player's state as a child node
#     for player_id, player_data in game_state.items():
#         if player_id not in ['current_bet', 'board']:  # Avoiding non-player keys
#             player_node = Node(f"Player {player_id}", parent=root)
#             for key, value in player_data.items():
#                 Node(f"{key}: {value}", parent=player_node)

#     return root

# def print_game_state_tree(game_state_tree):
#     """Prints the game state tree."""
#     for pre, _, node in RenderTree(game_state_tree):
#         print(f"{pre}{node.name}")