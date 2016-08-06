import csv
import cleaner
import dictionary

def modify(csvsource, modifydest,modifyfunct):
    """Modifies a csv and saves it at a given destination"""
    print "Modifying %s. Saving at %s" % (csvsource, modifydest)

    with open(csvsource, 'rb') as csvfile, open(modifydest,'wb') as destfile:
        sourcereader = csv.reader(csvfile)
        destwriter = csv.writer(destfile)

        #get headers to copy these won't be modified
        headers = sourcereader.next()
        #collect data that needs to be modified
        data_to_modify = list(sourcereader)
        
        #apply modifying function to each cell in each row of the file
        modified_data = [
                        map(modifyfunct,row)
                        for row in data_to_modify
                        ]

        
        #copy over headers
        destwriter.writerow(headers)
        #copy modified data
        for row in modified_data:
            destwriter.writerow(row)
        print "COMPLETE"

def main():
    mydict = dictionary.Dictionary()
    modifyfunct = lambda text: cleaner.clean_text(text,mydict)

    csvsource = 'csvs/A_test_csv.csv'
    modifydest = 'csvs/testing_with_fun.csv'

    modify(csvsource,modifydest,modifyfunct)

if __name__ =="__main__":
    main()



        
