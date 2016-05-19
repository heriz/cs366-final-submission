#!/bin/bash


#automatically create the master yaml file from all of the files in the cleaned
# folder -- used to be default output location for initial cleaning script
# NOTE: This file requires that the files be in word_tag format

#will automatically set the current working directory to the current directory
FILES=`ls ./cleaned`
CWD=`pwd`

#run a for loop for all of the files in the directory created
for item in $FILES
do
    #echo this just to make sure that's where things should be -- visual
    #    inspection--
    #echo "python3 tag_dict.py ./cleaned/$item data.yaml"
    `python3 $CWD/tag_dict.py $CWD/cleaned/$item $CWD/data.yaml`
done
