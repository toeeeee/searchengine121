import ast
import os
import ujson as json
#import requests
from bs4 import BeautifulSoup as BS
from collections import Counter, OrderedDict
from tokenizer import tokenize, check_for_duplicates
from postings import Posting
from partial_indexer import partial_index
from tfidf import calculate_tfidf

A_C = ['a','b','c']
D_F = ['d','e','f']
G_I = ['g','h','i']
J_L = ['j','k','l']
M_O = ['m','n','o']
P_R = ['p','q','r']
S_U = ['s','t','u']
V_X = ['v','w','x']
Y_Z = ['y','z']

# Key: token, Value: list of Postings
index_A_C = {}
index_D_F = {}
index_G_I = {}
index_J_L = {}
index_M_O = {}
index_P_R = {}
index_S_U = {}
index_V_X = {}
index_Y_Z = {}
index_misc = {}

index_list = ['index_A_C.txt', 'index_D_F.txt', 'index_G_I.txt', 'index_J_L.txt',
              'index_M_O.txt', 'index_P_R.txt', 'index_S_U.txt',
              'index_V_X.txt', 'index_Y_Z.txt', 'index_misc.txt']

def build_index(directories: str) -> None:
    """
    Given a path to a root directory, iterate over every file in every subdirectory to
    get each page's plain text contents

    Parameter(s)
    directories: str object, path to the root dir

    Return
    None
    """

    global index_A_C, index_D_F, index_G_I, index_J_L, index_M_O, index_P_R,\
        index_S_U, index_V_X, index_Y_Z, index_misc

    ID: int = 0 # id of file
    count: int = 0
    file_count: int = 0
    t_set: set = set()
    print('Working...')

    for root, dirs, files in os.walk(directories):  # traverse dirs & get files at all levels
        for file in files:  # iterate over every file in the directory
            path = os.path.join(root, file)
            tokens = [] # new list for each file!

            if ".DS_Store" in path:  # this file is hidden in the dir, and isn't a json file; skip it if found
                continue

            js_file = open(path)  # open the file
            js_data = json.load(js_file)  # get file contents
            js_file.close()  # close the file

            # Stuff for ranking
            html_content = js_data['content']  # get the html content from the json dictionary
            url = js_data['url']

            #Some error checking-------------------------------------------------------------------------
            if "cs.ics.uci.edu/news/" in url: # this website has a lot of depreciated links
                continue
            """try:
                response = requests.get(url, timeout = 0.7)
                headers = response.headers
                if "Last-Modified" in headers:
                    last_mod = headers['Last-Modified']
                    last_mod = last_mod.split(' ')
                    yr = last_mod[3]
                    if int(yr) < 2007:
                        continue
                status_code = response.status_code
                if status_code != 200:
                    continue
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.RequestException:
                print('unknown')
                continue
            """ # TAKES WAY TOO LONG FOR MINIMAL BENEFIT
            #-----------------------------------------------------------------------------------------


            soup = BS(html_content, 'html.parser')
            page_text = soup.get_text(strip=True)  # get plain text
            if soup.title:
                title = soup.title.string
            else:
                title = "No title"

            bolds = soup.findAll('b')
            bolds_strs = []
            for bold in bolds:
                bolds_strs.append(bold.string)


            if not check_for_duplicates(page_text): #check if page is a duplicate
                count += 1 #increment total files indexed
                file_count += 1 #increment file count
                tokens.extend([str(token).lower() for token in tokenize(page_text)]) #get tokens
                counter = Counter(tokens)  # automatically count all tokens (duplicates included)
                total_terms = len(tokens)
                tokens = list(OrderedDict.fromkeys(tokens))  # remove duplicates
                ID += 1

                for token in tokens:
                    freq = counter[token] #get the frequency that the token appears in the doc
                    first_char = token[0]
                    #get the first character of token to determine which index to save it to
                    choose_index(token, first_char, freq, ID, url, total_terms, title, bolds_strs)

                if file_count >= 18465: #if file chunk limit is reached
                    update_unique_tokens(t_set) #update the set of unique tokens
                    write_to_files() #write indexes to their files
                    index_A_C = {} #reset the local indexes
                    index_D_F = {}
                    index_G_I = {}
                    index_J_L = {}
                    index_M_O = {}
                    index_P_R = {}
                    index_S_U = {}
                    index_V_X = {}
                    index_Y_Z = {}
                    index_misc = {}
                    file_count = 0 #reset the file chunk count
                    print('Index size limit reached, saving to files.\n')
                    print('Working...\n')

    update_unique_tokens(t_set) #update unique tokens after finished
    write_to_files() #write remaining index to files after finishing
    print('End of files reached. Saved chunks to disk.\n')

    with open('a3_analytics.txt', 'w') as out: #write basic analytics to text file
        out.write(f'Number of indexed documents: {count}\nNumber of unique tokens: {len(t_set)}\n')

    print('Done!\n')
    print('Merging indices...\n')
    merge_indices() #merge the separate indices into one main index
    print('Done!\n')
    print("Calculating tfidf...")
    calculate_tfidf(count)
    print("Done! \n")
    print('Starting partial index...\n')
    partial_index() #create a partial index from the main index
    print('Done! \n')

