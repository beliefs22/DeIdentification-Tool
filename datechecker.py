import re
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

    pattern = ['[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}']

    test_pattern(date,pattern)

    pattern = ['January','February','March','April','May',
               'June','July','August','September','October',
               'December']
    test_pattern(date,pattern)
    

def main():
    
    pattern = ['[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}']
    text = '02/22/2015'

    test_pattern(text,pattern)

    pattern = ['[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}']
    text = '12/12/2015'

    test_pattern(text,pattern)

    pattern = ['[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}']
    text = '15/124/1'

    test_pattern(text,pattern)

    

    

if __name__ == '__main__':
    main()
    
    
