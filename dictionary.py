import pickle
import os
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
                if dictionary != self.user_all_dict:
                    self.allowed_words[word] = 'Found'
                else:
                    self.allowed_words[word] = 'User'
        for dictionary in all_prohibited_dicts:
            for word in dictionary.keys():
                if dictionary != self.user_not_all_dict:
                    self.prohibited_words[word] = 'Found'
                else:
                    self.prohibited_words[word] = 'User'

    def export_dicts(self):
        """Returns list of dictionaries to use in de-identification process

        Returns:
            list: list containing varioes dictionaries that will be used in
                check for words function
        """
        return self.allowed_words, self.prohibited_words
