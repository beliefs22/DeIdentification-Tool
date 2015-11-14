def create_dict(myfile):
    complete_dictionary = open("completedict.txt","w")    
    for line in myfile:
        temp = line.rstrip("\n").split(" ")        
        if len(temp) == 1 or len(temp) == 2:
            pass
        elif "." in temp[1]:
            complete_dictionary.write(temp[0] + " " + temp[1] + "\n")
        else:
            complete_dictionary.write(temp[0] + " " + temp[1] + " " + temp[2] + "\n")
    complete_dictionary.close()

class Dictionary:    

    def __init__(self, dictionary):

        self.prefix = ['anti','de','dis','en','em','fore','in','im','il','ir','inter',
              'mid','mis','non','over','pre','re','semi','sub','super','trans',
              'un','under']

        self.suffix = ['able','ible','al','ial','ed','en','er','est','ful','ic','ing','ion'
              ,'tion','ation','ition','ity','ty','ive','ative','itive','less','ly',
              'ment','ness','ous','eous','ious','s','es','y']
        self.complete_dict = {}
        for line in dictionary:
            temp = line.rstrip("\n").split(" ")
            self.complete_dict[temp[0].lower()] = None                            
            

    def size(self):
        return len(self.complete_dict)
    
    def check_word(self,word):
        found = False
        if word in self.complete_dict:
            return True
        else:
            for pre in self.prefix:                
                if word[:len(pre)] == pre and word[len(pre):] in self.complete_dict:
                    print word[len(pre):]
                    print pre
                    print "first ran"
                    return True
            for suf in self.suffix:
                if word[-len(suf):] == suf:
                    print word[:-len(suf)]
                    print "second ran"
                    print suf
                    return True
                
        if found == False:
            return False
            

def main():

    dictionary = open("completedict.txt","r")
    my_dict = Dictionary(dictionary)
    print my_dict.size()
    print my_dict.check_word("establishment")
    print my_dict.check_word("anticopulated")
        

main()
        
