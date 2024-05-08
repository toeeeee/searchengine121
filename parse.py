import os
import re
import json
from bs4 import BeautifulSoup as BS

def build_index(directories):
    """
    
    """
    index = {}
    ID = 0
    for root, dirs, files in os.walk(directories):  # traverse dirs & get files at all levels
        for file in files:  # iterate over every file in the directory
            path = os.path.join(root, file)

            if ".DS_Store" in path:  # this file is hidden in the dir, and isn't a json file; skip it if found
                continue

            js_file = open(path)  # open the file
            js_data = json.load(js_file)  # get file contents
            js_file.close()  # close the file

            html_content = js_data['content']  # get the html content from the json dictionary
            page_text = BS(html_content, 'html.parser').get_text(strip=True)  # get plain text
            page_text = page_text.lower()


if __name__ == '__main__':
    # build_index( "/home/farhanz/CS_121/Assignment_3/searchengine121/ANALYST" )
    pass
