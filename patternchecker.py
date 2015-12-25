import re
import os
import pickle
import datecheckers
import patternmaker

def check_for_dates(text):
    """Removes dates and numbers that may look like dates from a string.

    Args:
        text (str): string to remove dates from

    Returns:
        list: list of dates that were removed from string
        str: original string with dates removed
    
    >>> dates, non_dates = list(), list()
    >>> dates, non_dates = check_for_dates('2/12/2015, 2/2015,boxing'.replace(","," "))
    >>> dates == ['2/12/2015', '2/2015']
    True
    >>> non_dates == 'boxing'
    True
    
    """
    date_pattern = re.compile(
        '[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}|\d{1,2}[\W]\d{2,4}') #dates

    punct_pattern = re.compile(r'[^\w]+') #matches punctuation

    date_locations = date_pattern.finditer(text)
    matched_dates = date_pattern.findall(text)
    for date in matched_dates[:]:
        if not datecheckers.isDate(date):
            matched_dates.remove(date) #pass words that just look like dates
    pattern_template = \
                     '\A(%s)(\W)*( )|( )(%s)(\W)*( )|( )(%s)(\W)*\Z'
    matched_dates_patterns  = \
                           patternmaker.make_re(pattern_template,matched_dates)
    non_date_words = text[:]
    for date in matched_dates_patterns: #remove dates from string
        temp = date.sub(" ", non_date_words[:])
        non_date_words = temp
    #remove punc and leading spaces
    non_date_words = " ".join(punct_pattern.split(non_date_words[:])).strip()
    return matched_dates, non_date_words

def check_for_words(text):
    """Parses string and categorzes each words as allowed/notallowed/indeterm.

    Args:
        text (str): str to check for words.

    >>> allowed,not_allowed,indeterminate = check_for_words('Hello my vancomycin Seth Pitts blaze')
    >>> allowed == ['Hello', 'vancomycin']
    True
    >>> not_allowed == ['Seth', 'Pitts']
    True
    >>> indeterminate == ['my', 'blaze']
    True
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
        original_word = word #keep record of unaltered word
        word = word.lower() # all dictionarys use lower case words
        if user_all_dict != [] and word in user_all_dict:
            #words user wants to pass
            allowed_words.append(original_word)
            continue

        if user_not_all_dict != [] and word in user_not_all_dict:
            #words user doesn't want to pass
            not_allowed_words.append(original_word)
            continue
        
        allowed = word in dictionary or word in medicaldict or word.isdigit()
        not_allowed = word in firstnames or word in lastnames or word in months
        if allowed and not_allowed and word != "":
            #found in both allowed and not allowed list
            indeterminate.append(original_word)
            continue            
        if not_allowed and not allowed:
            #only found in not allowed list
            not_allowed_words.append(original_word)
            continue
        if allowed and not not_allowed:
            #only found in allowed list
           allowed_words.append(original_word)
           continue

        if not allowed and not not_allowed and word != "":
            #unidentifed word(mispelled?)
            indeterminate.append(original_word)
            continue
    return allowed_words, not_allowed_words, indeterminate
        
        
    
def main():

    test_string = '2/12/2015, 2/2015,boxing bitches'.replace(",", " ")

    dates, non_matched = check_for_dates(test_string)
    print dates, "dates"
    print non_matched.strip(), non_matched.strip() == 'boxing bitches',  "non dates"

if __name__ == '__main__':
    main()
    
    
