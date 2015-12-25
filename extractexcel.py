import patternchecker as ptchk
import re
import os
import pickle


class Excel:
    """Object representing an excel File containing PHI.

    Args:
        excelfile (file): file pointing to excelfile to be cleaned
    
    """

    def __init__(self,excelfile):
        self.excelfile = excelfile
        self.raw_headers = excelfile.readline().rstrip("\n").split(",")
        self.headers = {} #headers should be first line of csv

        for index, header in enumerate(self.raw_headers):
            self.headers[index] = header #keep headers in order

        self.subjects = [] #one subject is one line of file other than first
        for index, subjectdata in enumerate(excelfile):
            raw_data = subjectdata.rstrip("\n")
            self.subjects.append(Subject(self.headers,raw_data))
    def deidentify(self,master_not_allowed, master_indeterminate):
        """Runs Deidentification process.

        Args:
            master_not_allowed (list): list of identified PHI
            master_indeterminate (list): list of indeterminate words
        
        """
        for subject in self.subjects:
            subject.final_clean(master_not_allowed,master_indeterminate)
        

    def get_headers(self):
        """Return list of strings representing headers for excel file.

        Returns:
            dict: dict where v = header and k = position in file
        
        """
        return self.headers

    def get_subjects(self):
        """Return list of Subject objects created from excel file.

        Returns:
            list: list containing subjects objects created from file

        """
        return self.subjects

    def get_num_of_subjects(self):
        """Return number of subjects in file as int.

        Returns:
            int: number of subjects created from file
        
        """
        return len(self.subjects)

    def one_pass(self, size=None):
        """Part of Deidentification process.

        Args:
            size (int): represents the number of subjects to run the cleaning

        Returns:
            list: 3 list containing allowed, not allowed and interminate words
                   
        """
        master_allowed = list() #tracks permited words
        master_not_allowed = list()#tracks prohibited words
        master_indeterminate = list()# tracks ambigious words
        if size  == None:
            size = len(self.subjects)
        available_dictionaries = ptchk.Dictionary()
        dictionaries = available_dictionaries.export_dicts()
        for i in range(size):
            print "cleaning subject %d/%d " % (i + 1,size)
            # Finds permited, prohibited and ambiguous words for a subject
            allowed,not_allowed,indeterminate = \
                                              self.subjects[i].clean(
                                                  dictionaries)
            # Add words for one subject to master list
            for word in allowed:
                if word not in master_allowed:
                    master_allowed.append(word)
            for word in not_allowed:
                if word not in master_not_allowed:
                    master_not_allowed.append(word)
            for word in indeterminate:
                if word not in master_indeterminate:
                    master_indeterminate.append(word)
        return master_allowed, master_not_allowed, master_indeterminate
        
    def create_user_dictionary(self, user_allowed,user_not_allowed):
        """Creates a dictionary of words that could be ambigious that the user
        has chosen to let through. Persist throughout multiple sessions.

        Args:
            user_allowed (list): words user wants to let through
            user_not_allwed (list): words use wants to fail
        
        """
        user_allowed_dict = [] #list of user permitted words
        user_not_allowed_dict = [] #list of user prohibited words

        if os.path.exists('userallowedlist'): #opens previously made list
            wordfile = open('userallowedlist','r')
            try:
                user_allowed_dict = pickle.load(wordfile)
            except EOFError: #catches empty list from previous session
                user_allowed_dict = []
            wordfile.close()
        if os.path.exists('usernotallowedlist'):
            wordfile2 = open('usernotallowedlist','r')
            try:
                user_not_allowed_dict = pickle.load(wordfile2)
            except EOFError:
                user_not_allowed_dict = []
            wordfile2.close()

        for word in user_allowed: 
            if word not in user_allowed_dict:
                user_allowed_dict.append(word.lower())
        for word in user_not_allowed:
            if word not in user_not_allowed_dict:
                user_not_allowed_dict.append(word.lower())

        myfile1 = open('userallowedlist','w') 
        pickle.dump(user_allowed_dict,myfile1) #saves new changes
        myfile1.close()
        myfile2 = open('usernotallowedlist','w')
        pickle.dump(user_not_allowed_dict,myfile2)
        myfile2.close()

    def make_csv(self):
        """Creates CSV of deidentified data."""
        myfile = open('finalcleandata2.csv','w')
        myfile.write(",".join(self.raw_headers) + "\n")
        for subject in self.subjects:
            myfile.write(subject.get_clean_data() + "\n")
        myfile.close()    
            

class Subject:
    """Object Representing a subject or one line from an excel file.
    
    Args:
        headers (dict): dictionary containing header information
        rawdata (str): data to clean
    
    """

    def __init__(self,headers,rawdata):
        self.headers = headers
        self.raw_data = rawdata
        self.clean_data = ""
        self.date_time = None
        self.word_time = None
        self.final_clean_time = None

    def get_raw_data(self):
        """Return str representing unaltered data.

        Returns:
            str: string representing unaltered data

        """
        return self.raw_data

    def get_clean_data(self):
        """Return str representing clean data.

        Returns:
            str: string represeting de-identified data
        """
        return self.clean_data
        
    def clean(self, dictionaries):
        """Runs process to remove dates and find words that are allowed,
        not allowed(names), and ambiguous words.

        Returns:
            list: 3 list containg allowed, not alowed and unclear words
        
        """
        temp = self.raw_data.replace(","," ") #remove commas temporariarly
        dates,non_dates = ptchk.check_for_dates(temp)
        allowed,not_allowed,indeterminate =\
                                          ptchk.check_for_words(non_dates,
                                                                dictionaries)
        not_allowed = not_allowed + dates
        print "Took" , self.date_time, "seconds to remove dates"
        print "Took", self.word_time, "seconds to remove match words"
        return allowed, not_allowed, indeterminate

    def final_clean(self,master_not_allowed,master_indeterminate):
        """Replaces words in Subject data that are allowed or unclear.

        Args:
            master_not_allowed (list): words to remove from data
            master_indeterminate (list): words to mark as ambigious

        """
        self.clean_data = self.raw_data #initialize clean data to raw data

        def make_re(word):
            #Helper function to make words into re objects 
            return r'\b(%s)\b' % word 

        not_allowed_patterns = [re.compile(make_re(word))\
                                for word in master_not_allowed]
        indeterminate_patterns = [re.compile(make_re(word)) \
                                  for word in master_indeterminate]

        for pattern in not_allowed_patterns:#removes prohibited words
            temp = self.clean_data[:] 
            temp = pattern.sub("[REDACTED]",temp[:])
            self.clean_data = temp
        for index,pattern in enumerate(indeterminate_patterns):#mark ambg words
            temp = self.clean_data[:]
            temp = pattern.sub(master_indeterminate[index] \
                               + "[INDETER]",temp[:])
            self.clean_data = temp
def main():

    excelfile = open("a tst csv.csv",'r')

    ExcelFile = Excel(excelfile)
    print ExcelFile.get_headers()    
    ExcelFile.clean_data()    
    ExcelFile.make_csv()

if __name__ == "__main__":
    main()
        
