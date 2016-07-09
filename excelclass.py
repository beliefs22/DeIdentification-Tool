import csv

class ExcelFile:
    """Object representing an excel file in .csv format
    """

    def __init__(self, filename):
        #excel files are in .csv format
        with open(filename,'r') as excelfile:
            excelreader = csv.reader(excelfile)
            self.headers = excelreader.next()

            self.subjects = []
            #create a subject object for each line in the file
            for data in excelreader:
                self.subjects.append(Subject(self.headers,data))

    def getSubjects(self):
        """return all subject objects created from excel file"""
        return self.subjects

class Subject:
    """Represents data for a subject extracted from one line of an excel file
    """

    def __init__(self, headers, data):

        self.subjectdata = {}
        #check to make sure you have a header for each group of data
        if len(headers) == len(data):
            for index, header in enumerate(headers):
                self.subjectdata[header] = data[index]


    def getData(self):

        return self.subjectdata

                
                
            
        
