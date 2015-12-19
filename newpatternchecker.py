import re
import os
import pickle

dictionary = dict()
firstnames = dict()
lastnames = dict()

file_list = list((["englishwordslist",dictionary], #pickle files with word list
                 ["firstnameslist",firstnames],
                 ["lastnameslist",lastnames]))

for pair in file_list: # create list to use in program to check words
    print pair[0], pair[1]
    myfile = open(pair[0],'r')
    pair[1] = pickle.load(myfile)
    myfile.close()



def check_patterns(text):
    date_pattern = re.compile(
        '[0-9]{1,2}[\W][0-9]{1,2}[\W][0-9]{2,4}|^\d{1,2}[\W]\d{2,4}$') #dates

    punct_pattern = re.compile(r'[^\w]+') #matches punctuation

    date_locations = date_pattern.finditer(text)
    matched_dates = date_pattern.findall(text)
    print text, "before date removed"
    non_date_words = " ".join(date_pattern.split(text)) # remove dates
    print non_date_words, "after date removed"
    non_date_words = " ".join(punct_pattern.split(non_date_words)) # remove punct
    print non_date_words, "after punct removed"
    return matched_dates, non_date_words

def main():

    test_string = "Hello - my - name is Seth. Today is 12/19/15 , 12/15"

    print check_patterns(test_string)

if __name__ == '__main__':
    main()
    
    
