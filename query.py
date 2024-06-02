from timeit import default_timer as timer
from tfidf import calculate_tf_tq
from math import sqrt

search_data = None #global State object for accessing index data


def search(query: set, state, t): #main search function
    """Search and also compute ranking :sob:"""
    global search_data
    search_data = state

    posting_id_ref = {} #keeping track of the ID's associated with each url
    results = {} #create an empty dict to store results (list of doc IDs)
    # list of lists where inner list is [id, rank]

    wtd_vectors = {}
    sum_w_td_2 = 0

    wtq_vector = {}
    sum_w_tq_2 = 0

    for term in query:
        curr_results = {}
        tf_tq = calculate_tf_tq(term, query) # weighted tf for term in query
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

            w_tq = tf_tq * idf_tD # WEIGHT FOR SPEC. TERM IN QUERY
            wtq_vector[term] = w_tq
            sum_w_tq_2 += (w_tq ** 2)

            for posting in data[term]:
                curr_results.update({posting['ID']: 0}) #add the IDs of results to current results w 0 rank
                posting_id_ref[posting['ID']] = (posting['url'], posting['title'], posting['bolds']) #update the id reference dictionary

                w_td = posting['tf'] # WEIGHT FOR SPEC TERM IN A DOC THAT GETS CYCLED THRU
                if term in wtd_vectors:
                    wtd_vectors[posting['ID']][term] = w_td
                else:
                    wtd_vectors[posting['ID']] = {term: w_td}

            results.update(curr_results) #add the results to the main results
        except KeyError: #if the key does not exist in the partial index, nothing was found
            continue

    # CALCULATE NORMALIZED WEIGHTS FOR wtq
    len_wtq = sqrt(sum_w_tq_2)
    for wordd, wtq in wtq_vector.items():
        wtq /= len_wtq

    # FOR wtd
    for docid in wtd_vectors:
        for term in wtd_vectors[docid]:
            sum_w_td_2 += wtd_vectors[docid][term]
        len_wtd = sqrt(sum_w_td_2)

        for term in wtd_vectors[docid]:
            wtd_vectors[docid][term] /= len_wtd

        sum_w_td_2 = 0

    rank = 0
    for docid in wtd_vectors:
        for term in wtd_vectors[docid]:
            if term in wtq_vector:
                rank += (wtq_vector[term] * wtd_vectors[docid][term])
            if term in posting_id_ref[docid][1]: # extra relevance for title
                rank += 2
            for bold in posting_id_ref[docid][2]:
                if bold:
                    if term in bold:
                        rank += .3

        #done
        results[docid] = rank
        rank = 0

    end_time = timer() #for time testing
    print(end_time - t)
    print(' seconds.')
    return results, posting_id_ref #return the intersection and the doc ID to url reference