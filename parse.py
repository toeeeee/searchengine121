import os
import ujson as json
from bs4 import BeautifulSoup as BS
from collections import Counter, OrderedDict
from tokenizer import tokenize, check_for_duplicates
from postings import Posting

A_C = ['a','b','c']
D_F = ['d','e','f']
G_I = ['g','h','i']
J_L = ['j','k','l']
M_O = ['m','n','o']
P_R = ['p','q','r']
S_U = ['s','t','u']
V_X = ['v','w','x']
Y_Z = ['y','z']

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

    ID: int = 0
    count = 0
    file_count = 0
    t_set = set()
    print('Working...')

    for root, dirs, files in os.walk(directories):  # traverse dirs & get files at all levels
        for file in files:  # iterate over every file in the directory
            path = os.path.join(root, file)
            tokens = []

            if ".DS_Store" in path:  # this file is hidden in the dir, and isn't a json file; skip it if found
                continue

            js_file = open(path)  # open the file
            js_data = json.load(js_file)  # get file contents
            js_file.close()  # close the file

            html_content = js_data['content']  # get the html content from the json dictionary
            url = js_data['url']
            page_text = BS(html_content, 'html.parser').get_text(strip=True)  # get plain text

            if not check_for_duplicates(page_text): #check if page is a duplicate
                count += 1 #increment total files indexed
                file_count += 1 #increment file count
                tokens.extend([token.lower() for token in tokenize(page_text)]) #get tokens
                counter = Counter(tokens)  # for counting frequencies
                tokens = list(OrderedDict.fromkeys(tokens))  # remove duplicates
                ID += 1

                for token in tokens:
                    freq = counter[token]
                    first_char = token[0]

                    choose_index(token, first_char, freq, ID, url)

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
                    print('Working...')

    update_unique_tokens(t_set)
    write_to_files()
    print('End of files reached. Saved chunks to disk.')

    with open('a3_analytics.txt', 'w') as out:
        out.write(f'Number of indexed documents: {count}\nNumber of unique tokens: {len(t_set)}\n')

    print('Done!')

def choose_index(token, first_char, freq, ID, url) -> None:
    global index_A_C, index_D_F, index_G_I, index_J_L, index_M_O,\
            index_P_R, index_S_U, index_V_X, index_Y_Z, index_misc

    if first_char in A_C:
        update_index(token, freq, ID, url, index_A_C)
    elif first_char in D_F:
        update_index(token, freq, ID, url, index_D_F)
    elif first_char in G_I:
        update_index(token, freq, ID, url, index_G_I)
    elif first_char in J_L:
        update_index(token, freq, ID, url, index_J_L)
    elif first_char in M_O:
        update_index(token, freq, ID, url, index_M_O)
    elif first_char in P_R:
        update_index(token, freq, ID, url, index_P_R)
    elif first_char in S_U:
        update_index(token, freq, ID, url, index_S_U)
    elif first_char in V_X:
        update_index(token, freq, ID, url, index_V_X)
    elif first_char in Y_Z:
        update_index(token, freq, ID, url, index_Y_Z)
    else:
        update_index(token, freq, ID, url, index_misc)

def update_index(token, freq, ID, url, index) -> None:
    if token not in index.keys():
        index[token] = [Posting(ID, freq, url)]
    else:
        index[token].append(Posting(ID, freq, url))


def update_unique_tokens(t_set: set) -> None:
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
    _write_to_file(index_A_C, 'index_A_C.json')
    _write_to_file(index_D_F, 'index_D_F.json')
    _write_to_file(index_G_I, 'index_G_I.json')
    _write_to_file(index_J_L, 'index_J_L.json')
    _write_to_file(index_M_O, 'index_M_O.json')
    _write_to_file(index_P_R, 'index_P_R.json')
    _write_to_file(index_S_U, 'index_S_U.json')
    _write_to_file(index_V_X, 'index_V_X.json')
    _write_to_file(index_Y_Z, 'index_Y_Z.json')
    _write_to_file(index_misc, 'index_misc.json')

def _write_to_file(index, filename):

    for key, value in index.items():
        for i in range(len(value)):
            value[i] = value[i].to_dictionary()


    if not os.path.exists(filename): #check if file exists already
        with open(filename, 'w') as out:
            json.dump(index, out)
    else:
        with open(filename, 'r') as out: #if it exists, load the index from the file to update it
            data = json.load(out)
            for key, value in index.items():
                for posting in value:
                    try:
                        data[key].append(posting)
                    except KeyError:
                        data[key] = [posting]

        with open(filename, 'w') as out:
            json.dump(data, out)



if __name__ == '__main__':
    # build_index( "/home/farhanz/CS_121/Assignment_3/searchengine121/ANALYST" )
    pass
