"""Recommendation Engine."""

import numpy as np
from .matrix import Similarity, Map, InvMap

norm = 0.5


def recommend(users):
    """Recommend movies to users."""
    scores = build_score(compile_ratings(users))
    return Map()(np.argpartition(scores, -5)[-5:])


def compile_ratings(users):
    """Compile the ratings of all users."""
    return np.vstack([normalise_ratings(user.astype(float)) for user in users])


def build_score(ratings):
    """Build the score vector for a user."""
    (id_, ii) = InvMap().slicer(ratings[:, 0])
    return Similarity()[InvMap()(id_), :].T @ ratings[ii][:, 1]


def normalise_ratings(ratings):
    """Normalise the ratings."""
    ratings[:, 1] = (ratings[:, 1] / 5 - 1) / len(ratings)**norm
    return ratings
