from patternchecker import *
import re
import getchall
import os

class Excel:
    """ Object Reprsenting an excel file containing subject data
        Attributes:
            subjects (list): list containing Subject objects which represent
            a complete entry in the data file
            headers (list) : list containing headers of excel file
    """

    def __init__(self,excelfile):
        """
        Args:
            excelfile (file): csv to be de-identified
        """      

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
        """Print headers for excel file to screen"""
        headers = self.headers.keys()
        unordered_headers = [(self.headers[header],header) for header in headers]
        unordered_headers.sort()
        for item in unordered_headers:
            print item[0], item[1]

    def create_word_lists(self):
        """De-Identification Process"""
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
        master_indeterminate = list(set(sorted(master_indeterminate)))
        return list(set(master_allowed)), list(set(master_not_allowed)), \
               master_indeterminate

    def create_user_dicts(self,user_allowed,user_not_allowed):
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
        for item in user_allowed:
            if item not in self.user_allowed_dict:
                self.user_allowed_dict.append(item)
        myfile1 = open('useralloweddictionary.txt','w')
        for word in self.user_allowed_dict:
            myfile1.write(word + "\n")
        myfile1.close()        
        for item in user_not_allowed:
            if item not in self.user_not_allowed_dict:
                self.user_not_allowed_dict.append(item)
        myfile2 = open('usernotalloweddict.txt','w')
        for word in self.user_not_allowed_dict:
            myfile2.write(word + "\n")
        
        
    def clean_data(self, master_not_allowed,master_indeterminate):
        for subject in self.subjects:
            print "doing final pass"
            subject.final_pass(master_not_allowed,master_indeterminate)        
        final_data = []
        final_data.append(",".join(self.header_list))
        for subject in self.subjects:
            print "creating final cvs"
            final_data.append(",".join(subject.show_clean_data()))
        myfile = open('final_clean_data.csv','w')
        for line in final_data:
            myfile.write(line + "\n")
        myfile.close()
  
    def show_subjects(self):
        """Print number of subjects contained in excel file"""
        print "There are %d subjects present in this file" % (len(self.subjects))

    def export_subjects(self):
        """Return list of Subject objects created from excel file"""
        return self.subjects

class Subject:
    """Object representing single entry in an excel file"""
    def __init__(self,headers,data):
        """
        Args:
        headers (list) : list of headers for the subjects excel file
        data (list) : list where each index is a cell from the subjects file
    """

        self.data = data[:]
        self.raw_data = data[:]
        self.clean_data = []
        for index in range(len(self.data)):            
            self.data[index] = self.data[index].replace("<<:>>"," ")
            self.data[index] = self.data[index].replace("<<.>>",",")          
        self.headers = headers        

    def show_data(self):
        """Print data for subject to screen with headers. Headers: data"""
        for header in self.headers:
            print header + ":", self.data[self.headers[header]]
            
    def first_pass(self):
        """Find allowed not_allowed, and indeterminate words in file"""
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
        """Replaces words in data with [Redacted] or [Indeterminate]"""
        for index in range(len(self.data)):
            #print "entry is", self.data[index]
            #print
            #print "raw entry is", self.raw_data[index]
            self.clean_data.append(replace(self.raw_data[index],master_not_allowed,master_indeterminate))
        
        
    def show_raw_data(self):
        """Return list containing raw data for subject"""
        return self.raw_data

    def show_clean_data(self):
        """Return list containing de-identified data for subject"""
        return self.clean_data

def clean(entry):
    """Cleans a single entry to data
    Args:
        entry (str): str representing data entry for a subject

    Return:
        allowed (list): list of words that were found that were allowed
        not_allowed (list): list of words that are not allowed
        indeterminate (list): list of words that found that were
        indeterminate
    """
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


def make_re(word):
    """Return regular expression object created from given word
    Args:
        word (str): word to make into a regular expression object

    Return:
        regular expression object
    """
    return r'\b(%s)\b' % word

def replace(entry,not_allowed,indeterminate):
    """Return str representing a cleaned data entry
    Args:
        entry (str): entry to be claned
        not_allowed (list): list of words that are not allowed, if a match is
        found will be replaced with [REDACTED]
        indeterminate (list): list of words that are indeterminate, if a match
        is found it will be replaced with [Indeterminate]

    Return:
        str where allowed and not_allowed words have been replaced
    """

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

if __name__ == '__main__':
    main()
        
