import pickle

firstnames = {}
lastnames = {}

firstnamefile = open('firstnames.txt','rb')
lastnamefile = open('lastnames.txt','rb')

with open('firstnames.txt','rb') as fn, open('lastnames.txt','rb') as ln,\
     open('englishwords.txt','rb') as ew:
    print "Starting"
    firstnames = {
                line.split(",")[0].lower() : "Auto"
                for line in list(fn)
                }
    with open('Dictionaries/firstnameslist','wb') as firstnamedump:
        pickle.dump(firstnames, firstnamedump)

    lastnames = {
                line.split(",")[0].lower() : "Auto"
                for line in list(ln)
                }
    with open('Dictionaries/lastnameslist', 'wb') as lastnamedump:
        pickle.dump(lastnames, lastnamedump)


    englishwords = {
                    line.strip("\n") : "Auto"
                    for line in list(ew)
                    }
    with open('Dictionaries/englishwordslist', 'wb') as englishwordsdump:
        pickle.dump(englishwords, englishwordsdump)
            
    print "Done"


