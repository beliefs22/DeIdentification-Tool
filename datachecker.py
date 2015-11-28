import re

dictionary_file = open("completedict.txt","r")
first_name_file = open("firstnames.txt",'r')
last_name_file = open("lastnames.txt",'r')
med_dictionary_file = open("wordlist.txt",'r')
med_dictionary = {}
dictionary ={}
firstnames = {}
lastnames = {}
for line in dictionary_file:    
    dictionary[line.rstrip("\n").lower()] = None

for line in first_name_file:    
    firstnames[line.rstrip("\n").lower()] = None
    
for line in last_name_file:    
    lastnames[line.rstrip("\n").lower()] = None

for line in med_dictionary_file:
    med_dictionary[line.rstrip("\n").lower()] = None
  

def test_pattern(text, patterns=[]):
    """Given source text and a list of patterns, look for
    matches for each patternwithin the text and print
    them to stdout.
    """
    
    # Show the character positions and input text
    for pattern in patterns:
        if re.search(pattern,text):
            print
            print ''.join(str(i/10 or ' ') for i in range(len(text)))
            print ''.join(str(i%10) for i in range(len(text)))
            print text        
            print
            print 'Matching %s' % pattern
            for match in re.finditer(pattern,text):
                s = match.start()
                e = match.end()
                print '  %2d  :  %2d = "%s"' % \
                      (s, e-1, text[s:e])        
    return
                  
def check_pattern(word):
    print word
    print "check pattern ran"
    found = False    
    final_allowed = "allowed"
    patterns = [re.compile(p) for p in['[0-9]{1,2}[/\.-][0-9]{1,2}[/\.-][0-9]{2,4}',
                                       '^\d{1,2}[\W]\d{2,4}$']]    
    for pattern in patterns:        
        if pattern.search(word):
            found = True

            print "pattern ran"
            return True, "not allowed"
    
    if not found:
        print "not found"
        words = remove_punctuation(word)
        for item in words:
            print "item is", item
            status , allowed = check_word(item)
            print "status",status, "allowed",allowed
            if status == False:
                print "false ran"
                return status, allowed
            if allowed == 'not allowed':
                final_allowed = 'not allowed'
        return status, final_allowed            
    
    
def remove_punctuation(word):
    print "remove ran"    
    words = []
    punctuation = re.compile(r'\w+')
    matches =  punctuation.finditer(word)
    for match in matches:
        s = match.start()
        e = match.end()
        words.append(word[s:e])
    print "words is", words
    return words
                     
def check_word(word):
    word = word.lower()
    months = ['january','february','march','april','may','june',
              'july','august','september','october','november','december']
    single = re.compile(r'^\W*$')
    punctuaction_present = re.compile(r'[\w]+\W[\w]')
    if punctuaction_present.search(word):
        status , allowed = check_pattern(word)
        return status, allowed
    else:
        print "not puncht"
        print word
        single_item = True if single.search(word) else False
        allowed = word in dictionary or word in med_dictionary or word.isdigit()\
                  or single_item
        print allowed
        not_allowed = word in firstnames or word in lastnames or word in months
        print not_allowed

        if allowed and not_allowed:
            print "indeterm"
            return True, "indeterminate" 
        if not_allowed:
            print "not allowed ran"
            return True, "not allowed"
        if allowed:
            print  "allowed ran"
            return True, "allowed"

        if not allowed and not not_allowed:
            print "found neither"
            return False, "indeterminate"
   

def main():    

    words = ['..hello']
    
    for word in words:       
        print word, check_word(word)
    
        

    

if __name__ == '__main__':
    main()
    
    
