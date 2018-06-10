#Modified so that the main function returns a list of items and their occurences
#Sorted in descending order
#This version doesnt print anything. Previous ones do
#This version is built to be called from another script

def processLine(line,itemCounts):      #Identify each item in the line(assumes items are comma separated). Process word then add it to the dictionary)
    line= line.strip()            #Remove leading and trailing whitespace
    while (line[-1] is ","):
        line= line[ :-1]            #Remove all trailing commas
    
    while ("," in line):
        item= line[ :line.find(",")]        #new substring comprising all characters upto the comma
        item= processWord(item)             #Make all lower case, remove special xters and white spaces
                                                
        countItem(item,itemCounts)                     #Add item to dictionary or increase count if its already there
        
        line= line[line.find(",")+1: ]      #Remove this item from the current line

#When there are no more commas, line still contains 1 word
    while (line[-1] is ","):
        line= line[ :-1]					#Remove all trailing commas
    line= line.strip()
    line= processWord(line)   
    countItem(line, itemCounts)
    return
        

def processLineList(line):      #This version returns a list whose elements are the individual items in original line
    basket=[]
    line= line.strip()            #Remove leading and trailing whitespace
    while (line[-1] is ","):
        line= line[ :-1]            #Remove all trailing commas
    
    while ("," in line):
        item= line[ :line.find(",")]        #new substring comprising all characters upto the comma
        item= processWord(item)             #Make all lower case, remove special xters and white spaces
                                                
        basket.append(item)                     #Add item to dictionary or increase count if its already there
        
        line= line[line.find(",")+1: ]      #Remove this item from the current line

#When there are no more commas, line still contains 1 word
    while (line[-1] is ","):
        line= line[ :-1]					#REmove all trailing commas
    line= line.strip()
    line= processWord(line)   
    basket.append(line)
    return basket

        
def processWord(word):      # For each item(word), make it all lower case, remove special characters and white spaces
    word.strip()
    word= word.lower()
    word= word.replace(" ","")
    for ch in word:
        if ch in "`~!@#$%^&*()_-+={[]}|',./?;:":
            word= word.replace(ch, "")

    return word

def countItem(item,itemCounts):            #Add item to dictionary or increase count if its already there
    if item in itemCounts:
        itemCounts[item] += 1

    else:
        itemCounts[item] = 1
        return

## -----------------Start of main program---------------------##
def main(itemCounts):
    fileselect = 99 
    #fileselect=2

    while(not(fileselect>0 and fileselect<4)):      #Ensure the number selected is 1,2 or 3
      fileselect= input("Please select a file\n1.Test_data\n2.Historical_purchases\n3.Other -->\t\t")



    if fileselect== 1:
        filename= "Test_purchases.csv"

    elif fileselect== 2:
        filename= "historical_purchases.csv"

    else:
        filename= raw_input("Please enter the filename(or file path if file not in current directory)->      ")


    filename.strip()

    #print filename

    infile= open(filename, "r")

    #itemCounts= {}          #The dictionary that keeps (item,itemcount) pairs

    for line in infile:     #For each line in the selected file, get all the items there. In the csv, each line is a single basket
        processLine(line,itemCounts)


    #print itemCounts.items()
    infile.close()

    pairs= list(itemCounts.items())

    items= [[x,y] for (y,x) in pairs]

    items.sort(reverse=True)            #Sort in descending order

##    displayLimit= input("How many items would you like to see(-1 for all)->  ")
##    count= 0
##    for i in range(len(items)):
##        if displayLimit > 0:
##            if i >= displayLimit:
##                break
##        #print i+1, ".", items[i][1], "\t\t", items[i][0]
##        count +=items[i][0]
##
##    #if displayLimit <0 or displayLimit >len(items):
##        #print "The total number of items purchased in the entire dataset is ", count
##
##    #else:
##        #print "The total number of the ", displayLimit, "most popular items is", count


    return items

#itemCounts={}
#main(itemCounts)
