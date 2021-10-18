
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class Node:

    def __init__(self, char):
        """
        Initialize the node.
        """

        # Set the node character as the label.
        self.char = char

        # True when this node is the last character of the word.
        self.is_end = False

        # Number of similar words.
        self.counter = 0

        # Childrens of the node.
        self.children = {}

        # Store the location point tuples identified by this node.
        self.spatial_points = {}


class Trie:

    def __init__(self):
        """
        Initialize the Trie object.
        """

        # Initialize the root node.
        self.root = Node('#')

        # Set the Directed Graph.
        self.G = nx.DiGraph()

        # Add the node to NetworkX.
        self.G.add_node('#')

        # Initializes the edges.
        self.edges = []

        self.labels = {}
    def insert(self, word):
        """
        Insert the word into the Prefix-tree.
        """

        # Get the root node.
        node = self.root

        # Set the previous node.
        prev = str(1) + word[0]

        if ('#', prev) not in self.edges:
            self.edges.append(('#', prev))

        level = 1

        self.labels[prev] = '#'

        for ch in word:

            node_id = str(level) + ch

            # Create a node for each character in the word.
            self.labels[node_id] = ch
            # self.G.add_node(str(level) + ch, {'label': ch})

            # Add the edge from the previous character to the current character
            # node.
            if prev != node_id:
                # self.edges.append((prev, ch))
                self.edges.append((prev, node_id))

            if ch in node.children:
                node = node.children[ch]
            else:
                new_node = Node(ch)
                node.children[ch] = new_node
                node = new_node

            prev = node_id
            level += 1

        self.G.add_nodes_from(self.labels.keys())
        # Mark it as the final node.
        node.is_end = True

        # Increment the word counter.
        node.counter += 1

    def dfs(self, node, prefix):
        """
        Depth-First Search for the prefix tree.
        """

        if node.is_end:

            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        """
        Query the given work in the prefix-tree.
        """

        # Initialize the final output list.
        self.output = []

        # Get the root node.
        node = self.root

        for ch in x:

            if ch in node.children:

                # Get the child node reference.
                node = node.children[ch]

            else:
                return []

        # Perform DFS.
        self.dfs(node, x[:-1])

        # Returns the given words prefixed with the given x.
        return sorted(self.output, key = lambda x: x[1], reverse=True)

    def render(self, prog='twopi'):
        """
        Renders the Prefix-tree using NetworkX
        """

        # Add each edge.
        for edge in self.edges:
            self.G.add_edge(edge[0], edge[1])

        # Get the position for the tree layout.
        pos = graphviz_layout(self.G, prog=prog)

        # Draw the graph.
        nx.draw(self.G, pos, labels=self.labels, with_labels=True, node_color='#6ab4f0', edge_color='#595959', node_size=1500, edgecolors='#4075b1', font_color='white', font_size=14, font_weight='bold', linewidths=2, width=2)

        plt.show()

# t = Trie()
# t.insert("was")
# t.insert("word")
# t.insert("war")
# t.insert("what")
# t.insert("where")
# # print(t.query("wh"))

# t.render()

