"""Network module for the recommender system."""

import numpy as np


class Network:
    """Network class for the recommender system."""

    def __init__(self, adjacency_matrix):
        """Initialize the network."""
        self.adjacency_matrix = adjacency_matrix
        self.degrees = np.sum(adjacency_matrix, axis=1)

    def directed_similarity(self, depth=2):
        """Return the similarity matrix."""
        degrees_in = np.sum(self.adjacency_matrix, axis=0)
        return (
            np.sum(
                [
                    np.linalg.matrix_power(self.adjacency_matrix, k) / k
                    for k in range(depth)
                ]
            )
            / degrees_in
        )

    def cosine_similarity(self):
        """Return the cosine similarity matrix."""
        shared_neighbours = np.einsum(
            "il,lj->ij", self.adjacency_matrix, self.adjacency_matrix
        )
        degree_matrix = np.einsum("i,j->ij", self.degrees, self.degrees)
        return shared_neighbours / np.sqrt(degree_matrix)

    @classmethod
    def from_data(cls, data, symmetric=True):
        """Build the network from the data."""
        adjacency_matrix = build_adjacency_matrix(data)
        if symmetric:
            adjacency_matrix = make_symmetric(adjacency_matrix)

        return cls(adjacency_matrix)


def build_adjacency_matrix(data):
    """Build adjacency matrix."""
    adjacent_nodes = data["recommends"]
    n = len(adjacent_nodes)
    adjacency_matrix = np.zeros((n, n))

    for node, neightbours in enumerate(adjacent_nodes):
        adjacency_matrix[node, neightbours] = 1

    return adjacency_matrix


def build_mapping(data):
    """Build mapping from MAL ids to network indices."""
    return {id_: index for index, id_ in enumerate(data["id"])}


def make_symmetric(adjacency_matrix):
    """Make the adjacency matrix symmetric."""
    return adjacency_matrix + adjacency_matrix.T