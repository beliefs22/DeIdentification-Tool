import pickle
def dump_object(my_object,filename):
    myfile = open(filename,'w')
    pickle.dump(my_object, myfile)
    myfile.close()


def main():

    myfile = open('/home/beliefs22/python/primes.txt','r')
    prime_list = dict()
    for pos, line in enumerate(myfile):
        prime_list[int(line.rstrip("\n"))] = pos
    myfile.close()

    prime_list = tuple(sorted(tuple(prime_list)))

    dump_object(prime_list,'/home/beliefs22/python/primetuples')
    myfile = open('/home/beliefs22/python/primetuples', 'r')
    test = pickle.load(myfile)
    print len(test), type(test), test[17], 29 in test, test

if __name__ == '__main__':
    main()
    

    
