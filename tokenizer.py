import globals
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

    globals.FREQ_DICT

    for word in tokens_list:
        try:  # increment the number of times this word has been found by 1
            globals.FREQ_DICT[word] += 1
        except:  # if the word isn't in the dict, then add it to dict
            globals.FREQ_DICT[word] = 1
    return


def update_page_dict(tokens_list: list) -> dict:
    """
    Given a list of words, add them to the dictionary of word encounters.

    Parameter(s)
    tokens_list: list of word/tokens

    Return
    dictionary object of unique words encountered and their frequencies
    """

    freq_dict = {}
    for word in tokens_list:
        try:  # increment the number of times this word has been found by 1
            freq_dict[word] += 1
        except:  # if the word isn't in the dict, then add it to dict
            freq_dict[word] = 1
    
    return freq_dict


def tokenize(parsed_text: str) -> list:
    """
    Given text in str format, split up the string into all of its constituent words. Words that are hyphenated or have apostrophes are counted as single tokens.

    Parameters
    parsed_text: a string object of plain text
    
    Return
    tokens_list: a list of all the words in the string
    """

    # regex pattern that splits the string into separate word-tokens
    pattern = r"\b(?:[a-zA-Z]+(?:'[a-zA-Z]+)?(?:-[a-zA-Z]+)?)\b"
    # Create a tokenizer using the custom pattern
    tokenizer = RegexpTokenizer(pattern)
    # Tokenize the given text
    tokens_list = tokenizer.tokenize(parsed_text)
    # create a stemmer
    stemmer = PorterStemmer()
    # convert all word-tokens into their stems (ex.: "dogs" -> "dog")
    tokens_list = [stemmer.stem(word) for word in tokens_list]

    return tokens_list


if __name__ == '__main__':
    # print( tokenize("i can't believe it's may 7th, and we're still waiting for the sun to shine. asdf-qwer zxcv/tyui") )
    pass
