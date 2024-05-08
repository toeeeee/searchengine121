from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


def tokenize(parsed_text: str) -> list:
    """
    Parameters
    parsed_text: a string object of plain text
    
    Return
    tokens_list: a list of all the words in the string. Words that are hyphenated or that have apostrophes in them are counted as single tokens.
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
    # tokenize("i can't believe it's may 7th, and we're still waiting for the sun to shine. asdf-qwer zxcv/tyui")
    pass
