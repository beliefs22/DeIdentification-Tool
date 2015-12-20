from newpatternchecker import *
import re
import getchall
import os
import pickle


def deidentify(subjects,MainFrame ):
    master_allowed = []
    master_not_allowed = []
    master_indeterminate = []
    sample_size = len(subjects)/ 10
    if sample_size < 1:
        sample_size = len(subjects)

    temp_allowed, temp_not_allowed, temp_indeterminate = one_pass(MainFrame,
                            subjects,master_allowed,master_not_allowed,
                            master_indeterminate, sample_size)    
    one_pass(MainFramesubjects,temp_allowed,temp_not_allowed,
             temp_indeterminate)
    
def one_pass(MainFrame,subjects,master_allowed,master_not_allowed,master_indeterminate, num=None):
    master_allowed = master_allowed[:]
    master_not_allowed = master_not_allowed[:]
    master_indeterminate = master_indeterminate[:]
    if num == None:
        num = len(subjects)
    for i in range(num):
        print "cleaning subject ", i
        #print "subject type is", subjects[i], i
        allowed,not_allowed,indeterminate = subjects[i].clean()
        for word in allowed:
            if word not in master_allowed:
                master_allowed.append(word)
        for word in not_allowed:
            if word not in master_not_allowed:
                master_not_allowed.append(word)
        for word in indeterminate:
            if word not in master_indeterminate:
                master_indeterminate.append(word)
    user_allowed, user_not_allowed, temp_indeterminate = ask_user(MainFrame
        master_allowed, master_not_allowed,master_indeterminate)

    create_user_dictionary(user_allowed, user_not_allowed)

    for word in user_not_allowed:
        if word not in temp_indeterminate:
           temp_indeterminate.append(word)
    master_indeterminate = temp_indeterminate
    for i in range(num):
        print "final cleaning", i
        subjects[i].final_clean(master_not_allowed, master_indeterminate)
    

    return master_allowed, master_not_allowed, master_indeterminate
     
def ask_user(MainFrame, master_allowed,master_not_allowed,master_indeterminate):
    
    allowed = master_allowed[:]
    not_allowed = master_not_allowed[:]
    indeterminate = master_indeterminate[:]
    user_allowed = list()
    user_not_allowed = list()
    MainFrame.update_list(indeterminate)
    
    
    for word in indeterminate[:]:
        print "Word is %s. Is this allowed? Y N U - " % word
        choice = getch()
        if choice.lower().startswith('y'):
            #print "added allowed"
            user_allowed.append(word)
            indeterminate.remove(word)
        if choice.lower().startswith('n'):
            #print "added not allowed"
            user_not_allowed.append(word)
            indeterminate.remove(word)
        
    return user_allowed, user_not_allowed, indeterminate


def create_user_dictionary(user_allowed,user_not_allowed):
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
        
    
class Excel:

    def __init__(self,excelfile):

        self.excelfile = excelfile
        self.raw_headers = excelfile.readline().rstrip("\n").split(",")
        self.headers = {}

        for index, header in enumerate(self.raw_headers):
            self.headers[header] = index

        self.subjects = []

        for subjectdata in excelfile:
            raw_data = subjectdata.rstrip("\n")
            self.subjects.append(Subject(self.headers,raw_data))

    def clean_data(self):
        deidentify(self.subjects)
        

    def get_headers(self):
        return self.headers

    def get_subjects(self):
        return self.subjects

    def get_num_of_subjects(self):
        return len(self.subjects)

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
        

        
        
        
