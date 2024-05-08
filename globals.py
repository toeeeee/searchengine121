"""
This document holds all the global variables needed for our search engine
"""

FREQ_DICT = {}  # dict that holds all words encountered and the frequency of encounters

"""
INVERTED_INDEX_MAP: a map with the token as a key and a list of its corresponding postings
Posting: the representation of the token's occurrence in a document. The posting typically contains the following info (and could/should contain more):
 • The document name/id the token was found in
 • Its tf-idf score for that document
 • [add more]

INVERTED_INDEX_MAP key-value pair format: { word : [ posting1, posting2, ... ]
posting format: [doc name/id, tf-idf, ... ]
"""
INVERTED_INDEX_MAP = {}  # map of inverted indices
