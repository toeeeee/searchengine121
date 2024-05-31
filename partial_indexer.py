import ast

def partial_index(): #create the partial index
    create_partial_index('tfidf_index.txt')

def create_partial_index(index): #actually creates the partial index
    p_index = {} #make the dictionary where the partial index will be stored

    with open(index, 'r') as f:
        byte = 0 #set byte offset to 0
        line = f.readline()
        while line: #read each line of the index (in the form {token: [postings]}
            data = ast.literal_eval(line) #convert each line into a dictionary
            token = list(data.keys())[0] #get the token from the dictionary we extracted
            p_index[token] = byte #set the value to the byte offset (location of that token)
            byte = f.tell() #update the byte offset
            line = f.readline() #read the next line

    with open('partial_index.txt', 'w') as f:
        f.write(str(p_index)) #write the partial index to its own file