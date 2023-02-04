"""Module to store similarity matrix."""

import pickle


class Similarity:
    """Class to store similarity matrix."""

    _instance = None

    def __new__(cls, matrix=None):
        if cls._instance is None:
            print("Loading similarity matrix...")
            cls._instance = super(Similarity, cls).__new__(cls)
            cls._instance._load_matrix(matrix)

        return cls._instance

    def _load_matrix(self, matrix):
        if matrix is None:
            with open("../similarity_matrix.pkl", "rb") as f:
                self.matrix = pickle.load(f)
        else:
            self.matrix = matrix

    def _save_matrix(self):
        with open("../similarity_matrix.pkl", "wb") as f:
            pickle.dump(self.matrix, f)


class Map:
    """Class to store map from MAL ids to network indices."""

    def __new__(cls, mapping=None):
        if cls._instance is None:
            print("Loading id mapping...")
            cls._instance = super(Map, cls).__new__(cls)
            cls._instance._load_map(mapping)

        return cls._instance

    def _load_map(self, mapping):
        if mapping is None:
            with open("../id_mapping.pkl", "rb") as f:
                self.mapping = pickle.load(f)
        else:
            self.mapping = mapping

    def _save_map(self):
        with open("../similarity_matrix.pkl", "wb") as f:
            pickle.dump(self.mapping, f)
