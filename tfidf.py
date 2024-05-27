from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from math import log
import os
'''
corpus = ['This is the first document.',
          'This document is the second document.',
          'And this is the third one.',
          'Is this the first document?',
          ]

STOP_WORDS = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
              "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
              "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
              "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each",
              "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
              "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
              "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
              "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
              "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
              "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
              "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
              "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
              "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
              "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
              "what", "what's", "when", "when's", "where", "which", "while", "who", "whom", "why",
              "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
              "your", "yours", "yourself", "yourselves"]

# vectorizer = TfidfVectorizer() # Without Stop Words
vectorizer = TfidfVectorizer(stop_words=STOP_WORDS)  # With stop words

# gets the words and idf
vec = vectorizer.fit_transform(corpus)
dense_matrix = vec.todense()
word_names = vectorizer.get_feature_names_out()
df = pd.DataFrame(dense_matrix, columns=word_names)  # This contains the tf-idf for ALL documents
# print(df)
# the print will show you all of the words and their tf-idf values


# if you want it for a specific document
index = 1
tfidf_value = df.iloc[index]  # this would be
# print(tfidf_value)


# if you want to sort it, with highest values first for a single document
sorted_tfidf = tfidf_value.sort_values(ascending=False)
# print(sorted_tfidf)


# if you want to do it for all documents
word_tfidf_sum = df.sum(axis=0)  # This sums up the tf-idf for all documents
sorted_words = word_tfidf_sum.sort_values(ascending=False)  # sorts the words based on their tf-idf values
sorted_df = df[sorted_words.index]  # creates a new df that is sorted based on word importance throughout the corpus
# print(sorted_df)

# To access a specific word and find it's tf-idf
word_index = vectorizer.vocabulary_.get("document")
if word_index is not None:
    tfidf_for_single = vec[:,
                       word_index].toarray().flatten()  # gets values for the specific word where the index of the search word is
    df_for_single = pd.DataFrame({"document": tfidf_for_single})  # puts the values into a dataframe
    # print(df_for_single)
    # print(tfidf_for_single)

# number of times term t appears in document d
# total number of terms in document d

# total number of documents in CORPUS D
# number of documents containing term t

'''
'''
    tf = number of times term t appears in document  / total number of terms in document d
    idf = log(total_documents/Number of documents containing term t)
    
    find the tf and idf
    multiply them together to get the tfidf
    reassign it into the postings
    write the new key and postings into the file
    
for line in lines -> eval line to dictionary -> calculate tf using the frequency -> calculate idf -> calculate tfidf -> set 'tfidf' 
in the dictionary to the tdidf calculated -> write this back into another file -> continue

{term : posting}
{posting : id, frequency, url, tfidf}
posting = key[posting][0]
posting['frequency']

create a new directory with a few document
rather than use dev

run indexer with that
'''
def calculate_tfidf(total_documents):
    with open('tfidf_index.txt', 'w') as writefile:
        with open('main_index.txt', 'r') as file:
            line = file.readline()
            while line: #each line is an index
                index_content = eval(line)
                key  = list(index_content.keys())[0] # this gives us the key
                postings = index_content[key]

                df = len(postings)
                idf = log(total_documents/df + 1)

                for posting in postings:
                    times_term_appears = posting['frequency']
                    total_terms_in_document = posting['total_terms']
                    tf = times_term_appears / total_terms_in_document
                    tfidf = tf * idf
                    posting['tfidf'] = tfidf
                index_content = {key : postings}
                writefile.writelines(str(index_content) + "\n")  # write this data into the main index file
                line = file.readline()
    os.remove('main_index.txt')  # delete the index chunk from disk