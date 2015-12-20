import pickle
def dump_object(my_object,filename):
    myfile = open(filename,'w')
    pickle.dump(my_object, myfile)
    myfile.close()


def main():

    myfile = open('wordlist.txt','r')
    dictionary = dict()
    firstnames = dict()
    lastnames = dict()
    medlist = dict()

    file_list = list((["completedict.txt","englishwordslist",dictionary], #pickle files with word list
                 ["firstnames.txt","firstnameslist",firstnames],
                 ["lastnames.txt","lastnameslist",lastnames],
                    ["wordlist.txt","medicalwordlist",medlist]))

    for pairs in file_list:
        myfile = open(pairs[0],'r')
        for line in myfile:
            word = line.rstrip("\n").lower()
            pairs[2][word] = None
        myfile.close()
        dump_object(pairs[2],pairs[1])

    for pairs in file_list:
        myfile = open(pairs[1],'r')
        a = pickle.load(myfile)
        print type(a), len(a), "Hello" in a, pairs[1]

if __name__ == '__main__':
    main()
    

    
