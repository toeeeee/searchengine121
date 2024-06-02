from state import State
from query import search
from tokenizer import tokenize
from timeit import default_timer as timer

STOP_WORDS = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
              "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
              "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
              "did", "didn't", "do", "does", "doesn't", "doing","don't", "down", "during", "each",
              "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
              "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
              "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
              "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
              "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
              "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
              "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
              "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
              "they're", "they've","this", "those", "through", "to", "too", "under", "until", "up",
              "very", "was", "wasn't", "we", "we'd","we'll", "we're", "we've", "were", "weren't",
              "what", "what's", "when", "when's", "where", "which", "while","who", "whom", "why",
              "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
              "your", "yours", "yourself", "yourselves"]
#list of stop words to remove them from user queries


def load_partial_indices() -> State:
    """
    load the partial index on disk into a State object, which holds
    partial index data

    Parameter(s)
    None

    Return
    State object with 
    """
    
    search_state = State()

    with open('partial_index.txt', 'r') as f:
        data = eval(f.readline())  # the partial index is just one line, so read one line
        search_state.set_index(data)

    return search_state

if __name__ == '__main__':
    print('Loading...\n')
    index_file = open('tfidf_index.txt', 'r')
    search_data = load_partial_indices() #load the partial index on disk
    print('---------------------------')
    query: str = input('Enter query: ("~" to quit)\n') #prompt for query

    while query != '~':
        start_time = timer() #for time testing
        search_data.set_query(query) #set the query attribute in the State object
        search_data.set_main_index(index_file)
        terms = tokenize(query) #tokenize the query
        stop_word_amt = len([t for t in terms if t in STOP_WORDS])
        if stop_word_amt / len(terms) > 0.8:
            terms = set(terms)
        else:
            terms = set([term for term in terms if term not in STOP_WORDS]) #remove stop words from the query
        #search for documents with the given query, get a list of doc IDs and an ID and url reference
        results, id_ref = search(terms, search_data, start_time)
        if not results: #if no results, ask for another query
            print(f"No results for: {query}\n")
            print('---------------------------\n')
            query = input("Enter query: ('~' to quit)\n")
            continue
        results = {key: val for key,val in sorted(results.items(), key=lambda item: item[1], reverse = True)}
        i = 1
        print("RANKINGS:")
        for docid in results: #print the first 5 results to the console ( for now )
            if i >= 6:
                break
            print(f"{i}. Ranking: {round(results[docid], 3)}.")
            print(f"   Link: {id_ref[docid][0]}\n")
            #results is a list of doc IDs, so we use id_ref to get the url
            # associated with the ID
            i += 1
        print('---------------------------')
        query = input("Enter query: ('~' to quit)\n")

    print('Goodbye!')
    index_file.close() #keeping the index file open until the end, as per slides