from timeit import default_timer as timer
from tfidf import calculate_tf_tq
from math import sqrt

search_data = None #global State object for accessing index data


def search(query: set, state, t): #main search function
    """Search and also compute ranking :sob:"""
    global search_data
    search_data = state

    posting_id_ref = {} #keeping track of the ID's associated with each url
    results = [] #create an empty list to store results (list of doc IDs)
    # list of lists where inner list is [id, rank]

    # calculate cosine similarity
    # (sum of w_td*w_tq) / (sqrt(sum of w_td^2) *  sqrt(sum of w_tq^2))
    # we have mult. documents to calc w for but only one query to calc w for
    sum_of_wtq_wtd = []
    w_td_w_tq = {} # key is ID , value is query weight with respect to term
    sum_of_wtd = {}
    sum_w_tq_2 = 0

    for term in query:
        #print(f'term: {term}')
        curr_results = []
        tf_tq = calculate_tf_tq(term, query) # tf for term in query
        #print(tf_tq)
        idf_tD = None

        # SHOULD SUM UP ALL WEIGHTS FOR A SPECIFIC TERM IN QUERY * WEIGHT OF SPEC. TERM IN DOC.

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
            w_tq = tf_tq * idf_tD # WEIGHT FOR SPEC. TERM IN QUERY
            sum_w_tq_2 += (w_tq ** 2)

            for posting in data[term]: #for each posting/document associated with the term
                curr_results.append([posting['ID'], 0]) #add the IDs of results to current results
                posting_id_ref[posting['ID']] = posting['url'] #update the id reference dictionary

                # go through each document for a term and
                # calculate weight_term_in_query * weight_term_in_document
                w_td = posting['tfidf'] # WEIGHT FOR SPEC TERM IN A DOC THAT GETS CYCLED THRU
                if posting['ID'] in w_td_w_tq.keys():
                    w_td_w_tq[posting['ID']] += w_tq * w_td # GO TO ID AND ADD UP ALL WEIGHTS FOR ALL TERMS
                else:
                    w_td_w_tq[posting['ID']] = w_tq * w_td

                if posting['ID'] in sum_of_wtd.keys():
                    sum_of_wtd[posting['ID']] += posting['tfidf2']
                else:
                    sum_of_wtd[posting['ID']] = posting['tfidf2']
            results += curr_results #add the results to the main results list

        except KeyError: #if the key does not exist in the partial index, nothing was found
            print('error')
            return None, None

    # CALCULATE AND APPEND SCORE TO RESULT
    for result in results:
        if (result[0] in w_td_w_tq.keys()) and (result[0] in sum_of_wtd.keys()):
            rank = (w_td_w_tq[result[0]]) / (sqrt(sum_of_wtd[result[0]]) * sqrt(sum_w_tq_2))
            result[1] = rank

    results = sorted(results, key= lambda r: r[1], reverse = True)
    #results = set.intersection(*map(set, results))

    end_time = timer() #for time testing
    print(end_time - t)
    print(' seconds.')
    return results, posting_id_ref #return the intersection and the doc ID to url reference