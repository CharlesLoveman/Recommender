"""Module to store similarity matrix."""

import pickle
import numpy as np
from scipy.sparse import csr_matrix


class Similarity:
    """Class to store similarity matrix."""

    _instance = None

    def __new__(cls, matrix=None, tol=1e-4):
        if cls._instance is None:
            print("Loading similarity matrix...")
            cls._instance = super(Similarity, cls).__new__(cls)
            cls._instance._load_matrix(matrix, tol)

        return cls._instance

    def _load_matrix(self, matrix, tol):
        if matrix is None:
            with open("similarity_matrix.pkl", "rb") as f:
                self.matrix = pickle.load(f)
        else:
            matrix[matrix < tol] = 0
            self.matrix = csr_matrix(matrix)

    def _save_matrix(self):
        with open("similarity_matrix.pkl", "wb") as f:
            pickle.dump(self.matrix, f)

    def __getitem__(self, index):
        return self.matrix[index]


class Map:
    """Class to store map from network indices to media ids."""

    _instance = None

    def __new__(cls, mapping=None):
        if cls._instance is None:
            print("Loading id mapping...")
            cls._instance = super(Map, cls).__new__(cls)
            cls._instance._load_map(mapping)

        return cls._instance

    def _load_map(self, mapping):
        if mapping is None:
            with open("id_mapping.pkl", "rb") as f:
                self.dictionary = pickle.load(f)
        else:
            self.dictionary = mapping

        self.keys = np.fromiter(self.dictionary.keys(), np.int64)
        
        def f(index):
            return self.dictionary[int(index)]

        self.mapping = np.vectorize(f)

    def _save_map(self):
        with open("id_mapping.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)

    def __call__(self, index):
        if isinstance(index, np.ndarray):
            if len(index):
                return self.mapping(np.intersect1d(index.astype(int), self.keys))
            else:
                return np.array([], np.int64)

        return self.dictionary[index]


class InvMap:
    """Class to store map from media ids to network indices."""

    _instance = None

    def __new__(cls, mapping=None):
        if cls._instance is None:
            print("Loading inverse id mapping...")
            cls._instance = super(InvMap, cls).__new__(cls)
            cls._instance._load_map(mapping)

        return cls._instance

    def _load_map(self, mapping):
        if mapping is None:
            with open("inv_mapping.pkl", "rb") as f:
                self.dictionary = pickle.load(f)
        else:
            self.dictionary = mapping

        self.keys = np.fromiter(self.dictionary.keys(), np.int64)

        def f(id_):
            return self.dictionary[int(id_)]

        self.mapping = np.vectorize(f)

    def _save_map(self):
        with open("inv_mapping.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)

    def slicer(self, id_):
        """Return indices of id_ in self.keys."""
        return np.intersect1d(
            id_.astype(int), self.keys, assume_unique=True, return_indices=True
        )[1]

    def __call__(self, id_):
        if isinstance(id_, np.ndarray):
            if len(id_):
                return self.mapping(np.intersect1d(id_.astype(int), self.keys))
            else:
                return np.array([], np.int64)

        return self.dictionary[id_]
