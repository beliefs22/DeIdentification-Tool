import re
from datetime import datetime

def makeRePattern(pattern, words):
    """Creates a re-object by substituting the given word into
    the given pattern.

    i.e pattern = '\A(%s)( )|( )(%s)( )|( )(%s)\Z'
        word = 'hello'
        results in pattern '\A(hello)( )|( )(hello)( )|( )(hello)\Z'
    """
    #create list of re objects in the given pattern for each word
    re_patterns = [
        re.compile(pattern % tuple([word] * pattern.count("%s")),re.X)
        for word in words
    ]
    return re_patterns

def isDate(text):
    """Determines if given string is an actual date rather than looks
    like a date
    """
    #find character that separaters dates usually / or - or .
    separator = re.compile(r'.([^\w]).')
    #find the separater in the string
    match = separator.search(text)
    #Find the actual separater rather than something like a negative sign
    #Use this to split the date into it components
    found_separator_pattern = re.compile(r'[%s]' % match.group(1))
    date_pieces = found_separator_pattern.split(text)
    #convert strings to numbers to check if these are actually dates
    date_pieces = [int(piece) for piece in date_pieces]
    #Determine if date is in ##/#### or ##/##/#### format
    # Dates in ##/##/#### format
    if len(date_pieces) not in [2,3]:
        return False
    if len(date_pieces) == 3:
        month = int(date_pieces[0])
        day = int(date_pieces[1])
        year = int(date_pieces[2])
        year_len = len(str(year))
        # negative numbers aren't dates
        if month < 0 or day < 0 or year < 0:
            return False
        # ex 233/13/2015
        if len(str(month)) not in [1,2]:
            return False
        # ex 12/222/2015
        if len(str(day)) not in [1,2]:
            return False
        # ex 12/22/20155
        if year_len not in [1,2,4]:
            return False
        # ex 12/45/2015
        if day not in range(1,32):
            return False
        # ex 14/24/2015
        if month not in range(1,13):
            return False
        # ex 12/24/0 
        if (year_len == 1 and year not in range(1,9)):
            return False
        # ex 12/20/9
        if (year_len == 2 and year not in range(0,100)):
            return False
        # ex 12/20
        if (year_len == 4 and year not in range(
            1913, datetime.now().year + 1)):
            return False

        return True
        
    if len(date_pieces) == 2:
        month = date_pieces[0]
        day_or_year = date_pieces[1]
        day_or_year_len = len(str(day_or_year))
        # neagative numbers aren't dates
        if month < 0 or day_or_year < 0:
            return False
        # ex 112/23/2015
        if len(str(month)) not in [1,2]:
            return False
        if month not in range(1,13):
            return False
        # ex 12/23/20156
        if len(str(day_or_year)) not in [1,2,4]:
            return False
        # ex 12/35/2015
        if day_or_year_len in [1,2] and \
           day_or_year not in range(1,32):
            return False
        # ex 12/25/2858
        if day_or_year_len == 4 and day_or_year not in range(
            1913, datetime.now().year + 1):
            return False
        return True
                
    
def remove_dates(text):
    """Returns a string of text with dates redacted"""
    text_without_dates = text[:]    
    #template to make regular expressions
    #finds words at begining, end , and anywhere in sentence
    pattern_template = \
        '\A(%s)(\W)*[\s]|[\s](%s)[\s]|[\s](%s)(\W)*\Z|\A(%s)\Z'    

    # regular expression to use to match dates
    date_patterns = makeRePattern(pattern_template,
            ['[-]*[0-9]{1,2}[\W][-]*[0-9]{1,2}[\W][-]*[0-9]{2,4}',
             '[-]*\d{1,2}[\W][-]*\d{2,4}'])

    # regular expression to match punctuation
    punct_pattern = re.compile(r'[^\w]+')

    #find all dates in  the text fir each pattern
    matched_dates = []
    for date_pattern in date_patterns:
        found_dates = date_pattern.finditer(text)
        for date in found_dates:
            matched_dates.append(date.group().strip())

    for date in matched_dates[:]:
        #pass words that just look like dates
        if not isDate(date):
            matched_dates.remove(date)
    #create patterns from found dates that were actual dates
    matched_date_patterns = makeRePattern(pattern_template, matched_dates)
    #loop to remove each found date from the text
    for date_pattern in matched_date_patterns:
        text_without_dates = date_pattern.sub("[REDACTED] ", text_without_dates)
    return text_without_dates

def main():


    dates = ['2/20/201', '31/23','12/35/2015','6 12 2015','5/5/2016','5/15',
             '3/23/15','03/2015','-3/-15/-2016', '5/23/23/3235/12', '5.2015']
##    for date in dates:
##        print isDate(date), date

    text = "Hello world this is 2/2015 and 2/26 but not 2/5/2353 and vancomycin \
is here to make John Lilly angry"

    print text
    print remove_dates(text)

if __name__ == "__main__":
    main()
                
    
        
