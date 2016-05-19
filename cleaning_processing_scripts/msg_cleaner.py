##########################################
#
#
#   This code was pulled from:
# http://stackoverflow.com/questions/7166922/
#  extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
#
##########################################

import mailbox
import sys, os
import re
import unicodedata
from subprocess import call

def get_charsets(msg):
  #add stuff to the character set if not None
  charsets = set({})
  for c in msg.get_charsets():
      if c is not None:
          charsets.update([c])
  return charsets

def get_body(msg):
  #make sure that all parts of the message are evaluated
  while msg.is_multipart():
    ##append the payload of the message to the message
      msg=msg.get_payload()[0]
  #decode the message to make sure that it's readable
  t=msg.get_payload(decode=True)
  #get the list of character sets
  for charset in get_charsets(msg):
      #decode the message with character sets from message
      t=t.decode(charset)
  #return decoded message
  return t

def remove_emojis(msg):
  """
    This function will get rid of things in the unicode set listed below, which
    is the most common set of unicode emojis. A few emojis won't be taken out of
    the output, however, as they are in different range zones. this one is
    effective for our data though.
    @param msg string a string representation of the message to be cleaned.
  """
  htmlReg = re.findall(u'([\U0001f300-\U0001f64F])',msg)
  if htmlReg:
    for terms in htmlReg:
      msg = msg.replace(terms, "")
  return msg
  
def cleanup_email(email, strip_url=False):
  """
  Go through each element of the list of tweets, cleaning up overly repetitious
   words (veeeeeerrrrrrrryyyyyy -> veerryy), getting rid of html tags (<p> ->
   '') and stripping out white space and things enclosed by stars. (*very* ->
   very)
   @param  tweetList    list   list of tweets to be fully cleaned
   @return cleanTweets  list   list of fully cleaned tweets
  """
  #split on space to get words
  email = email.split("\n")
  cleanedEmail = list()
  for lines in email:
    if lines.startswith(">"):
      lines = ""
    reply_email = re.findall(r"On .*\,.*at.*\,.* \<.*@.*\> wrote:", lines)
    if reply_email:
      lines = ""
    if "begin forwarded message:" in lines.lower():
      lines = ""
    lines = lines.strip().strip("-")
    email = re.findall(r"([a-zA-Z1-9+_*]{1,255}\@.*\.)(com|net|org|edu)",lines)
    if email:
      for elem in email:
        wholeaddress = elem[0] + elem[1]
        lines = lines.replace(wholeaddress, "")
    line = lines.split(" ")
    cleanedLine = list()
    for word in line:
      cleanWord = word.strip().strip("*")
    
      #clean up the word to get rid of white space and * enclosures
      if(strip_url == True):
        if cleanWord.startswith("http") or cleanWord.startswith("www"):
          cleanWord = ""
        if cleanWord.endswith("@vassar.edu"):
          cleanWord = ""
      #if cleanWord.startswith("http") or cleanWord.startswith("www"):
      #  cleanWord = "URL"
      #elif cleanWord.startswith("@"):
      #  cleanWord = "AT_USER"
      #elif re.match(r"[0-9]",cleanWord):
      #  cleanWord = ''
      #replace words that have 4 or more repetitions with 2 of that letter
      cleanWord = re.sub(r"(.)\1{3,}", deleteRepeatingLetters, cleanWord)
        
      #attach the cleaned word to the initially clean list
      cleanedLine.append(cleanWord)
    #join the word list into a sentence
    fullyCleanedLine = " ".join(cleanedLine)
    #get rid of any html tags that snuck through the intiial cleaning
    htmlReg = re.findall(r"<[^>]+>",fullyCleanedLine)
    #if there was a match, get rid of the matching term
    if htmlReg:
      for terms in htmlReg:
        fullyCleanedLine = fullyCleanedLine.replace(terms, "")
    imageReg = re.findall(r"\[image\: .*",fullyCleanedLine)
    if imageReg:
      for terms in imageReg:
        fullyCleanedLine = fullyCleanedLine.replace(terms,"")
    #if fullyCleanedLine != "":
    cleanedEmail.append(fullyCleanedLine)
  fullyCleanedEmail = "\n".join(cleanedEmail) 
  return fullyCleanedEmail

