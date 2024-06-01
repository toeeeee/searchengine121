from timeit import default_timer as timer
from tfidf import calculate_tf_tq
from math import log

search_data = None #global State object for accessing index data


def search(query, state, t): #main search function
    global search_data
    search_data = state

    posting_id_ref = {} #keeping track of the ID's associated with each url
    results = [] #create an empty list to store results (list of doc IDs)
    scores = {} # key is ID , value is query weight with respect to term
    length = {}

    for term in query:
        curr_results = []
        tf_tq = calculate_tf_tq(term, query)
        idf_tD = None

        # FETCH POSTING LIST FOR TERM
        try:
            byte = search_data.partial_index[term] #get the byte where the term appears in the index
            search_data.main_index.seek(byte) #navigate to the byte
            data = search_data.main_index.readline()
            data = eval(data)
            #convert the line into a dictionary with eval() function

            for posting in data[term]:
                idf_tD = posting['idf']
                break

            w_tq = tf_tq * idf_tD

            for posting in data[term]: #for each posting/document associated with the term
                curr_results.append(posting['ID']) #add the IDs of results to current results
                posting_id_ref[posting['ID']] = posting['url'] #update the id reference dictionary

                # compute vector
                w_td = posting['tfidf']
                if posting['ID'] in scores.keys():
                    scores[posting['ID']] += w_tq * w_td
                else:
                    scores[posting['ID']] = w_tq * w_td

                # compute vector magnitude/length


            results.append(curr_results) #add the results to the main results list

        except KeyError: #if the key does not exist in the partial index, nothing was found
            return None, None

    #at the end of searching, get the intersection of all the lists
    #('results' is a list of lists containing docs IDs at this point)
    results = sorted(results, key=len)
    results = set.intersection(*map(set, results))

    end_time = timer() #for time testing
    print(end_time - t)
    print(' seconds.')
    return results, posting_id_ref #return the intersection and the doc ID to url reference