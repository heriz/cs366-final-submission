from collections import defaultdict
import yaml
import random
import sys, os
import re
import nltk

def replace_word_random(tag, dictionary):
  options = len(dictionary[tag])
  if options > 0:
    choice = random.randint(0, options - 1)
    return dictionary[tag][choice].lower()
  else:
    return ""

def replace_and_output(input_file, output_file, yaml_file):
  yaml_load_file = open(yaml_file, "r")
  dict_file = yaml.load(yaml_load_file)
  yaml_load_file.close()
  lines = open(input_file, "r")
  line_list = list()
  for line in lines:
    word_list = list()
    words = line.split(" ")
    for word in words:
      word_list.append(replace_word_random(word, dict_file))
    #@todo make sure that space isn't added before period
    sentence = " ".join(word_list)
    punctuation = re.findall(r"(\ )([\.\,\!\)\]\;\:]+)",sentence)
    if punctuation:
      for entries in punctuation:
        space_punctuated = entries[0] + entries[1]
        sentence = sentence.replace(space_punctuated, entries[1])
    punctuation_left = re.findall(r"([\(\[]+)(\ )", sentence)
    if punctuation_left:
      for entries in punctuation_left:
        brackies = entries[0] + entries[1]
        sentence = sentence.replace(brackies, entries[0])
    line_list.append(sentence)
  lines.close()
  write_file = open(output_file, "w")
  for line in line_list:
    write_file.write(line+"\n")
  write_file.close()


def main(arg):
  input_file = arg[1]
  output_file = arg[2]
  yaml_file = arg[3]
  replace_and_output(input_file, output_file, yaml_file) 


if __name__ == "__main__":
  main(sys.argv)
