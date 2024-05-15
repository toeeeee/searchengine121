

class State:
    """Class to hold partial index data and queries"""
    def __init__(self):
        self.partial_index = None
        self.query = None

    def set_index(self, data): #set the partial index
        self.partial_index = data

    def set_query(self, query): #set the query
        self.query = query
