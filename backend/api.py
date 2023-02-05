from abc import ABC, abstractmethod


class API(ABC):
    
    @classmethod
    @abstractmethod
    def extract_user_entries(user):
        """Get an np array of tuples containing the id, and user score of each watched show."""
        return NotImplemented
   
    @abstractmethod
    def pickle_global_entries():
        """Get a data frame of all the media entries, with headers 'id', 'title', 'rating' and 'recommends'. Also pickles the database."""
        return NotImplemented