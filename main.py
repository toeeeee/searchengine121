import parse
import os

'''
main.py -> parse.py
'''

def run():
    if os.path.isfile("hashes.db"):
        os.remove("hashes.db")
    if os.path.isfile("tfidf_index.txt"):
        os.remove("tfidf_index.txt")
    if os.path.isfile("partial_index.txt"):
        os.remove("partial_index.txt")
    
    user_path = input( "Please enter the path to your folder of domain folders (ANALYST or DEV): ")
    parse.build_index( user_path ) 


if __name__ == '__main__':
    run()
