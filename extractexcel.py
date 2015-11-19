def extract(myfile):
    i = 0
    for line in myfile:
        temp = line.rstrip("\n").split(",")
        #print temp
        for item in temp:
            a = item.split(" ")
            for word in a:
               # print word
               # print word
                word = word.replace("<<:>>","")
                word = word.replace("<<.>>","")
                print word
            
            
        i += 1
        if i > 20:
            break

def main():

    myfile = open("September 2015 Samples De-Identified2.csv","r")

    extract(myfile)

    myfile.close()

main()
        
