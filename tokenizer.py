import hashlib
from sqllite_context_manager import SQLite
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def tokenize(parsed_text: str) -> list:
    """
    Given text in str format, split up the string into all of its constituent words. Words that are hyphenated or have apostrophes are counted as single tokens.

    Parameters
    parsed_text: a string object of plain text

    Return
    tokens_list: a list of strings (tokens)
    """

    # regex pattern: split text into separate tokens, keeping hyphenated words and words with apostrophes together
    # pattern = r"\b(?:[a-zA-Z]+(?:'[a-zA-Z]+)?(?:-[a-zA-Z]+)?)\b"
    pattern = r'\b\d+\.\d+\b|\b\d+\b|\b\w+(?:-\w+)*\b|\b\w+(?:\'\w+)*\b'
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


# SAME PAGE CHECK CODE -------------------------------------------------------------------------------------------------
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


# SIMHASHING CODE ------------------------------------------------------------------------------------------------------
def string_to_binary_hash(string):
    hash_value = hashlib.sha256(string.encode()).hexdigest()
    binary_hash = bin(int(hash_value, 16))[2:] # remove header of binary string
    binary_hash = binary_hash[:10].zfill(10)
    return binary_hash

def list_to_binary_hash(string_list):
    binary_hashes = []
    for string in string_list:
        binary_hash = string_to_binary_hash(string)
        binary_hashes.append(binary_hash)
    return binary_hashes

def computeWordFrequencies(tokens) -> dict :  # return frequencies of file's tokens
    instances = {} # dict of frequencies of words in the given text file
    for token in tokens:
        if token not in instances:
            instances[token] = 0
        instances[token] += 1
    return instances

def count_digit(token_freq):
    data_for_fingerprint = []
    for x in range(10):
        bit_sum = 0
        for key, value in token_freq.items():
            if get_digit(int(key), x) > 0:
                bit_sum += value
            else:
                bit_sum -= value
        data_for_fingerprint.append(bit_sum)
    return data_for_fingerprint

# The // performs integer division by a power of ten to move the digit to the ones position, 
# then the % gets the remainder after division by 10.
# Note that the numbering in this scheme uses zero-indexing and starts from the right side of the number.
def get_digit(number, n):
    return number // 10**n % 10

def generate_fingerprint(list):
    fingerprint = []
    for value in list:
        if value > 0:
            fingerprint.append(1)
        else:
            fingerprint.append(0)
    return fingerprint

#if its similar return true, else return false
def compare_fingerprint(previous_hash, new_fingerprint):
    #see how many bits are the same from the first fingerprint to the second
    similarity_score = 0
    threshold = 0.85
    for x in range(10):
        if previous_hash[x] == new_fingerprint[x]:
            similarity_score += 1
    if similarity_score/10 > threshold:
        return True
    return False

#handles calendar webpages/ blogs/ events
#values of the binary are reversed, that means the data originally is 1-2-3-4-5, but our fingerprint is stored as 5-4-3-2-1
#if you want to access these values, start from the beginning of the fingerprint (but know that that's the last hash)
def sim_hash(previous_hash, tokens):
    global PREVIOUS_HASH

    hash_tokens = list_to_binary_hash(tokens)
    token_freq = computeWordFrequencies(hash_tokens)
    #print(token_freq)
    fingerprint = generate_fingerprint(count_digit(token_freq))
    if PREVIOUS_HASH:
        if compare_fingerprint(previous_hash, fingerprint) == True:
            return True
    PREVIOUS_HASH = fingerprint
    return False
