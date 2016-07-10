import re
from datetime import datetime

def isDate(date):
    """Finds dates of the format ##/##/####"""
    pattern = re.compile(r'.([^\w]).') #find punct patter that splits dates
    match = pattern.search(date)
    found_punct_pattern = re.compile(match.group(1))
    
    date_pieces = found_punct_pattern.split(date) #split date string at backslash
    print date_pieces,  'pieces are'
    pieces = [int(x) for x in date_pieces]
    if len(pieces) == 3: #check if this is actually a date
        print "one ran"
        if pieces[0] not in range(1, 13) or pieces[1] not in range(1, 32) or \
           (len(str(pieces[2])) == 3) or \
           (len(str(pieces[2])) == 2 and pieces[2] not in range(0,100) or \
           (len(str(pieces[2])) == 4 and \
            pieces[2] not in range(1913, datetime.now().year + 1))):
            return False
    if len((pieces)) == 2:
        if int(pieces[0]) not in range(1,13) or int(pieces[1]) > 2016:
            return False
    try:
        return True
    except len(pieces) != 2 or len(pieces) !=3:
        return False

def main():

    dates = ['2/20/201', '31/23','12/35/2015','6/12/1353','5/5/2016','5/15',
             '3/23/15','03/2015','-3/-15/-2016']
    for date in dates:
        print "date is %s it is" % date, isDate(date)
        
if __name__ =='__main__':
    main()
