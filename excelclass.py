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
    def getHeaders(self):
        """return list of headers for excel file"""
        return self.headers
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
        """return dictionary of headers mapped to data for that header"""

        return self.subjectdata

class CleanExcelFile:
    """object representing cleaned excel file to be exported into csv"""
    def __init__(self, header_data, cleaned_subjects):
        self.headers = header_data
        self.subjects = cleaned_subjects


    def create_csv(self, outfile_name):
        with open(outfile_name,'w') as output:
            output_writer = csv.writer(output, dialect='excel')
            csv.writerow(self.headers)
            for subject in self.subjects:
                row = []
                data_to_write = subject.getData()
                for header in self.headers:
                    row.append(data_to_write[header])
                csv.writerow(self.headers)



        
        
                
                
            
        
