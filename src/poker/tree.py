from anytree import Node, RenderTree

class GameNode(Node):
    def __init__(self, game_data, parent=None, children=None) -> None:
        super().__init__(name=game_data, parent=parent, children=children)

