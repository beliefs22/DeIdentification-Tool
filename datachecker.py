import re

dictionary_file = open("completedict.txt","r")
first_name_file = open("firstnames.txt",'r')
last_name_file = open("lastnames.txt",'r')
dictionary ={}
firstnames = {}
lastnames = {}
for line in dictionary_file:    
    dictionary[line.rstrip("\n").lower()] = None

for line in first_name_file:    
    firstnames[line.rstrip("\n").lower()] = None
for line in last_name_file:    
    lastnames[line.rstrip("\n").lower()] = None
  

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
                  
def check_date(date):

    pattern = ['[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}','[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4}',
               'January','February','March','April','May','June',
               'July','August','September','October','December','^\d+\.\d+$']

    test_pattern(date,pattern)

def check_word(word):
    punctuation = ['.',',',':','"',]
    patterns = ['[0-9]{1,2}[/\.-][0-9]{1,2}[/\.-][0-9]{2,4}','january',
                'february','march','april','may','june','july','august',
                'september','october','december','^\d+\.\d+$']
    other = '^\w+[/:-]\w+$'
    
    word = word.lower()
    for mark in punctuation:
        if word.endswith(mark):
            word = word[:len(word)-1]
            break
    if re.search(other,word):
        found = True
        options =['/',':',':','-']
        for option in options:
            if option in word:
                temp = word.split(option)                 
                for item in temp:                    
                    if not check_word(item):
                        found = False
        return found
            
        
   
    for pattern in patterns:
        if re.search(pattern,word):
            return True
        
    return word in dictionary or word in firstnames \
           or word in lastnames or word.isdigit()
    

def main():    

    words = ['1.2.2015','jessica','Jessica', '10/20/15','n/a','4.5',
             'September 2015','4/15','nk/efas','Quentis','Sally']

    for word in words:
        print word, check_word(word)

    

if __name__ == '__main__':
    main()
    
    
