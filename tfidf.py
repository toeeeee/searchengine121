from math import log
from tokenizer import tokenize
import os


def calculate_tf_tq(given_term: str, query: set) -> float:
    """
    Calculate tf for term in a query
    
    Parameter(s)
    given_term: the tf_tq score calculated for this term
    query: set object of individual words searched for by user

    Return
    tf: term frequency score
    """
    
    freq = 0
    total_terms = 0
    for term in query:
        total_terms += 1
        if given_term == term:
            freq += 1
    if freq <= 0:
        tf = 0
    else:
        tf = 1 + log(freq)
    return tf


def calculate_tfidf(total_documents: int) -> None:
    """
    Calculate tf for term in a query
    
    Parameter(s)
    total_documents: total number of documents, used to calculate tfidf score

    Return
    None
    """
    
    with open('tfidf_index.txt', 'w') as writefile:
        with open('main_index.txt', 'r') as file:
            line = file.readline()
            while line:  # each line is an index
                index_content = eval(line)
                key  = list(index_content.keys())[0]  # this gives us the key
                postings = index_content[key]

                df = len(postings)
                idf = log(total_documents/(df + 1))

                for posting in postings:
                    times_term_appears = posting['frequency']
                    total_terms_in_document = posting['total_terms']
                    # tf = times_term_appears / total_terms_in_document
                    if times_term_appears <= 0:
                        tf = 0
                    else:
                        tf = 1 + log(times_term_appears)
                    tfidf = tf * idf
                    if tfidf > 2:
                        posting['tfidf'] = 2
                    else:
                        posting['tfidf'] = tfidf
                        posting['tfidf2'] = tfidf ** 2
                        posting['tf'] = tf
                        posting['idf'] = idf
                # index_content = {key: postings}
                writefile.write(f'{{"{key}": {postings}}}\n')  # write this data into the main index file
                line = file.readline()
    os.remove('main_index.txt')  # delete the index chunk from disk

# out.write(f'{{"{key}": {value}}}\n')