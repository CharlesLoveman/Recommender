"""Recommendation Engine."""

import numpy as np
from .matrix import Similarity, Map, InvMap


def recommend(users):
    """Recommend movies to users."""
    scores = build_score(compile_ratings(users))
    return Map()(np.argpartition(scores, -4)[-4:])


def compile_ratings(users):
    """Compile the ratings of all users."""
    return np.vstack([normalise_ratings(user) for user in users])


def build_score(ratings):
    """Build the score vector for a user."""
    return Similarity()[InvMap()(ratings[:, 0]), :] @ ratings[:, 1]


def normalise_ratings(ratings):
    """Normalise the ratings."""
    ratings[:, 1] = (ratings[:, 1] / 5 - 1) / len(ratings)
    return ratings
