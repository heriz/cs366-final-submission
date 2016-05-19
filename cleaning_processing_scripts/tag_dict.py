import os, sys
import yaml
from collections import defaultdict

"""
    to run this code:
    python3 tag_dict.py [name of file which is output from msg_cleaner.py or
    text_file_to_tagged.py] [yaml file which you want to use to store data]

    [] indicate a filename parameter in the form *.* because it doesn't really
    matter to a computer. :)

"""

def create_tag_dict(input_file, yaml_file):
  #do this so that way there are empty lists for empty entries
  all_tags = defaultdict(list)
  #this will be the output from arc with tags and words
  ark_output = open(input_file, "r")
  for lines in ark_output:
    #strip out superfluous data
    lines = lines.strip()
    #get each set of pairs
    word_pairs = lines.split(" ")
    #avoid superfluous code by using defaultdic
    for pairs in word_pairs:
      #some of the tag pairs aren't actually pairs, so just get the first two
      #   elements
      word, tag = pairs.split("_")[:2]
      all_tags[tag].append(word)
  #This is used to add to a yaml file if that's the desired behavior 
  if os.path.exists(yaml_file):
    #do some stuff to get the current values of the yaml written to hard disk
    temp = defaultdict(list)
    read_file = open(yaml_file, "r")
    tags = yaml.load(read_file)
    #kind of ridiculous, but merge entries from both files
    for entries in tags:
      #do a merge of the two lists
      temp[entries] = tags[entries] + all_tags[entries]
      #get rid of all the duplicates
      temp[entries] = list(set(temp[entries]))
    #close this file
    read_file.close()
    #so you can remove it
    os.remove(yaml_file)
    #output this new temporary dictionary into the same yaml name
    output = open(yaml_file,"w")
    yaml.dump(temp, output)
    output.close()
  else:
    #otherwise, just write everything to the new yaml file
    output = open(yaml_file, "w")
    for entries in all_tags:
      all_tags[entries] = list(set(all_tags[entries]))
    yaml.dump(all_tags, output)
    output.close()

def main(arg):
  #set up the input and output file here
  input_file = arg[1]
  yaml_file = arg[2]
  #make the script friendlier if being run from the commandline
  #print("Adding terms and tags for " + input_file + " to " + yaml_file)
  create_tag_dict(input_file, yaml_file)
  


if __name__ == "__main__":
  main(sys.argv)
