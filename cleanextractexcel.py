from newpatternchecker import *
import re
import getchall
import os
import pickle

class Excel:

    def __init__(self,excelfile):

        self.excelfile = excelfile
        self.raw_headers = excelfile.readline().rstrip("\n").split(",")
        self.headers = {}

        for index, header in enumerate(self.raw_headers):
            self.headers[index] = header

        self.subjects = []

        for subjectdata in excelfile:
            raw_data = subjectdata.rstrip("\n")
            self.subjects.append(Subject(self.headers,raw_data))

    def deidentify(self,master_not_allowed, master_indeterminate):
        for subject in self.subjects:
            subject.final_clean(master_not_allowed,master_indeterminate)
        

    def get_headers(self):
        return self.headers

    def get_subjects(self):
        return self.subjects

    def get_num_of_subjects(self):
        return len(self.subjects)

    def one_pass(self, size=None):
        master_allowed = list()
        master_not_allowed = list()
        master_indeterminate = list()
        if size  == None:
            size = len(self.subjects)
        print "running", size, "times"
        for i in range(size):
            print "cleaning subject ", i
            #print "subject type is", subjects[i], i
            allowed,not_allowed,indeterminate = self.subjects[i].clean()
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
        user_allowed_dict = []
        user_not_allowed_dict = []

        if os.path.exists('userallowedlist'):
            wordfile = open('userallowedlist','r')
            try:
                user_allowed_dict = pickle.load(wordfile)
            except EOFError:
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
        pickle.dump(user_allowed_dict,myfile1)
        myfile1.close()
        myfile2 = open('usernotallowedlist','w')
        pickle.dump(user_not_allowed_dict,myfile2)
        myfile2.close()

    def make_csv(self):
        myfile = open('finalcleandata2.csv','w')
        myfile.write(",".join(self.raw_headers) + "\n")
        for subject in self.subjects:
            myfile.write(subject.get_clean_data() + "\n")
        myfile.close()

class Subject:

    def __init__(self,headers,rawdata):
        self.headers = headers
        self.raw_data = rawdata
        self.clean_data = ""

    def get_raw_data(self):
        return self.raw_data

    def get_clean_data(self):
        return self.clean_data
    def clean(self):
        
        dates,non_dates = check_for_dates(self.raw_data)
        allowed,not_allowed,indeterminate = check_for_words(non_dates)
        not_allowed = not_allowed + dates
        return allowed, not_allowed, indeterminate

    def final_clean(self,master_not_allowed,master_indeterminate):
        self.clean_data = self.raw_data # initially they are equal

        def make_re(word):
            return r'\b(%s)\b' % word 

        not_allowed_patterns = [re.compile(make_re(word))\
                                for word in master_not_allowed]
        indeterminate_patterns = [re.compile(make_re(word)) \
                                  for word in master_indeterminate]

        for pattern in not_allowed_patterns:
            temp = self.clean_data[:]
            temp = pattern.sub("[REDACTED]",temp[:])
            self.clean_data = temp
        for index,pattern in enumerate(indeterminate_patterns):
            temp = self.clean_data[:]
            temp = pattern.sub(master_indeterminate[index] + "[INDETER]",temp[:])
            self.clean_data = temp


def main():

    excelfile = open("September 2015 Samples De-Identified2.csv",'r')

    ExcelFile = Excel(excelfile)
    print ExcelFile.get_headers()
    subjects = ExcelFile.get_subjects()
    print type(subjects), len(subjects)
    ExcelFile.clean_data()    
    ExcelFile.make_csv()

if __name__ == "__main__":
    main()
        

        
        
        
