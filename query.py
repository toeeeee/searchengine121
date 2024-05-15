import ast
from timeit import default_timer as timer

search_data = None #global class for accessing index data

def search(query, state, t): #main search function
    global search_data
    search_data = state

    posting_id_ref = {} #keeping track of the ID's associated with each url
    results = []

    for term in query:
        curr_results = []
        #this is used to determine which partial and full index to query from
        #partial_index, index_name = get_index(term[0])

        try:
            byte = search_data.partial_index[term] #get the byte where the term appears in the index
            with open('main_index.txt', 'r') as f:
                f.seek(byte) #navigate to the byte
                data = ast.literal_eval(f.readline()) #convert the line into a dictionary

                for posting in data[term]:
                    curr_results.append(posting['ID']) #add the IDs of results to current results
                    posting_id_ref[posting['ID']] = posting['url'] #update the id reference

                if len(results) == 0: #if results is empty, just extend it
                    results.extend(curr_results)
                else: #otherwise, get the intersection of the current results and the overall results
                    results = list(set(results).intersection(curr_results))

        except KeyError: #if the key does not exist in the partial index, nothing was found
            return None, None
    end_time = timer() #for time testing
    print(end_time - t)
    return results, posting_id_ref
