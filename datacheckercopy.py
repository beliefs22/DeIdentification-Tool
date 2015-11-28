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
    found_pattern = False
    punctuation_end =  re.compile(r'^\w+\W+$')
    punctuation_begin = re.compile(r'^\W+\w+$')
    enclosed = re.compile(r'^\W{1}[\S]+\W{1}$')
    
    patterns = [re.compile(p) for p in['[0-9]{1,2}[/\.-][0-9]{1,2}[/\.-][0-9]{2,4}',
                                       '^\d+\.\d+$','^\d{1,2}[\W]\d{2,4}$']]
    middle = re.compile('^\w+[/:\-;()[\]{\}]\w+$')    
    
    if  punctuation_end.search(word):
        found_pattern = True
        print "punc_end rant"
        punct = re.compile(r'\W+$')                           
        match = punct.search(word)        
        word = word[:match.start()]

    if punctuation_begin.search(word):
        found_pattern = True
        print "punt_bein ran"
        punct = re.compile(r'^\W+')
        match = punct.search(word)
        word = word[match.end():]

    if enclosed.search(word):
        found_pattern = True
        print "enclosed ran"        
        word = word[1:len(word)-1]        
 
    if middle.search(word):
        found_pattern = True
        print "middle ran" 
        options =['/',':',':','-',';','(',')','[',']','{','}']
        for option in options:
            if option in word:
                temp = word.split(option)                
                for item in temp:                    
                    if not check_word(item):
                        found = False
        return found, "not allowed"
    
    for pattern in patterns:
        found_pattern = True
        if pattern.search(word):
            print "pattern ran"
            return True, "not allowed"
    if found_pattern:
        return True, "not allowed"
    else:
        ret
    
def remove_punctuation(word):
    print "remove ran"
    found = True
    words = []
    punctuation = re.compile(r'\w+')
    matches =  punctuation.finditer(word)
    for match in matches:
        s = match.start()
        e = match.end()
        words.append(word[s:e])
    for item in words:
        if not check_word(item):
            found = False
    if found:
        return found, "allowed"
    else:
        return found, "not allowed"
    
                     
def check_word(word):
    word = word.lower()
    punctuaction_present = re.compile(r'\W')
    if punctuaction_present.search(word):
        if check_pattern(word):
            return True, "not allowed"
        else:
            print "remove word", word
            return remove_punctuation(word)
    else:
        print "not puncht"
        found = word in dictionary or word in med_dictionary or not word in firstnames \
               or not word in lastnames or word.isdigit()
        if found:
            return True, "allowed"
        else:
            return False, "not allowed"
    

def main():    

    words = ['1.2.2015','jessica','Jeessica.',"days),cefazolin(1", '10/20/15','n/a','4.5',
             'September','4/15','nk/efas','Quentis','Sally','house(1',
             'vancomycin','left-sided','hello...::::','hello.',"..hello","(hh)",
             '(hello)','(2.2)',"Quentin"]

    for word in words:
        found, status = check_word(word)
        print word, found, status

    

if __name__ == '__main__':
    main()
    
    
