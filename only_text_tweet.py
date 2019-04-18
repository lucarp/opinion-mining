import json
import os
import re
import emoji


def extract_text(pathdownload,filename,pathnewfile,newfilename):
    newf = open(pathnewfile + newfilename, 'w')

    with open(pathdownload + filename, 'r') as f:
        distros_dict = json.load(f)

    for distro in distros_dict["statuses"]:
        print(len(distro["text"]))

        if (os.stat(pathnewfile + newfilename).st_size == 0):

            tweet = distro["text"]
            tweet = re.sub("RT", "", tweet)
            tweet = re.sub("\n","", tweet)
            tweet = emoji.demojize(tweet) #Convert emojis to text for sentiment analysis purposes
            newf.write(tweet)
            newf.write("\n \n")

    newf.close()

pathdownload="crawler/downloads/"
pathnewfile="tweet-texts/"


# for root, dirs, files in os.walk(pathdownload):
#     for filename in files:
#         print(filename)
#         newfilename = filename[:-5] + ".txt"
#         extract_text(pathdownload,filename,pathnewfile,newfilename)


filename = "1553850539719.json"

newfilename=filename[:-5]+".txt"

extract_text(pathdownload,filename,pathnewfile,newfilename)

