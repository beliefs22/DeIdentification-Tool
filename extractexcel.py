from patternchecker import *
import re
import msvcrt
import os

class Excel: #creates an excel object.

    def __init__(self,excelfile):
        self.excelfile = excelfile
        self.headers = {}
        self.subjects = []
        self.header_list = self.excelfile.readline().rstrip("\n").split(",")
        for index, header in enumerate(self.header_list):
            #print index, header
            self.headers[header] = index     
        for rawdata in self.excelfile:
            data = rawdata.rstrip("\n").split(",")
            self.subjects.append(Subject(self.headers,data))

    def show_headers(self):
        headers = self.headers.keys()
        unordered_headers = [(self.headers[header],header) for header in headers]
        unordered_headers.sort()
        for item in unordered_headers:
            print item[0], item[1]
    
    def clean_data(self):
        self.user_allowed_dict = []
        self.user_not_allowed_dict = []
        if os.path.exists('useralloweddictionary.txt'):            
            myfile1 = open('useralloweddictionary.txt','r')
            for line in myfile1:
                self.user_allowed_dict.append(line.rstrip("\n"))
            myfile1.close()
        if os.path.exists('usernotalloweddict.txt'):
            myfile2 = open('usernotalloweddict.txt','r')
            for line in myfile2:
                self.user_not_allowed_dict.append(line.rstrip("\n"))
            myfile2.close()

        master_allowed = []
        master_not_allowed = []
        master_indeterminate = []
        for subject in self.subjects:
            allowed,not_allowed,indeterminate = subject.first_pass()
            for item in allowed:
                master_allowed.append(item)
            for item in not_allowed:
                master_not_allowed.append(item)
            for item in indeterminate:
                master_indeterminate.append(item)
        print 'there are %d indeterm items' % len(master_indeterminate)
        master_indeterminate = list(set(sorted(master_indeterminate)))        
        print 'there are %d indeterm items' % len(master_indeterminate)
        print master_indeterminate
        for word in master_indeterminate[:]:
            print 'Is %s an allowed word? Please enter y or n or u ' % word
            choice = msvcrt.getch()
            if choice.lower() == 'y':
                self.user_allowed_dict.append(word)
                master_allowed.append(word)
                master_indeterminate.remove(word)
            if choice.lower() == 'n':
                self.user_not_allowed_dict.append(word)
                master_not_allowed.append(word)
                master_not_allowed.append(word)
        print "choices done"        
        master_allowed = list(set(master_allowed))
        master_not_allowed = list(set(master_not_allowed))
        print "setting done"
        for subject in self.subjects:
            print "starting final pass"
            subject.final_pass(master_not_allowed,master_indeterminate)                
        self.user_allowed_dict = list(set(self.user_allowed_dict))
        self.user_not_allowed_dict = list(set(self.user_not_allowed_dict))
        myfile1 = open('useralloweddictionary.txt','w')
        myfile2 = open('usernotalloweddict.txt','w')
        for item in self.user_allowed_dict:
            print "writing usser"
            myfile1.write(item.lower() + "\n")
        for item in self.user_not_allowed_dict:
            print "writing not allowed"
            myfile2.write(item.lower() + "\n")
        myfile1.close()
        myfile2.close()
        
        
    def show_subjects(self):
        print "There are %d subjects present in this file" % (len(self.subjects))

    def export_subjects(self):
        return self.subjects

    def create_final_csv(self):
        final_data = []
        final_data.append(",".join(self.header_list))
        for subject in self.subjects:
            print "creating final cvs"
            final_data.append(",".join(subject.show_clean_data()))
        myfile = open('final_clean_data.csv','w')
        for line in final_data:
            myfile.write(line + "\n")
        myfile.close()
        

class Subject: # creats a Subject object
    def __init__(self,headers,data):

        self.data = data[:]
        self.raw_data = data[:]
        self.clean_data = []
        for index in range(len(self.data)):            
            self.data[index] = self.data[index].replace("<<:>>"," ")
            self.data[index] = self.data[index].replace("<<.>>",",")          
        self.headers = headers        

    def show_data(self):        
        for header in self.headers:
            print header + ":", self.data[self.headers[header]]
            
    def first_pass(self):
        master_allowed = []
        master_not_allowed = []
        master_indeterminate = []
        
        for index in range(len(self.data)):
            allowed, not_allowed, indeterminate = clean(self.data[index])
            for item in allowed:
                master_allowed.append(item)
            for item in not_allowed:
                master_not_allowed.append(item)
            for item in indeterminate:
                master_indeterminate.append(item)
        return master_allowed, master_not_allowed, master_indeterminate                                                
            
    def final_pass(self,master_not_allowed,master_indeterminate):
        for index in range(len(self.data)):
            #print "entry is", self.data[index]
            #print
            #print "raw entry is", self.raw_data[index]
            self.clean_data.append(replace(self.raw_data[index],master_not_allowed,master_indeterminate))
        
        
    def show_raw_data(self):
        return self.raw_data

    def show_clean_data(self):
        return self.clean_data

    def getData(self):
        return self.data
        
def extract(myfile):
    all_words = []
    raw_words = []
    for line in myfile:
        temp = line.rstrip("\n").split(",")
        print temp
        
        for item in temp:
            a = item.split(" ")
            for word in a:
                raw_words.append(word)
                word = word.replace("<<:>>","")
                word = word.replace("<<.>>",",")
                all_words.append(word)
    return all_words

def clean(entry):
    # entry is one line from one subject in an excel file
    allowed = []
    not_allowed = []
    indeterminate = []
    pattern_matches, unmatched = check_patterns(entry)
    #print "umatched", unmatched, len(unmatched)
    if len(unmatched) > 1:
        
        allowed,not_allowed,indeterminate = check_words(unmatched)
        #print "inde", indeterminate, "" in indeterminate, " " in indeterminate
    not_allowed = not_allowed + pattern_matches
    return allowed, not_allowed, indeterminate

def final_clean(entry,userdict):
    # entry is one line in an excel file
    allowed = []
    not_allowed = []
    indeterminate = []
    pattern_matches, unmatched = check_patterns(entry)
    #print "umatched", unmatched, len(unmatched)
    if len(unmatched) > 1:        
        allowed,not_allowed,indeterminate = check_words_final(unmatched,userdict)
        #print "inde", indeterminate, "" in indeterminate, " " in indeterminate
    not_allowed = not_allowed + pattern_matches
    return allowed, not_allowed, indeterminate

def make_re(word):
    return r'\b(%s)\b' % word

def replace(entry,not_allowed,indeterminate):
    not_allowed = [re.compile(make_re(word)) for word in not_allowed]
    indeterminate = [re.compile(make_re(word)) for word in indeterminate]
    inside_pattern = re.compile("(\()(.*)(\))")
    for pattern in not_allowed:
        entry = pattern.sub("[REDACTED]",entry,1)
    for pattern in indeterminate:
        inside = inside_pattern.search(pattern.pattern)
        entry = pattern.sub(inside.group(2).upper() + "[INDETERMINATE]",entry)
    return entry

def main():
    choice = raw_input('What is your file name?')
    excelfile = open(choice,'r')
    test_Excel = Excel(excelfile)
    test_Excel.show_headers()
    test_Excel.clean_data()
    test_Excel.create_final_csv()
    subjects = test_Excel.export_subjects()
            
main()
        
