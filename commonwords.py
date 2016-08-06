import pickle
import os
import re
import dictionary
import logging

logging.basicConfig(level=logging.DEBUG, format= '%(message)s')
#logging.disable(logging.CRITICAL)

def remove_words(text, allowed, prohibited):
    """Returns a text with prohibited words removed, also creates user defined
    dictionary? """
    indeterm = lambda text,w: text.replace(w,w + "[Indeterminate] ")
    redactauto = lambda text,w: text.replace(w, "[Redacted][Auto]")
    redactuser = lambda text,w: text.replace(w, "[Redacted][User]")

    logging.debug('Original text is %s' % text)
    allowed_words = allowed
    prohibited_words = prohibited
    #remove punct from text
    punct_pattern = re.compile(r'[".,:\[\]()!@#$%\^&*-=_+{\}|\\/`~; ]+')
    possible_words = list(set(punct_pattern.split(text[:])))
    logging.debug('words found when splitting on punctuation %s' % \
                  str(possible_words))
    #remove empty strings found at weird punctuation places
    possible_words = [word for word in possible_words if word != ""]
    modified_text = text[:]
    for word in(possible_words):
        logging.debug(' testing word %s' % word)
        allowed = allowed_words.get(word.lower())
        prohibited = prohibited_words.get(word.lower())
        logging.debug('Allowed[%s] = %s , Prohibited[%s] = %s' % \
                      (word, allowed, word, prohibited))
        #found neither
        if allowed == None and prohibited == None:
            modified_text = indeterm(modified_text, word)
            logging.debug('%s was marked as indeterminate' % word)
            continue
        #found user allowed word
        if allowed == "User" and \
           (prohibited == "Found" or prohibited == None):
            logging.debug('%s was marked as allowed' % word)
            continue
        #found user prohibited word
        if prohibited == "User" and \
           (allowed == "Found" or allowed == None):
            logging.debug('%s was marked as prohibited' % word)
            continue
        #found user allowed and prohibited
        if prohibited == "User" and allowed == "User":
            modified_text = indeterm(modified_text,word)
            logging.debug('%s was marked as indeterminate' % word)
            continue
        #found allowed and prohibited word
        if prohibited == "Found" and allowed == "Found":
            if word[0].isupper() and word[1:len(word)].islower():
                modified_text = redactauto(modified_text,word)
                logging.debug('%s was marked as prohibited' % word)
                continue
            else:
                modified_text = indeterm(modified_text,word)
                logging.debug('%s was marked as indeterminate' % word)
                continue
        #found allowed only
        if allowed == "Found" and prohibited == None:
            logging.debug('%s was marked as allowed' % word)
            continue
        #found prohibited only
        if prohibited == "Found" and allowed == None:
            modified_text = redactauto(modified_text, word)
            logging.debug('%s was marked as prohibited' % word)
            continue
        
    return modified_text

def main():

    mydict = dictionary.Dictionary()

    a,b = mydict.export_dicts()
    print len(a), len(b)

    text = "Hello world this is vancomycin and I am ETA299  asdf  John Smith who clindamycin,\
and this is the world that we: random pucn'ctuation; will sometimes] \
kill us[all"
    print text
    print remove_words(text, a, b)
if __name__ =="__main__":
    main()

    
