import re

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


def check_patterns(text,pattern):

    matches = pattern.finditer(text)
    words = pattern.findall(text)

    return matches, words

def check_words(word):
    word = word.lower()
    allowed = word in dictionary or word in med_dictionary or word.isdigit()
    not_allowed = word in firstnames or word in lastnames or word in months
    #print allowed, not_allowed
    if allowed and not_allowed:
        #print "indeterm"
        return "indeterminate" 
    if not_allowed:
        #print "not allowed ran"
        return "not allowed"
    if allowed:
       #print  "allowed ran"
       return "allowed"

    if not allowed and not not_allowed:
        #print "found neither"
        return "indeterminate"

    #print "Oh no it didn't catch"
    

def main():

    myfile = open("September 2015 Samples De-Identified2.csv",'r')
    patterns = [re.compile(p) for p in \
                ['[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}',
                '^\d{1,2}[\W]\d{2,4}$']]

    line = myfile.read()
    line = line.replace(","," ")
    words = line.split(" ")
    allowed = {}
    not_allowed = {}
    indeterminate = {}
    

    a = ["hello","simple","sample"]
    for word in words:
        result =check_words(word)
        if result == 'allowed':
            if word in allowed:
                allowed[word] = allowed[word] + 1
            else:
                allowed[word] = 1
        elif result == 'not_allowed':
            if word in not_allowed:
                not_allowed[word] = not_allowed[word] + 1
            else:
                not_allowed[word] = 1
        else:
            if word in indeterminate:
                indeterminate[word] = indeterminate[word] + 1
            else:
                indeterminate[word] = 1

    a = [[allowed,"allowed"],[not_allowed,"not allowed"],
         [indeterminate,"indeterminate"]]
    for word_list in a:
        print word_list[1]
        print"_________________________________________________________"
        for k,v in word_list[0].items():
            print k + ":", v
        
    

if __name__ =='__main__':
    main()
