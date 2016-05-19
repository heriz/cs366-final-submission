import sys
import random
import jumble as j
from random import choice

def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        d[key].append(third)

    return d

def generate_sentence(d, eos):
    """
      Markov Chain function which will generate a sentence
    """
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in eos:
            break
        # else
        key = (second, third)
        first, second = key
 
    return ' '.join(li)


def generate_email(greeting_file, body_file, closing_file, output_file,
    replace=False, par_min=2, par_max=4, sen_min=1, sen_max=4):
    """
      This function generates an email of the format opening -> body -> closing
      The opening and the closing are chosen from a predefined list of openings
      and closings, but the body is randomly generated using markov chains.
      @param greeting_file filename the file to pull email greetings from
      @param body_file     filename the file to pull email body text from
      @param closing_file  filename the file to pull email closers from
      @param output_file   filename the file to write output to
      @param replace       boolean  the flag to set if word replacement is
                                    desired
      @param par_min       integer  the minimum paragraph amount
      @param par_max       integer  the maximum paragraph amount
      @param sen_min       integer  the minimum sentence  amount
      @param sen_max       integer  the maximum sentence  amount
    """

    with open(greeting_file, "rt", encoding="utf-8") as f:
        greeting_text = f.read()
    with open(body_file, "rt", encoding="utf-8") as g:
        body_text = g.read()
    with open(closing_file, "rt", encoding="utf-8") as h:
        closing_text = h.read()

    output = open(output_file, "w")

    # remove residual empty strings
    greeting_list = list(filter(None, greeting_text.split("\n")))
    closing_list = list(filter(None, closing_text.split("\n")))

    # * is designated newline character in source text file
    for i in range(len(closing_list)):
        closing_list[i] = closing_list[i].replace('*','\n')

    #get all the greeting words into a dict
    greeting_words = greeting_text.split()
    greeting = build_dict(greeting_words)

    #get all of the body words into a dict
    body_words = body_text.split()
    body = build_dict(body_words)

    #these strings denote end of sentence 
    body_EOS = ['.', '?', '!']
    
    #choose a greeting and closing randomly rather than generating
    greeting = str(random.choice(greeting_list))
    closing = str(random.choice(closing_list))
    
    #initialize the message body
    message = ""
    #here we set the amount of body paragraph
    body_len = random.randint(par_min, par_max)

    #first step of building the message: append the greeting
    message += "\n" + greeting + "\n\n"

    #this is to highlight the word that is being replaced
    highlighting = False

    #create a certain amount of paragraphs
    for i in range(body_len):
      #make the amount of sentences per paragraph different
      paragraph_len = random.randint(sen_min,sen_max)
      #generate the decided amount of sentences
      for l in range(paragraph_len):
        sentence = generate_sentence(body, body_EOS) + " "
        #if the flag was set, then do replacements
        if(replace):
          #look through all of the words
          for word in sentence.split():
            #check if replaceable noun first
            if(j.is_replaceable_noun(word) and
               random.randint(1,100) <= j.noun_replacement_prob):
                if(highlighting):
                    message += "*" + j.switch_noun(word) + "*" + " "
                else:
                    message += j.switch_noun(word) + " "
            #else check if in adverb list - these should all work
            elif(word in j.adverb_list and
                    random.randint(1,100) <= j.adverb_replacement_prob):
                    if(highlighting):
                        message += "*" + j.switch_by_pos(word, j.adverb_list) + "*" + " "
                    else:
                        message += j.switch_by_pos(word, j.adverb_list) + " "
            #else check if in adjective list - these shouldn't have bum results
            elif(word in j.adjective_list and
                    random.randint(1,100) <= j.adjective_replacement_prob):
                    if(highlighting):
                        message += "*" + j.switch_by_pos(word, j.adjective_list) + "*" + " "
                    else:
                        message += j.switch_by_pos(word, j.adjective_list) + " "
            #append the word to the message
            else:
                message += word + " "
        #if replace wasn't set up, just append the sentence
        else:
          message += sentence
      #at the end add new lines to the message
      message += "\n\n"

    #now add the closing
    message += "\n\n\n" + closing + "\n"
    
    #and write the file!
    output.write(message)
    output.close()

def main():
    generate_email(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()
