    
def data_prep():
    import pandas as pd 
    import numpy as np
    
    

    #Importing the data and basic preparing
    names = pd.read_csv("All_Elvish_Names")

    names.drop("Unnamed: 0", axis=1)

    names["input"] = names["Elvish_Names"].apply(lambda x : "\t" + x)

    names["target"] = names["Elvish_Names"].apply(lambda x : x[:len(x)] + "\n")
    
    def get_vocabulary(names):  
        # Define vocabulary to be set
        all_chars=set()
    
        # Add the start and end token to the vocabulary
        all_chars.add('\t')
        all_chars.add('\n')  
        
        # Iterate for each name
        for name in names:
            
            # Iterate for each character of the name
            for c in name:
                
                if c not in all_chars:
                    # If the character is not in vocabulary, add it
                    all_chars.add(c)
                    
                    # Return the vocabulary
        return all_chars
    
    
    #Getting the Vocabalary
    global vocab
    vocab = get_vocabulary(names["input"])

    vocab_sorted = sorted(vocab)

    char_to_idx = {char:idx for idx, char in enumerate(vocab_sorted)}

    global max_len
    max_len = len(max(names["input"], key=len)) #Finding the longest Name


    # Initialize the input vector
    global input_data
    input_data = np.zeros(
        (len(names['input']), 
         max_len+1,
         len(get_vocabulary(names['input']))), 
        dtype='float32')
    
    # Initialize the target vector
    global target_data
    target_data = np.zeros(
        (len(names['input']), 
         max_len+1,
         len(get_vocabulary(names['input']))), 
        dtype='float32')
    

    #Filling the Empy vectors with data
    # Iterate for each name in the dataset
    for n_idx, name in enumerate(names["input"]):
        # Iterate over each character and convert it to a one-hot encoded vector
        for c_idx, char in enumerate(name):
            input_data[n_idx, c_idx, char_to_idx[char]] = 1
            
            
            
    # Iterate for each name in the dataset
    for n_idx, name in enumerate(names["target"]):
        # Iterate over each character and convert it to a one-hot encoded vector
        for c_idx, char in enumerate(name):
            target_data[n_idx, c_idx, char_to_idx[char]] = 1
            
    return None





def get_names(model,  amount_of_names):
    '''
    Get the shapes from the input data
    '''
    import pandas as pd 
    import numpy as np

    #Importing the data and basic preparing
    names = pd.read_csv("All_Elvish_Names")
    
    names.drop("Unnamed: 0", axis=1)
    
    names["input"] = names["Elvish_Names"].apply(lambda x : "\t" + x)
        
    def get_vocabulary(names):  
       # Define vocabulary to be set
       all_chars=set()

       # Add the start and end token to the vocabulary
       all_chars.add('\t')
       all_chars.add('\n')  
       
       # Iterate for each name
       for name in names:
           
           # Iterate for each character of the name
           for c in name:
               
               if c not in all_chars:
                   # If the character is not in vocabulary, add it
                   all_chars.add(c)
                   
                   # Return the vocabulary
       return all_chars
    
    vocab = get_vocabulary(names["input"])
    vocab_sorted = sorted(vocab)
    
    max_len = len(max(names["input"], key=len)) #Finding the longest Name
    

    
    '''
    This Part of the function uses the model to generate names
    '''
    char_to_idx = {char:idx for idx, char in enumerate(vocab_sorted)}
    
    output_seq = np.zeros((1, max_len+1, len(vocab))) 
    output_seq[0, 0, char_to_idx['\t']] = 1
    
    all_generated_names = []
    
    for amount in range(0,amount_of_names):
        
        string_list = ""
        #Create a name
        for i in range(0,max_len):
            probs = model.predict_proba(output_seq, verbose=0)[:,i,:]
            char = np.random.choice(vocab_sorted, replace=False, p=probs.reshape(len(vocab)))
            if char != "\n":
                string_list = string_list + char
            else:
                break
                
        all_generated_names.append(string_list)
            
            
            
    return all_generated_names