def add_connection(graph, node1, node2, label):
    """
       Add nodes and an edge to a NetworkX graph.

       Args:
           graph (networkx.Graph): NetworkX graph object
           node1 (str): First node identifier
           node2 (str): Second node identifier
           label: Edge label (typically similarity percentage)

       Returns:
           None (modifies graph in place)

       Example:
           >>> import networkx as nx
           >>> G = nx.Graph()
           >>> add_connection(G, "en", "es", "85.5%")
       """
    # Node adding
    graph.add_node(node1)
    graph.add_node(node2)
    # Edge adding
    graph.add_edge(node1, node2, label=label)


"""
   Calculate the average of diagonal elements in a matrix.
   Used to compute overall similarity between language word lists.

   Args:
       matrix (list of lists): 2D matrix (can be non-square)

   Returns:
       float: Average of diagonal elements, or 0 if matrix is empty

   Example:
       >>> matrix = [[1.0, 0.5], [0.3, 0.9]]
       >>> diagonal_average(matrix)
       0.95  # average of 1.0 and 0.9
   """
def diagonal_average(matrix):
    # Handle empty matrix or matrix with empty rows
    if not matrix or not matrix[0]:
        return 0

    n = min(len(matrix), len(matrix[0]))  # works for non-square matrices
    diagonal = [matrix[i][i] for i in range(n)]

    return sum(diagonal) / len(diagonal) if diagonal else 0
