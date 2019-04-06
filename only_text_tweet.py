import json
import os

pathdownload="crawler/downloads/"
filename = "1553850539719.json"

newfilename="extracted"+filename[:-5]+".txt"
pathnewfile="tweet-texts/"

def extract_text(pathdownload,filename,pathnewfile,newfilename):
    newf = open(pathnewfile + newfilename, 'w')

    with open(pathdownload + filename, 'r') as f:
        distros_dict = json.load(f)

    for distro in distros_dict["statuses"]:
        print(distro["text"])
        print("\n \n \n \n \n \n")
        if (os.stat(pathnewfile + newfilename).st_size == 0):
            newf.write(distro["text"])
            newf.write("\n \n")

    newf.close()


#
# for root, dirs, files in os.walk(pathdownload):
#     for filename in files:
#         print(filename)


extract_text(pathdownload,filename,pathnewfile,newfilename)

