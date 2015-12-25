import re

def make_re(pattern,words):
    """Makes re-objects in the given patter from given words.

    Args:
        pattern (str): string representation of what you would like the pattern
            to look like. I.E. '\A(%s)( )|( )(%s)( )|( )(%s)\Z'
        words (list): list of words to covert to re objects

    Returns:
        list: list containin converted re objects

    """
    pattern_strings = [pattern % tuple([word] * pattern.count("%s"))\
                       for word in words]

    patterns = [re.compile(p) for p in pattern_strings]
    return patterns

def main():

    pattern = '\A(%s)( )|( )(%s)( )|( )(%s)\Z'

    words = ['2/2015/2015','hello','monday','BlazeEKre','EJREIF..dfjeifea slk']

    results = make_re(pattern,words)
    for pattern in results:
        print pattern.pattern

    words_string = " ".join(words) + " added word goes here"
    i = 0
    for pat in results:
        print "word string at start", words_string
        print "pattern is",pat.pattern
        a = pat.split(words_string[:], maxsplit=1)
        print "non matched items", a[len(a)-1]
        words_string = a[len(a) -1]
        print "word string at end", words_string, len(words_string)
        print
        print
        i = i + 1

if __name__ =='__main__':
    main()
