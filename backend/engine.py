"""Recommendation Engine."""

import numpy as np
from .matrix import Similarity, Map


def recommend(users):
    """Recommend movies to users."""
    scores = build_score(compile_ratings(users))
    mapping = Map()
    return mapping[np.argmax(scores)]


def compile_ratings(users):
    """Compile the ratings of all users."""
    return np.vstack([normalise_ratings(user) for user in users])


def build_score(ratings):
    """Build the score vector for a user."""
    similarity = Similarity()
    return np.sum(similarity[ratings[:, 0], :] * ratings[:, 1], axis=0)


def normalise_ratings(ratings):
    """Normalise the ratings."""
    ratings[:, 1] = (ratings[:, 1] / 5 - 1) / len(ratings)
    return ratings
