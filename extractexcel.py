from patternchecker import *
import re

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

    def show_subjects(self):
        print "There are %d subjects present in this file" % (len(self.subjects))

    def export_subjects(self):
        return self.subjects

class Subject: # creats a Subject object
    def __init__(self,headers,data):

        self.data = data[:]
        self.raw_data = data[:]
        for index in range(len(self.data)):            
            self.data[index] = self.data[index].replace("<<:>>"," ")
            self.data[index] = self.data[index].replace("<<.>>",",")          
        self.headers = headers        

    def show_data(self):        
        for header in self.headers:
            print header + ":", self.data[self.headers[header]]
    def clean_data(self):
        self.clean_data = []
        for index in range(len(self.data)):
            #print "entry is", self.data[index]
            #print
            #print "raw entry is", self.raw_data[index]
            allowed, not_allowed, indeterminate = clean(self.data[index])
            results = [(allowed,"allowed"), (not_allowed,"not allowed")
                       ,(indeterminate,"indeterminate")]
            self.clean_data.append(replace(self.raw_data[index],not_allowed,indeterminate))
        return self.clean_data
        
    def show_raw_data(self):
        return self.raw_data

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
    # entry is one line in an excel file
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

    excelfile = open('September 2015 Samples De-Identified2.csv','r')
    test_Excel = Excel(excelfile)
    #test_Excel.show_headers()
    #test_Excel.show_subjects()
    subjects = test_Excel.export_subjects()
    print len(subjects)
    print subjects[0].getData()
    print subjects[0].clean_data()
            
main()
        
