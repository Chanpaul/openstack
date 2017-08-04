import requests
import re
import pdb
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json

imgdir="gatech/ce/"
url="http://cidse.engineering.asu.edu/facultyandresearch/directory/faculty/"
base="https://semte.engineering.asu.edu"
urltext=requests.get(url)
#pdb.set_trace()
soup=BeautifulSoup(urltext.text,"html5lib")
scholars={}
rawInfo=soup.findAll("a",attrs={"class":"image_icon_doc"})
#pdb.set_trace()

for ele in rawInfo:    
    #pdb.set_trace()
    info_img=requests.get(ele.img["src"])
    info_name=ele["title"].encode("utf8")
    info_personalurl=ele["href"]    
    subhtml=requests.get(ele["href"])
    subbf=BeautifulSoup(subhtml.text,"html5lib")

    info_email=subbf.find("a",attrs={"href":re.compile("mailto:.*")})
    if info_email:
        info_email=info_email["href"][7:] 
    info_title="Unknown"
    
    info_tel="unknown"
    info_bio="unknown"
    if info_email:
        with open(info_email+'.jpg', 'wb') as imghandle:
            for block in info_img.iter_content(1024):
                imghandle.write(block)
    #pdb.set_trace()
        scholars[info_email]=[info_name,info_title,info_tel,info_bio,"School of Computing, Informatics, and Decision Systems Engineering"]
    
with open("scholar.json",'w') as infohandle:
    json.dump(scholars,infohandle)
print "Got it!"

