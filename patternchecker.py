import re
import os
import pickle

def check_for_dates(text):
    """Removes dates and numbers that may look like dates from a string
    Args:
        text (str): string of text to remove dates from

    Returns:
        matched_dates (list)
        non_date_words (str)
    """
    date_pattern = re.compile(
        '[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}|\d{1,2}[\W]\d{2,4}') #dates

    punct_pattern = re.compile(r'[^\w]+') #matches punctuation

    date_locations = date_pattern.finditer(text)
    matched_dates = date_pattern.findall(text)
    #print text, "before date removed"
    non_date_words = " ".join(date_pattern.split(text)) # remove dates
    #print non_date_words, "after date removed"
    non_date_words = " ".join(punct_pattern.split(non_date_words)) # remove punct
    #print non_date_words, "after punct removed"
    return matched_dates, non_date_words

def check_for_words(text):
    """Checks for wors in a string of text that are clearly english words that
    aren't protected health information. Returns a list of allowe, not allowed,
    and indeterminate words from the text

    Args:
        text (str): sring of text to check for word matches

    Returns:
        allowed,not_allowed,indeterminate (list): list containing words from
        given text in their category
    """
    dictionary = dict() #container for allowed english words
    firstnames = dict() #container for prohibited first names
    lastnames = dict()  #container for prohibited last names
    medicaldict = dict()#container for allowed medical words
    
    file_list = [["englishwordslist",dictionary], #pickle files with word list
                     ["firstnameslist",firstnames],
                     ["lastnameslist",lastnames],["medicalwordlist",medicaldict]]

    for pair in file_list: # create list to use in program to check words
        myfile = open(pair[0],'r')
        pair[1] = pickle.load(myfile)

    dictionary = file_list[0][1]
    firstnames = file_list[1][1]
    lastnames = file_list[2][1]
    medicaldict = file_list[3][1]

    user_all_dict = list() #User defined dictionary of allowed words
    user_not_all_dict = list() #User defined dictionary of prohibited words
    months = ['january','february','march','april','may','june',
              'july','august','september','october','november','december']
    

    if os.path.exists('userallowedlist'): #Open saved user file if exist
        saved_list = open('userallowedlist','r')
        try:
            user_all_dict = pickle.load(saved_list)
        except EOFError: #if list is empty skip
            pass
        saved_list.close()
        
    if os.path.exists('usernotallowedlist'): #Open save user file if exist
        saved_list = open('usernotallowedlist','r')
        try:
            user_not_all_dict = pickle.load(saved_list)
        except EOFError:#if list is empty skip
            pass
        saved_list.close()

    text = text.split(" ") #Convert given str to list. necessary?
    allowed_words = list()
    not_allowed_words = list()
    indeterminate = list()

    

    for word in text:
        #print "word is", word
        original_word = word #keep record of unaltered word
        word = word.lower() # all dictionarys use lower case words
        #print "word in user_all_dict", word in user_all_dict
        #print "word in user_not_all_dict", word in user_not_all_dict
        if user_all_dict != [] and word in user_all_dict:
            #words user wants to pass
            #print "user allowed ran"
            allowed_words.append(original_word)
            continue

        if user_not_all_dict != [] and word in user_not_all_dict:
            #words user doesn't want to pass
            #print "not user allowed ran"
            not_allowed_words.append(original_word)
            continue
        
        allowed = word in dictionary or word in medicaldict or word.isdigit()
        not_allowed = word in firstnames or word in lastnames or word in months
        #print "word in allowed", allowed,"word in not allowed", not_allowed
        if allowed and not_allowed and word != "":
            #print "allowed and not allowed ran"
            indeterminate.append(original_word)
            continue
            
        if not_allowed and not allowed:
            #print "not allowed ran"
            not_allowed_words.append(original_word)
            continue
        if allowed and not not_allowed:
           #print  "allowed ran"
           allowed_words.append(original_word)
           continue

        if not allowed and not not_allowed and word != "":
            #print "found neither"
            indeterminate.append(original_word)
            continue

        #print "Oh no it didn't catch"
    return allowed_words, not_allowed_words, indeterminate
        
        
    
def main():

    test_string = "Hello - vancomycin - name is Seth. Today is 12.15.1234 or 12/2015"

    dates, non_matched = check_patterns(test_string)
    a,b,c = check_words(non_matched)
    ##print a
    ##print
    ##print b
    ##print
    ##print c

if __name__ == '__main__':
    main()
    
    
