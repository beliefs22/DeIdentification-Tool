import cleaner
import excelclass
import dictionary


def main():

    excelfile = excelclass.ExcelFile('csvs/A_test_csv.csv')
    subjects = excelfile.getSubjects()
    headers = excelfile.getHeaders()
    cleaned_subjects = []
    cleaning_dictionary = dictionary.Dictionary()
    mycleaner = cleaner.Cleaner(cleaning_dictionary)

    for subject in subjects:
        old_data = subject.getData()
        print old_data
        cleaned_data = []
        for header in headers:
            #print header, old_data[header], mycleaner.clean_text(old_data[header])
            cleaned_data.append(mycleaner.clean_text(old_data[header]))
        cleaned_subjects.append(excelclass.Subject(headers, cleaned_data))
        print cleaned_data

    clean_excelfile = excelclass.CleanedExcelFile(headers, cleaned_subjects)
    clean_excelfile.create_csv('csvs/CleanData/newmethod.csv')
        
if __name__=="__main__":
    main()
             
            

    

        
            
            
        
    
    