def choose_index(token, first_char, freq, ID, url, total_terms, title, bolds) -> None:
    #chooses which index to update based on the token (alphabetical)
    global index_A_C, index_D_F, index_G_I, index_J_L, index_M_O,\
            index_P_R, index_S_U, index_V_X, index_Y_Z, index_misc

    if first_char in A_C:
        update_index(token, freq, ID, url, index_A_C, total_terms, title, bolds)
    elif first_char in D_F:
        update_index(token, freq, ID, url, index_D_F, total_terms, title, bolds)
    elif first_char in G_I:
        update_index(token, freq, ID, url, index_G_I, total_terms, title, bolds)
    elif first_char in J_L:
        update_index(token, freq, ID, url, index_J_L, total_terms, title, bolds)
    elif first_char in M_O:
        update_index(token, freq, ID, url, index_M_O, total_terms, title, bolds)
    elif first_char in P_R:
        update_index(token, freq, ID, url, index_P_R, total_terms, title, bolds)
    elif first_char in S_U:
        update_index(token, freq, ID, url, index_S_U, total_terms, title, bolds)
    elif first_char in V_X:
        update_index(token, freq, ID, url, index_V_X, total_terms, title, bolds)
    elif first_char in Y_Z:
        update_index(token, freq, ID, url, index_Y_Z, total_terms, title, bolds)
    else:
        update_index(token, freq, ID, url, index_misc, total_terms, title, bolds)

def update_index(token, freq, ID, url, index, total_terms, title, bolds) -> None:
    #update the given index with a token and Posting values
    if token not in index.keys():
        index[token] = [Posting(ID, freq, url, total_terms, title, bolds)]
    else:
        index[token].append(Posting(ID, freq, url, total_terms, title, bolds))


def update_unique_tokens(t_set: set) -> None:
    #update the set of unique tokens
    t_set.update(list(index_A_C.keys()))
    t_set.update(list(index_D_F.keys()))
    t_set.update(list(index_G_I.keys()))
    t_set.update(list(index_J_L.keys()))
    t_set.update(list(index_M_O.keys()))
    t_set.update(list(index_P_R.keys()))
    t_set.update(list(index_S_U.keys()))
    t_set.update(list(index_V_X.keys()))
    t_set.update(list(index_Y_Z.keys()))
    t_set.update(list(index_misc.keys()))


def write_to_files():
    #write each index to its respective file
    _write_to_file(index_A_C, 'index_A_C.txt')
    _write_to_file(index_D_F, 'index_D_F.txt')
    _write_to_file(index_G_I, 'index_G_I.txt')
    _write_to_file(index_J_L, 'index_J_L.txt')
    _write_to_file(index_M_O, 'index_M_O.txt')
    _write_to_file(index_P_R, 'index_P_R.txt')
    _write_to_file(index_S_U, 'index_S_U.txt')
    _write_to_file(index_V_X, 'index_V_X.txt')
    _write_to_file(index_Y_Z, 'index_Y_Z.txt')
    _write_to_file(index_misc, 'index_misc.txt')

def _write_to_file(index, filename):
    #does the actual writing to the index files

    for key, value in index.items():
        #converts posting objects into dictionaries
        #in the form {ID, frequency, url}
        for i in range(len(value)):
            value[i] = value[i].to_dictionary()


    if not os.path.exists(filename): #check if file exists already
        with open(filename, 'w') as out: #if it doesn't, simply write the index to the file
            for key, value in sorted(index.items()): #writes one line per token
                out.write(f'{{"{key}": {value}}}\n')
    else:
        with open(filename, 'r') as out: #if it exists, load the index from the file to update it
            data = [ast.literal_eval(dic) for dic in out.readlines()]
            #collects the data and transforms each line into a usable dictionary

        temp_dic = {}
        temp_dic.update(index) #populate a temporary dictionary with the current index

        for d in data: #for each {token: [postings]} in the data extracted
            for key, value in temp_dic.items(): #iterate over temp dictionary items
                if key in d: #if the index key exists in the file already, append the postings
                    d[key].extend(value)
                    del index[key] #delete the appended item from the current index

        with open(filename, 'w', encoding = 'utf-8') as out:
            data = [str(d) + '\n' for d in data] #convert the index back ito the string format
            out.writelines(data) #write the data back to the file
            for key, value in sorted(index.items()):
                #write the new items from the index into the end of the file
                out.write(f'{{"{key}": {value}}}\n')


def merge_indices(): #merges all the index files that were created
    with open('main_index.txt', 'w') as file:
        for index in index_list:
            with open(index, 'r') as infile:
                data = infile.readlines() #get the data from the file
            file.writelines(data) #write this data into the main index file
            os.remove(index) #delete the index chunk from disk