def deleteRepeatingLetters(matchobj):
  """
  Use this to reduce the match object to the first two of the match, which will
   be called from from the re.sub area.
  @param   matchobj     matchobj     the object created when re search matches
  @return  replacement  string       the string to replace when matched
  """
  replacement = matchobj.group(0)[:2]
  return replacement

def main(argv):
  #deal with multiple argument amounts
  input_file = argv[1]
  output_file = argv[2]
  #since I didn't want to have a certain amount of arguments required,
  # this set of statements changes how things are interpreted based on
  # the amount of arguments that are fed into the function
  if len(argv) == 4:
    #in this situation, you run the tagger, but don't only have POS tags
    tagger_flag = argv[3]
    pos_flag = "f"
  elif len(argv) == 5:
    #this situation is only pos tags, but tagger must also be set bc of length
    tagger_flag = argv[3]
    pos_flag = argv[4]
  else:
    #this will set both flags to "f" for false if not set
    tagger_flag = "f"
    pos_flag = "f"

  #read in from the input file
  current_mailbox = mailbox.mbox(input_file)
  #create an intermediary file if necessary, otherwise write directly
  if tagger_flag == "t":
    write_file = open("interText.txt", "w")
  else:
    write_file = open(output_file, 'w')
  #use this to store the emails
  decoded_emails = list()
  #get all of the emails in the current_mailbox
  for this_email in current_mailbox:
    #get body and then run all cleaning routines
    body = get_body(this_email)
    body = remove_emojis(body)
    body = cleanup_email(body, strip_url=True)
    decoded_emails.append(body)
  #make sure that the emails don't have weird white space characters, and then
  #  append them onto the file that you're writing to
  for elements in decoded_emails:
    elements = elements.strip()
    write_file.write(elements + "\n")
  write_file.close()
  #now do the tagger stuff if you need to
  if tagger_flag == "t":
    #open a temporary file to write the tagged tweets to
    temp = open("temp.txt","w")
    #create a subprocess call in order to tag from within python
    #  Note: cwd is set to the ark folder under current
    call(["./runTagger.sh", "--model",
      "model.ritter_ptb_alldata_fixed.20130723.txt",
      "../interText.txt"],cwd="./ark-tweet-nlp-0.3.2/",stdout=temp)
    temp.close()
    #remove the intermediate text for cleanup
    os.remove("interText.txt")
    #read in the tagged text file
    tweets = open("temp.txt","r")
    #create a new list for the taggedtweets
    taggedTweets = list()
    for tweet in tweets:
      #hold each of the sets of pairs
      wordTagPair = list()
      #only want the first two b/c those are all that are needed
      words, tags = tweet.split("\t")[:2]
      #get individual words and tags
      words = words.split(" ")
      tags = tags.split(" ")
      #get the length of words for iteration
      sentenceLength = len(words)
      for i in range(sentenceLength):
        #join the words and tags with an underscore if desired
        if pos_flag == "t":
          pair = tags[i]
        else:
          pair = words[i] + "_" + tags[i]
        #then add it to the list of pairs
        wordTagPair.append(pair)
      #Afterwards, join the pairs like a sentence
      taggedTweet = " ".join(wordTagPair)
      #then append it to the taggedTweets list
      taggedTweets.append(taggedTweet)
    tweets.close()
    #reattach the sentimnets to the tweets
    #for i in range(len(taggedTweets)):
    #    taggedTweets[i] = tweetSentiment[i] + "\t"+ taggedTweets[i]
    outputFile = open(output_file, "w")
    #finally, write to the final file cleaning up temp files
    for fullyTaggedTweets in taggedTweets:
      tweetWN = fullyTaggedTweets + "\n"
      outputFile.write(tweetWN)
    outputFile.close()
    #clean up the last temporary file
    os.remove("temp.txt")


if __name__ == "__main__":
  main(sys.argv)
