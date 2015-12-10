import re
import os

dictionary_file = open("completedict.txt","r")
first_name_file = open("firstnames.txt",'r')
last_name_file = open("lastnames.txt",'r')
med_dictionary_file = open("wordlist.txt",'r')
med_dictionary = {}
dictionary ={}
firstnames = {}
lastnames = {}
months = ['january','february','march','april','may','june',
              'july','august','september','october','november','december']
for line in dictionary_file:    
    dictionary[line.rstrip("\n").lower()] = None

for line in first_name_file:    
    firstnames[line.rstrip("\n").lower()] = None
    
for line in last_name_file:    
    lastnames[line.rstrip("\n").lower()] = None

for line in med_dictionary_file:
    med_dictionary[line.rstrip("\n").lower()] = None


def check_patterns(text):
    pattern = re.compile(
        '[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}|^\d{1,2}[\W]\d{2,4}$')
    

    matched_word_locations = pattern.finditer(text)
    matched_words = pattern.findall(text)
    unmatched_words = pattern.split(text)
    unmatched_words = " ".join(unmatched_words)
    unmatched_words, unmatched_word_locations = \
                     remove_punctuation(unmatched_words)

    return matched_words, unmatched_words

def remove_punctuation(text):
    pattern = re.compile(r'[^\w]+')
    matches = pattern.finditer(text)
    for match in matches:
        s = match.start()
        e = match.end()
        #print "match was", text[s:e]
    removed = pattern.split(text)
    return " ".join(removed), matches

def find_user_know_words(text):
    text = text.split(" ")
    #print "text is",text
    indeterminate = []
    for word in text:
        print "word is",word
        originalword = word
        word = word.lower()
        allowed = word in dictionary or word in med_dictionary or word.isdigit()
        not_allowed = word in firstnames or word in lastnames or word in months
        print allowed, not_allowed
        if allowed and not_allowed and word != "":
            print "allowed and not allowed"
            indeterminate.append(originalword)  

        if not allowed and not not_allowed and word != "":
            print "found neither"
            indeterminate.append(originalword)

        print "Oh no it didn't catch"
    return indeterminate

def check_words(text):
    user_allowed_dict = None
    user_not_allowed_dict = None
    if os.path.exists('useralloweddictionary.txt'):
        user_allowed_dict = []        
        myfile = open('useralloweddictionary.txt','r')
        for line in myfile:
            user_allowed_dict.append(line.rstrip("\n"))
            
    if os.path.exists('usernotalloweddicttxt'):
        user_not_allowed_dict = []        
        myfile = open('usernotalloweddict.txt','r')
        for line in myfile:
            user_not_allowed_dict.append(line.rstrip("\n"))
    text = text.split(" ")
    #print "text is",text
    allowed_words = []
    not_allowed_words = []
    indeterminate = []
    for word in text:        
        #print "word is",word
        originalword = word
        word = word.lower()
        
        if user_allowed_dict and word in user_allowed_dict:
            allowed_words.append(word)
            continue

        if user_not_allowed_dict and word in user_not_allowed_dict:
            not_allowed_word.append(word)
            continue
        
        allowed = word in dictionary or word in med_dictionary or word.isdigit()
        not_allowed = word in firstnames or word in lastnames or word in months
        #print allowed, not_allowed
        if allowed and not_allowed and word != "":
            indeterminate.append(originalword)
            continue
            
        if not_allowed and not allowed:
            #print "not allowed ran"
            not_allowed_words.append(originalword)
            continue
        if allowed and not not_allowed:
           #print  "allowed ran"
           allowed_words.append(originalword)
           continue

        if not allowed and not not_allowed and word != "":
            #print "found neither"
            indeterminate.append(originalword)
            continue

        #print "Oh no it didn't catch"
    return allowed_words, not_allowed_words, indeterminate

def check_words_final(text,userdict):
    text = text.split(" ")
    #print "text is",text
    allowed_words = []
    not_allowed_words = []
    indeterminate = []
    for word in text:
        #print "word is",word
        originalword = word
        word = word.lower()
        user_allowed = word in userdict
        allowed = word in dictionary or word in med_dictionary or word.isdigit()
        not_allowed = word in firstnames or word in lastnames or word in months
        #print allowed, not_allowed

        if user_allowed:
            #print "user allowed ran"
            allowed_words.append(originalword)
            break
        if allowed and not_allowed and word != "":
            indeterminate.append(originalword)
            
        if not_allowed and not allowed:
            #print "not allowed ran"
            not_allowed_words.append(originalword)
        if allowed and not not_allowed:
           #print  "allowed ran"
           allowed_words.append(originalword)

        if not allowed and not not_allowed and word != "":
            #print "found neither"
            indeterminate.append(originalword)

        #print "Oh no it didn't catch"
    return allowed_words, not_allowed_words, indeterminate
    
   

def main():

    myfile = open("September 2015 Samples De-Identified2.csv",'r')
    patterns = [re.compile(p) for p in \
                ['[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}',
                '^\d{1,2}[\W]\d{2,4}$']]

    line = myfile.read()
    line = line.replace(","," ")

    allowed,not_allowed,indeterminate = check_words(line)   


    a = [[allowed,"allowed"],[not_allowed,"not allowed"],
         [indeterminate,"indeterminate"]]
    for word_list in a:
        print word_list[1]
        print"_________________________________________________________"
        for word in word_list[0]:
            print word
        
    

if __name__ =='__main__':
    main()
