"""Rebuild and save maps and similarity matrix."""

from .network import Network
from .matrix import Similarity, Map, InvMap
import pickle

print("Loading data...")
with open("data.pkl", "rb") as f:
    data = pickle.load(f)

print("Building network...")
Network.configure(data)

print("Storing similarity matrix...")
Similarity()._save_matrix()
print("Storing maps...")
Map()._save_map()
InvMap()._save_map()

print("Done!")
