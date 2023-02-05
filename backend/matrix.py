"""Module to store similarity matrix."""

import pickle
import numpy as np
from functools import singledispatch


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

    def __getitem__(self, index):
        return self.matrix[index]


class Map:
    """Class to store map from network indices to MAL ids."""

    _instance = None

    def __new__(cls, mapping=None):
        if cls._instance is None:
            print("Loading id mapping...")
            cls._instance = super(Map, cls).__new__(cls)
            cls._instance._load_map(mapping)

        return cls._instance

    def _load_map(self, mapping):
        if mapping is None:
            with open("../id_mapping.pkl", "rb") as f:
                self.dictionary = pickle.load(f)
        else:
            self.dictionary = mapping

        def f(index):
            return self.dictionary[index]

        self.mapping = np.vectorize(f)

    def _save_map(self):
        with open("../id_mapping.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)

    def __call__(self, index):
        if len(index):
            return self.mapping(index)


class InvMap:
    """Class to store map from MAL ids to network indices."""

    _instance = None

    def __new__(cls, mapping=None):
        if cls._instance is None:
            print("Loading inverse id mapping...")
            cls._instance = super(InvMap, cls).__new__(cls)
            cls._instance._load_map(mapping)

        return cls._instance

    def _load_map(self, mapping):
        if mapping is None:
            with open("../inv_mapping.pkl", "rb") as f:
                self.dictionary = pickle.load(f)
        else:
            self.dictionary = mapping

        def f(id_):
            return self.dictionary[id_]

        self.mapping = np.vectorize(f)

    def _save_map(self):
        with open("../inv_mapping.pkl", "wb") as f:
            pickle.dump(self.dictionary, f)

    def __call__(self, id_):
        if len(id_):
            return self.mapping(id_)
