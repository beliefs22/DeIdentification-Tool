import cleaner
import excelclass
import dictionary


def main():

    excelfile = excelclass.ExcelFile('csvs/test_csv_2.csv')
    subjects = excelfile.getSubjects()
    headers = self.getHeaders()
    clean_subjects = []
    cleaning_dictionary = dictionary.Dictionary()
    mycleaner = Cleaner(cleaning_dictionary)

    for subject in subjects:
        old_data = subject.getData()
        cleaned_data = []
        for header in headers:
             cleaned_data.append(mycleaner.clean_text(old_data[header]))
        cleaned_subjects.append(Subject(headers, cleaned_data)
             
            

    

        
            
            
        
    
    
