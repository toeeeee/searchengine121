from math import log
from tokenizer import tokenize
import os


def calculate_tf_tq(given_term: str, query: set):
    """Calculate tf for term in a query"""
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

def calculate_weight_tq(tf, idf):
    """
    Calculate tfidf for a term in a query
    """



def calculate_tfidf(total_documents):
    with open('tfidf_index.txt', 'w') as writefile:
        with open('main_index.txt', 'r') as file:
            line = file.readline()
            while line: #each line is an index
                index_content = eval(line)
                key  = list(index_content.keys())[0] # this gives us the key
                postings = index_content[key]

                df = len(postings)
                idf = log(total_documents/(df + 1))

                for posting in postings:
                    times_term_appears = posting['frequency']
                    total_terms_in_document = posting['total_terms']
                    #tf = times_term_appears / total_terms_in_document
                    if times_term_appears <= 0:
                        tf = 0
                    else:
                        tf = 1 + log(times_term_appears)
                    posting['tf'] = tf
                    posting['idf'] = idf
                #index_content = {key: postings}
                writefile.write(f'{{"{key}": {postings}}}\n')  # write this data into the main index file
                line = file.readline()
    os.remove('main_index.txt')  # delete the index chunk from disk

#out.write(f'{{"{key}": {value}}}\n')