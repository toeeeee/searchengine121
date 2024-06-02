
class Posting:
    """Class to represent a posting of a document.
        Attributes:
        ID: unique ID of the document
        frequency: frequency that a token appears in the document
        url: URL of the document"""
    def __init__(self, ID, frequency, url, total_terms):
        self.ID = ID
        self.frequency = frequency
        self.url = url
        self.total_terms = total_terms

    def to_dictionary(self): #convert a Posting into a dictionary of its attributes
        return {'ID': self.ID, 'frequency': self.frequency, 'url': self.url, 'total_terms': self.total_terms}
