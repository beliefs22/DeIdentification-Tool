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

def clean_text(text, Dictionary):
    """Attempts to remove or mark each work that could be a name or date
    in the given text. Return a string with those words removed or marked
    indeterminate
    """
    #Dictionary object contains list of allowed and prohibited words
    allowed,prohibited = Dictionary.export_dicts()

    cleaned_text = ""
    #remove dates
    cleaned_text = datechecker.remove_dates(text)
    #remove prohibited words, and mark ambiguous words as indeerminate
    cleaned_text = commonwords.remove_words(cleaned_text, allowed,prohibited)

    return cleaned_text

def main():

    mydict = dictionary.Dictionary()
    text = "Hello world this is 2/2015 and 2/26 but not 2/5/2353 and vancomycin \
is here to make John Lilly angry"
    mycleaner = Cleaner(mydict)

    print text
    print mycleaner.clean_text(text)
    print clean_text(text, mydict)

if __name__ == "__main__":
    main()
                
    
        
            
