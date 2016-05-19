#!/bin/bash


#automate the running of the python script to get newly cleaned files
#will automatically set the current working directory to the current directory
FILES=`ls *.mbox`
CWD=`pwd`

#it's easiest to run this from the file which contains all of the mbox files

#this is a for loop going over elements in the FILES variable
for item in $FILES
do
    #this will get the first item from the item variable created above
    textfile="${item[0]}.txt"
    #this runs a raw bash command to create the destination directory
    `mkdir cleaned`
    #this will echo what is going where to check
    echo "python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned/$textfile"
    #this will actually run that command through the script
    `python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned/$textfile`
done

#for item in $FILES
#do
#    textfile="${item[0]}.txt"
#    `mkdir cleaned_tag_only`
#    echo "python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned_tag_only/$textfile t t"
#    `python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned_tag_only/$textfile t t`
#done
