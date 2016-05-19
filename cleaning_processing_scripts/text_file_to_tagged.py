import sys, os
from subprocess import call

def main(arg):
  file_input= arg[1]
  file_output=arg[2]
  temp = open("temp.txt","w")
  call(["./runTagger.sh", "--model",
      "model.ritter_ptb_alldata_fixed.20130723.txt",
      "../"+file_input],cwd="./ark-tweet-nlp-0.3.2/",stdout=temp)
  temp.close()
  tagged = open("temp.txt","r")
  tagged_sentences = list()
  for phrases in tagged:
    word_tag_pair = list()
    words, tags = phrases.split("\t")[:2]

    words = words.split(" ")
    tags = tags.split(" ")
    #get the length of words for iteration
    sentenceLength = len(words)
    for i in range(sentenceLength):
      #join the words and tags with an underscore if desired
      
      pair = words[i] + "_" + tags[i]
      #then add it to the list of pairs
      word_tag_pair.append(pair)
    #Afterwards, join the pairs like a sentence
    tagged_sentence = " ".join(word_tag_pair)
    #then append it to the taggedTweets list
    tagged_sentences.append(tagged_sentence)
  tagged.close()
  #reattach the sentimnets to the tweets
  #for i in range(len(taggedTweets)):
  #    taggedTweets[i] = tweetSentiment[i] + "\t"+ taggedTweets[i]
  output_file = open(file_output, "w")
  #finally, write to the final file cleaning up temp files
  for each_sentence in tagged_sentences:
    sentence_lined = each_sentence + "\n"
    output_file.write(sentence_lined)
  output_file.close()
  #clean up the last temporary file
  os.remove("temp.txt")

if __name__ == "__main__":
  main(sys.argv)
