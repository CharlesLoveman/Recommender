"""Module to store similarity matrix."""

import pickle


class Similarity:
    """Class to store similarity matrix."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Loading similarity matrix...")
            cls._instance = super(Similarity, cls).__new__(cls)
            cls._instance._load_matrix()

        return cls._instance

    def _load_matrix(self):
        with open("../similarity_matrix.pkl", "rb") as f:
            self.matrix = pickle.load(f)

    def _save_matrix(self):
        with open("../similarity_matrix.pkl", "wb") as f:
            pickle.dump(self.matrix, f)
