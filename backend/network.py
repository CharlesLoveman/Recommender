"""Network module for the recommender system."""

import numpy as np
from scipy.sparse import csr_matrix
from .matrix import Similarity, Map, InvMap


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
        shared_neighbours = self.adjacency_matrix @ self.adjacency_matrix
        degree_matrix = self.degrees @ self.degrees.T
        similarity_matrix = shared_neighbours / np.sqrt(degree_matrix)
        return np.nan_to_num(similarity_matrix, nan=0)

    @classmethod
    def configure(cls, data, symmetric=True):
        """Configure the network."""
        # Build maps
        Map({i: media for i, media in enumerate(data["id"])})
        InvMap({media: i for i, media in enumerate(data["id"])})

        # Build adjacency matrix
        adjacency_matrix = csr_matrix(build_adjacency_matrix(data))
        if symmetric:
            adjacency_matrix = make_symmetric(adjacency_matrix)

        # Build network
        network = cls(adjacency_matrix)
        Similarity(network.cosine_similarity())

        return network


def build_adjacency_matrix(data):
    """Build adjacency matrix."""
    adjacent_nodes = data["recommends"]
    n = len(adjacent_nodes)
    adjacency_matrix = np.zeros((n, n))

    for node, neighbours in enumerate(adjacent_nodes):
        ii = InvMap().slicer(neighbours)
        adjacency_matrix[node, InvMap()(neighbours[ii])] = 1

    return adjacency_matrix


def build_mapping(data):
    """Build mapping from MAL ids to network indices."""
    return {id_: index for index, id_ in enumerate(data["id"])}


def make_symmetric(adjacency_matrix):
    """Make the adjacency matrix symmetric."""
    return adjacency_matrix + adjacency_matrix.T
