import datachecker

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

        self.data = data        
        for index in range(len(self.data)):            
            self.data[index] = self.data[index].replace("<<:>>"," ")
            self.data[index] = self.data[index].replace("<<.>>",",")          
        self.headers = headers        

    def show_data(self):
        
        for header in self.headers:
            print header + ":", self.data[self.headers[header]]

    def getData(self):
        return self.data
        

        
def extract(myfile):
    all_words = []
    for line in myfile:
        temp = line.rstrip("\n").split(",")
        
        for item in temp:
            a = item.split(" ")
            for word in a:
               
                word = word.replace("<<:>>","")
                word = word.replace("<<.>>",",")
                all_words.append(word)
    return all_words

def clean(data):
    allowed = {}
    not_allowed = {}
    indeterminate = {}

    for entry in data:
        temp = entry.split(" ")
        for item in temp:
            stats, allow = datachecker.check_word(item)            
            if allow == "allowed":
                if item in allowed:
                    allowed[item] = allowed[item] + 1
                else:
                    allowed[item] = 1
            if allow == "not allowed":
                if item in not_allowed:
                    not_allowed[item] = not_allowed[item] + 1
                else:
                    not_allowed[item] = 1
            if allow == "indeterminate":
                if item in indeterminate:
                    indeterminate[item] = indeterminate[item] + 1
                else:
                    indeterminate[item] = 1
    return allowed, not_allowed, indeterminate
def main():

    excelfile = open('September 2015 Samples De-Identified2.csv','r')
    test_Excel = Excel(excelfile)
    #test_Excel.show_headers()
    #test_Excel.show_subjects()
    subjects = test_Excel.export_subjects()
    print len(subjects)
    allowed, not_allowed, indeterminate = clean(subjects[0].getData())
    results = [[allowed,"allowed"],[not_allowed,"not_allowed"],[indeterminate,
                "indeterminate"]]
    for dictionary in results:
        pairs = list(dictionary[0].items())
        print
        print dictionary[1].upper()
        print "_________________________________________________"
        print        
               
        for words in pairs:
            print str(words[0]) + "|" + str(words[1])
    for item in subjects[0].getData():
        print item


main()
        
