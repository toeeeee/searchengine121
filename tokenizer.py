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
    return tokens_list


if __name__ == '__main__':
    pass
    # print( tokenize("I can't believe it's May 7th, and we're still waiting for the sun to shine. asdf-qwer zxcv/tyui") )
