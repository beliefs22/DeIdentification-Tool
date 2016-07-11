import datechecker
import commonwords
import dictionary

class Cleaner:

    def __init__(self, Dictionary):

        self.allowed_words, self.prohibited_words = Dictionary.export_dicts()

    def clean_text(self,text):
        """Returns given text with dates and prohibited words removed.
        Indeterminate words are marked as such
        """        
        cleaned_text = ""
        #remove dates
        cleaned_text = datechecker.remove_dates(text)
        #marked remove prohibited words, mark indeterminate words
        cleaned_text = commonwords.remove_words(cleaned_text, self.allowed_words,
                                                self.prohibited_words)

        return cleaned_text


        
        



def main():

    mydict = dictionary.Dictionary()
    text = "Hello world this is 2/2015 and 2/26 but not 2/5/2353 and vancomycin \
is here to make John Lilly angry"
    mycleaner = Cleaner(mydict)

    print text
    print mycleaner.clean_text(text)

if __name__ == "__main__":
    main()
                
    
        
            
