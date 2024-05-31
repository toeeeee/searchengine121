class State:
    """Class to hold partial index data and queries"""
    def __init__(self):
        self.partial_index = None
        self.query = None
        self.main_index = None

    def set_index(self, data): #set the partial index
        self.partial_index = data

    def set_query(self, query): #set the query
        self.query = query

    def set_main_index(self, main_index): #set the main index
        self.main_index = main_index