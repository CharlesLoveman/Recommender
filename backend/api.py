from abc import ABC, abstractmethod

class API:

    @abstractmethod
    @classmethod
    def extract_user_entries(user):
        """Get an np array of tuples containing the id, and user score of each watched show."""
        pass