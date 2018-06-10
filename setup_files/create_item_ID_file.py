#This script is designed to be run only once ever!
#This script runs the script item_occurence_count and creates a new file(or writes into an existing one in the same directory)
#called Item_IDs that assigns an ID to every item occuring in the transactional dataset(required by item_occurence)
#Each item has a name and a UID. The UID's count from 1 upwards
#The text file is tab separated and lines end in a line feed(newline) xter
#It is designed to be loaded onto a database e.g MySQL

import item_occurence_count3 as icc



tempDict={}

item= icc.main(tempDict)
count= 0

count= input("How many unique items should be in the database(-1 for max)?-->  ")
assert count < len(item)		#TODO: Fail gracefully and display suitable error message

if count < 0:
    count= len(item)

outfile= open("Item_IDs.txt","w")
for i in range (count):
    outfile.write(str(i+1))
    outfile.write("\t")
    outfile.write(item[i][1])
    outfile.write("\n")

outfile.close()
