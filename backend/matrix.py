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
