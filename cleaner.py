class Cleaner:

    def __init__(self, allowed_words,prohibited_words):

        self.allowed = allowed_words
        self.prohibited = prohibited_words


    def makeRePattern(self,pattern, words):
        """Creates a re-object by substituting the given word into
        the given pattern.

        i.e pattern = '\A(%s)( )|( )(%s)( )|( )(%s)\Z'
            word = 'hello'
            results in pattern '\A(hello)( )|( )(hello)( )|( )(hello)\Z'
        """
        #create list of re objects in the given pattern for each word
        re_patterns = [
            re.compile(pattern % tuple([word] * pattern.count("%s")))
            for word in words
        ]

    def isDate(self,text):
        """Determines if given string is an actual date rather than looks
        like a date
        """
        #find character that separaters dates usually / or - or .
        separator = re.compile(r'.([^\w]).')
        #find the separater in the string
        match = pattern.search(text)
        #Find the actual separater rather than something like a negative sign
        #Use this to split the date into it components
        found_separator_pattern = re.compile(match.group(1))
        date_pieces = found_separator_pattern.split(text)
        #convert strings to numbers to check if these are actually dates
        date_pieces = [int(piece) for piece in date_pieces]
        #Determine if date is in ##/#### or ##/##/#### format
        # Dates in ##/##/#### format
        if len(pieces) == 3:
            month = int(pieces[0])
            day = int(pieces[1])
            year = int(pieces[2])
            year_len = len(str(year))
            if day not in range(1,13) or month not in range(1,32) or \
               (year_len != 2 or year_len != 4) or \
               (year_len == 2 and year_len not in range(0,100)) or \
               (year_len == 4 and year_len not in range(
                   1913, datetime.now().year + 1)):
                return False
        if len(pieces) == 2:
            if month not in range(1,13) or year not in range(0,1
        
    def check_for_date(self,text):
        """checks the given string for dates"""

        # regular expression to use to match dates
        date_pattern = re.compile(
            '[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}|\d{1,2}[\W]\d{2,4}')

        # regular expression to match punctuation
        punct_pattern = re.compile(r'[^\w]+')

        #find all dates that match date_pattern in text
        matched_dates = date_pattern.findall(text)
        
            
