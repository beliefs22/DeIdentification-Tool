import patternchecker as ptchk
import re
import os
import pickle

class Excel:
    """Object representing an excel File containing PHI

    Attr:
        Headers (list): contains heders(1st line) of excel file
        Subjects (list): contains Subject objects created from excel file
        """

    def __init__(self,excelfile):
        """
        Args:
            excelfile (file): file object pointing to csv to be deidentified
        """     

        self.excelfile = excelfile
        self.raw_headers = excelfile.readline().rstrip("\n").split(",")
        self.headers = {} #headers should be first line of csv

        for index, header in enumerate(self.raw_headers):
            self.headers[index] = header #keep headers in order

        self.subjects = [] #one subject is one line of file other than first

        for index, subjectdata in enumerate(excelfile):
            raw_data = subjectdata.rstrip("\n")
            print "Creating Subject[%d] using: " % index
            print raw_data
            self.subjects.append(Subject(self.headers,raw_data))

    def deidentify(self,master_not_allowed, master_indeterminate):
        """Runs Deidentification process
        Args:
            master_not_allowed (list): list of identified PHI
            master_indeterminate (list): list of indeterminate words
        """
        for subject in self.subjects:
            subject.final_clean(master_not_allowed,master_indeterminate)
        

    def get_headers(self):
        """Return list of strings representing headers for excel file"""
        return self.headers

    def get_subjects(self):
        """Return list of Subject objects created from excel file"""
        return self.subjects

    def get_num_of_subjects(self):
        """Return number of subjects in file as int"""
        return len(self.subjects)

    def one_pass(self, size=None):
        """Part of Deidentification process
        Args:
            size (int): represents the number of subjects to run the cleaning
            prosses on. If no size is given , will run on all subjects possible
        """
        master_allowed = list() #tracks permited words
        master_not_allowed = list()#tracks prohibited words
        master_indeterminate = list()# tracks ambigious words
        if size  == None:
            size = len(self.subjects)
        for i in range(size):
            print "cleaning subject %d/%d " % (i,size)
            # Finds permited, prohibited and ambiguous words for a subject
            allowed,not_allowed,indeterminate = self.subjects[i].clean()
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
        has chosen to let through. Persist throughout multiple sessions
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
        """Creates CSV of deidentified data"""
        myfile = open('finalcleandata2.csv','w')
        myfile.write(",".join(self.raw_headers) + "\n")
        for subject in self.subjects:
            myfile.write(subject.get_clean_data() + "\n")
        myfile.close()

class Subject:
    """Object Representing a subject or one line from an excel file
    Attributes:
        raw_data (str): string representing unaltered data
        clean_data (str): string represening deindentified data
    """

    def __init__(self,headers,rawdata):
        """
        Args
            headers (dict): dictionary containing header information
            rawdata (str): str representing data from excel file use to create
            subejct object
        """
        self.headers = headers
        self.raw_data = rawdata
        self.clean_data = ""

    def get_raw_data(self):
        """Return str representing unaltered data"""
        return self.raw_data

    def get_clean_data(self):
        """Return str representing clean data"""
        return self.clean_data
        
    def clean(self):
        """Runs process to remove dates and find words that are allowed,
        not allowed(names), and ambiguous words
        """
        dates,non_dates = ptchk.check_for_dates(self.raw_data)
        allowed,not_allowed,indeterminate = ptchk.check_for_words(non_dates)
        not_allowed = not_allowed + dates
        return allowed, not_allowed, indeterminate

    def final_clean(self,master_not_allowed,master_indeterminate):
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

    excelfile = open("September 2015 Samples De-Identified2.csv",'r')

    ExcelFile = Excel(excelfile)
    print ExcelFile.get_headers()
    
    ExcelFile.clean_data()    
    ExcelFile.make_csv()

if __name__ == "__main__":
    main()
        

        
        
        
