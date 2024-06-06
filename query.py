from timeit import default_timer as timer
from tfidf import calculate_tf_tq
from math import sqrt

search_data = None #global State object for accessing index data

vague_words = ['software', 'computer', 'master', 'slave']
# less ranking points for words that appear WAY too commonly for this corpus /
# ones i just notice give bad results :)

def search(query: set, raw_q, state, stop_words_enabled,  t) -> tuple:
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

            # trim down data for stop_words
            if stop_words_enabled:
                data[term] = data[term][0:5]

            idf_tD = data[term][0]['idf']
            # print(f"data: {idf_tD}")

            w_tq = tf_tq * idf_tD  # WEIGHT FOR SPEC. TERM IN QUERY
            wtq_vector[term] = w_tq
            sum_w_tq_2 += (w_tq ** 2)

            for posting in data[term]:
                curr_results.update({posting['ID']: 0})  # add the IDs of results to current results w 0 rank
                posting_id_ref[posting['ID']] = (posting['url'], posting['title'], posting['b'])  # update the id reference dictionary

                w_td = posting['tf']  # WEIGHT FOR SPEC TERM IN A DOC THAT GETS CYCLED THRU
                if term in wtd_vectors:
                    wtd_vectors[posting['ID']][term] = w_td
                else:
                    wtd_vectors[posting['ID']] = {term: w_td}

            results.update(curr_results)  # add the results to the main results
        except KeyError:  # if the key does not exist in the partial index, nothing was found
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
            # title for term then url and then same for whole queue msg
            if posting_id_ref[docid][2]:
                rank += 3
            if posting_id_ref[docid][1]:
                rank += 3
            if term.lower() in posting_id_ref[docid][0]:
                rank += 3
            for untokenized in raw_q.split():
                # if untokenized.title() in posting_id_ref[docid][1] or untokenized in posting_id_ref[docid][1]:
                #     rank += 3
                if untokenized.lower() in posting_id_ref[docid][0]:
                    rank += 3

            # if raw_q.title() in posting_id_ref[docid][1] or raw_q in posting_id_ref[docid][1]:
            #     rank += 10
            if raw_q in posting_id_ref[docid][0] or raw_q.lower() in posting_id_ref[docid][0]:
                rank += 10
            if ' '.join(raw_q.lower()) in posting_id_ref[docid][0]:
                rank += 5
            if raw_q.title() in 'Master Of Software Engineering' and 'mswe' in posting_id_ref[docid][0]:
                rank += 2

            if term in vague_words:
                rank -= 1
            if 'ngs' in posting_id_ref[docid][0]: # a lot of junk blog posts
                rank -= 8
            if term in posting_id_ref[docid][0] and 'slave' in posting_id_ref[docid][0]:
                rank -= 2

        # done
        results[docid] = rank
        rank = 0

    end_time = timer() # for time testing
    print(f"\nquery time: {round(((end_time - t) * 1000), 3)} milliseconds.\n")
    
    return results, posting_id_ref #return the intersection and the doc ID to url reference
