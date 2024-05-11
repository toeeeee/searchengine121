import parse
import globals
import postings
import tokenizer


# def build_index(docs_list):
#     hashTable = dict()
#     n = 0
#     for doc in docs_list:
#         n += 1
#         parsed_text = parse.parse(doc)
#         tokens_list = tokenizer.tokenize(parsed_text)
#         unique_tokens = list( set(tokens_list) )  # get all unique 
#         for token in unique_tokens:
#             if token not in hashTable:
#                 hashTable[token] = list( postings )  # TODO
#             hashTable[token].append( postings.list[n] )  # TODO

#     return hashTable

"""
procedure BUILDINDEX(D)
    I = HashTable()
    n = 0
    for all documents d in D do
        n = n + 1
        T = Parse(d)
        Remove duplicates from T
        for all tokens t in T do 
            if I[t] not in I then
                I[t] = list(Posting)
            end if 
            I[t].append(Posting(n))
        end for
    end for
    return I
end procedure

* D is a set of text documents
        * Inverted list storage
    * Document numbering
* Parse document into tokens
"""

def run():
    user_path = input( "Please enter the path to your folder of domain folders (ANALYST or DEV): ")
    parse.build_index( user_path )
    #tokens_list = tokenizer.tokenize(parsed_text)


if __name__ == '__main__':
    run()
