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
