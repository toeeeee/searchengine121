import globals


class Posting:
    def __init__(self, ID, frequency, url):
        self.ID = ID
        self.frequency = frequency
        self.url = url

    def to_dictionary(self):
        return {f'ID': self.ID, 'frequency': self.frequency, 'url': self.url}

      
def update_inverted_index_map(word: str, doc_id: str, tfidf_score: str) -> None:
    """
    Quote from assignment description:
    " The inverted index is simply a map with the token as a key and a list of its corresponding postings. A posting is the representation of the token's occurrence in a document "
    
    Given a word, find it in the inverted index map and update it with new posting info, generated from the parameters given.

    Parameters
    word: the key in the inverted index map that nees to be updated
    doc_id, tfidf_score: posting info to be appended to the value's postings list

    Return
    None
    """

    globals.INVERTED_INDEX_MAP
    posting = [doc_id, tfidf_score]  # create the posting

    try:  # update the word's list of postings
        # append this posting to the word's list of postings
        globals.INVERTED_INDEX_MAP[word].append(posting)
    except KeyError:  # word isn't in the map, so add it to the map with posting info
        # create a list of postings
        globals.INVERTED_INDEX_MAP[word] = [posting]
    
    return


if __name__ == '__main__':
    pass
