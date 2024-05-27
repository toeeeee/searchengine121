from timeit import default_timer as timer

search_data = None #global State object for accessing index data

def search(query, state, t): #main search function
    global search_data
    search_data = state

    posting_id_ref = {} #keeping track of the ID's associated with each url
    results = [] #create an empty list to store results (list of doc IDs)

    for term in query:
        curr_results = []

        try:
            byte = search_data.partial_index[term] #get the byte where the term appears in the index
            search_data.main_index.seek(byte) #navigate to the byte
            data = eval(search_data.main_index.readline())
            #convert the line into a dictionary with eval() function

            for posting in data[term]: #for each posting associated with the term
                curr_results.append(posting['ID']) #add the IDs of results to current results
                posting_id_ref[posting['ID']] = posting['url'] #update the id reference dictionary

            results.append(curr_results) #add the results to the main results list

        except KeyError: #if the key does not exist in the partial index, nothing was found
            return None, None

    #at the end of searching, get the intersection of all the lists
    #('results' is a list of lists containing docs IDs at this point)
    results = set.intersection(*map(set, results))

    end_time = timer() #for time testing
    print(end_time - t)
    return results, posting_id_ref #return the intersection and the doc ID to url reference