import pickle
import os
import re
import dictionary

def remove_words(text, allowed, prohibited):
    """Returns a text with prohibited words removed, also creates user defined
    dictionary? """
    allowed_words = allowed
    prohibited_words = prohibited
    #remove punct from text
    punct_pattern = re.compile(r'[".,:\[\]()!@#$%\^&*-=_+{\}|\\/`~; ]+')
    possible_words = list(set(punct_pattern.split(text[:])))
    #remove empty strings found at weird punctuation places
    possible_words = [word for word in possible_words if word != ""]
    modified_text = text[:]
    for word in(possible_words):
        allowed = allowed_words.get(word.lower())
        prohibited = prohibited_words.get(word.lower())
        if (allowed == "User" and prohibited == "User") or \
           (allowed == "Found" and prohibited == "Found"):
            modified_text = \
                          modified_text.replace(
                              word, '[Indeterminate]' + word + " ")
        elif allowed == "User" or allowed == "Found":
            pass
        elif prohibited == "User" or prohibited == "Found":
            if prohibited == "User":
                modified_text = \
                              modified_text.replace(word, '[REDACTED][User] ')
            else:
                modified_text = \
                              modified_text.replace(word, '[REDACTED][Auto]')
    return modified_text
def main():

    mydict = dictionary.Dictionary()

    a,b = mydict.export_dicts()
    print len(a), len(b)

    text = "Hello world this is vancomycin and I am     John Smith who clindamycin,\
and this is the world that we: random pucn'ctuation; will sometimes] \
kill us[all"
    print text
    print remove_words(text, a, b)
if __name__ =="__main__":
    main()

    
