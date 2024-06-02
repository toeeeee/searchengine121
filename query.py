from timeit import default_timer as timer
from tfidf import calculate_tf_tq
from math import sqrt

search_data = None #global State object for accessing index data


def search(query: set, state, t) -> tuple:
    """
    Main search function: search and also compute ranking
    
    Parameter(s)
    query: set of words the user inputted to the search engine
    state: 
    t: time object, used to measure how long it took to return results for user query

    Return
    tuple (results, posting_id_ref)
    * results: 
    * posting_id_ref: 
    """

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
            byte = search_data.partial_index[term]  # get the byte where the term appears in the index
            search_data.main_index.seek(byte)  # navigate to the byte
            data = search_data.main_index.readline()
            data = eval(data)
            # convert the line into a dictionary with eval() function

            idf_tD = data[term][0]['idf']
            # print(f"data: {idf_tD}")

            w_tq = tf_tq * idf_tD  # WEIGHT FOR SPEC. TERM IN QUERY
            wtq_vector[term] = w_tq
            sum_w_tq_2 += (w_tq ** 2)

            for posting in data[term]:
                curr_results.update({posting['ID']: 0})  # add the IDs of results to current results w 0 rank
                posting_id_ref[posting['ID']] = (posting['url'], posting['title'])  # update the id reference dictionary

                w_td = posting['tf']  # WEIGHT FOR SPEC TERM IN A DOC THAT GETS CYCLED THRU
                if term in wtd_vectors:
                    wtd_vectors[posting['ID']][term] = w_td
                else:
                    wtd_vectors[posting['ID']] = {term: w_td}

            results.update(curr_results)  # add the results to the main results
        except KeyError:  # if the key does not exist in the partial index, nothing was found
            # print(f"KeyError: can't find term '{term}' in partial_index.\n")
            continue

    # CALCULATE NORMALIZED WEIGHTS FOR wtq
    len_wtq = sqrt(sum_w_tq_2)
    for _, wtq in wtq_vector.items():
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
            if term in posting_id_ref[docid][1]:
                rank += 2
        # done
        results[docid] = rank
        rank = 0

    end_time = timer() # for time testing
    print(f"\nquery time: {round(((end_time - t) * 1000), 3)} milliseconds.\n")
    # print(f"\nquery time: {round((end_time - t), 3)} seconds.\n")
    
    return results, posting_id_ref #return the intersection and the doc ID to url reference
