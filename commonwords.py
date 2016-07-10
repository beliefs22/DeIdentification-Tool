import pickle
import os
import re
class Dictionary:
    """Object representing available dictionaries to used in search."""

    def __init__(self):
        self.allowed_words = {}
        self.prohibited_words = {}


        # pickle filess with saved word lists
        file_list = [["Data/Dictionaries/englishwordslist"],
                     ["Data/Dictionaries/firstnameslist"],
                     ["Data/Dictionaries/lastnameslist"],
                     ["Data/Dictionaries/medicalwordlist"]
                     ]
        # create list to use in program to check words
        for index, fileinfo in enumerate(file_list):  
            with open(fileinfo[0], 'r') as myfile:
                file_list[index].append(pickle.load(myfile))

        english_dictionary = file_list[0][1]
        print len(english_dictionary)
        firstnames = file_list[1][1]
        lastnames = file_list[2][1]
        medicaldict = file_list[3][1]
        # User defined dictionary of allowed words
        self.user_all_dict = dict()
        # User defined dictionary of prohibited words
        self.user_not_all_dict = dict()
        months = {'january':None, 'february':None, 'march':None, 'april':None,
                  'may':None, 'june':None, 'july':None, 'august':None,
                  'september':None, 'october':None, 'november':None,
                  'december':None
                  }

        # Open saved user file if exist
        if os.path.exists('Data/UserDictionaries/userallowedlist'):
            saved_list = open('Data/UserDictionaries/userallowedlist', 'r')
            try:
                user_list = pickle.load(saved_list)
                self.user_all_dict = dict(zip(user_list,
                                          [None]*len(user_list)))
            except EOFError:  # if list is empty skip
                pass
            saved_list.close()
        # Open save user file if exist
        if os.path.exists('Data/UserDictionaries/usernotallowedlist'):  
            saved_list = open('Data/UserDictionaries/usernotallowedlist', 'r')
            try:
                user_list = pickle.load(saved_list)
                self.user_not_all_dict = dict(zip(user_list,
                                                  [None]*len(user_list)))
            except EOFError:  # if list is empty skip
                pass
            saved_list.close()        

        all_allowed_dicts = [english_dictionary, medicaldict,
                             self.user_all_dict]
        all_prohibited_dicts = [firstnames, lastnames, months,
                                self.user_not_all_dict]
        for dictionary in all_allowed_dicts:
            for word in dictionary.keys():
                self.allowed_words[word] = None
        for dictionary in all_prohibited_dicts:
            for word in dictionary.keys():
                self.prohibited_words[word] = None

    def export_dicts(self):
        """Returns list of dictionaries to use in de-identification process

        Returns:
            list: list containing varioes dictionaries that will be used in
                check for words function
        """
        return self.allowed_words, self.prohibited_words

def remove_words(text, Dictionary):
    """Returns a text with prohibited words removed, also creates user defined
    dictionary? """
    
    self.myDict = Dictionary
    allowed_words, prohibited_words = self.myDict.export_dicts()
    #remove punct from text
    punct_pattern = re.compile(r'[^\w]+')
    new_text = punct_pattern.split(text[:]
def main():

    mydict = Dictionary()

    a,b = mydict.export_dicts()
    print len(a), len(b)

if __name__ =="__main__":
    main()

    
