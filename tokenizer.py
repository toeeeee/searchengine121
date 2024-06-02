import hashlib
from sqllite_context_manager import SQLite
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def update_global_dict(tokens_list: list) -> None:
    """
    Given a list of words, add them to the global dictionary of word frequencies (this dict counts frequency of word encounters across all pages visited).

    Parameter(s)
    tokens_list: list of tokens generated from 'tokenize' function

    Return
    None
    """

    # globals.FREQ_DICT

    for token in tokens_list:
        try:
            # increment the number of times this token has been encountered by 1
            globals.FREQ_DICT[token] += 1
        except KeyError:
            # if the token isn't in the dict, this must be the first time this token has been encountered: add the token to dict with frequency of encounters = 1
            globals.FREQ_DICT[token] = 1
    return


def update_page_dict(tokens_list: list) -> dict:
    """
    Given a list of tokens, add them to the dictionary of tokens encountered.

    Parameter(s)
    tokens_list: list of tokens

    Return
    dictionary object of unique tokens encountered and their frequencies
    """

    freq_dict = {}
    for token in tokens_list:
        try:
            # increment the number of times this token has been encountered by 1
            freq_dict[token] += 1
        except KeyError:
            # if the token isn't in the dict, this must be the first time this token has been encountered: add the token to dict with frequency of encounters = 1
            freq_dict[token] = 1

    return freq_dict


def tokenize(parsed_text: str) -> list:
    """
    Given text in str format, split up the string into all of its constituent words. Words that are hyphenated or have apostrophes are counted as single tokens.

    Parameters
    parsed_text: a string object of plain text

    Return
    tokens_list: a list of strings (tokens)
    """

    # regex pattern: split text into separate tokens, keeping hyphenated words and words with apostrophes together
    # also keeps together space + numbers
    pattern = r"\b(?:[a-zA-Z0-9]+(?:'[a-zA-Z]+)?(?:-[a-zA-Z]+)?)\b"
    # Create a tokenizer using the custom pattern
    tokenizer = RegexpTokenizer(pattern)
    # Tokenize the given text
    tokens_list = tokenizer.tokenize(parsed_text)
    # create a stemmer
    stemmer = PorterStemmer()
    # convert all word-tokens into their stems (ex.: "dogs" -> "dog")
    tokens_list = [stemmer.stem(word) for word in tokens_list]

    # globals.DOCID += 1  # this is the ith page visited: increment the counter by 1
    return tokens_list


def check_for_duplicates(text: str) -> bool:
    """
    check if the current page is an exact duplicate of other pages already visited. Does so by creating a sha256 hash object of the text,

    Parameters
    text: a str object of the plain text of a page
    url: a str object of the page's url

    Return
    a boolean object: True if this page is an exact duplicate of one already visited, False otherwise
    """

    hash_obj = hashlib.sha256(text.encode()).hexdigest()  # generate the sha256 hash of the given text
    # create a connection to the database 'hashes.db' (creates the db if it doesn't already exist)
    with SQLite("hashes.db") as db:
        # check if the 'hashes' table already exists in the 'hashes' db
        res = db.cursor.execute("SELECT name FROM sqlite_master WHERE name='hashes'")
        res = res.fetchone()  # if res == anything other than None, then it exists in db
        if not res:  # if it doesn't exist, create the 'hashes' table
            db.cursor.execute("CREATE TABLE hashes (hash STR)")  # table created with one column named 'hash'
            db.connection.commit()  # commit the CREATE TABLE transaction to the db

        # check if hash already in db
        res = db.cursor.execute("SELECT * FROM hashes WHERE hash = ?", (hash_obj,))
        res = res.fetchone()  # if res == anything other than None, it was found in the table
        if res:  # since it's in db, return True: this page is a duplicate of one already crawled over
            return True
        # otherwise, add its hash to the table
        db.cursor.execute(f"""INSERT INTO hashes(hash) VALUES(?)""", (hash_obj, ))
        db.connection.commit()  # commit the INSERT transaction to db

    return False


if __name__ == '__main__':
    pass