import requests
import re
import pdb
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json

imgdir="gatech/ce/"
url="https://semte.engineering.asu.edu/faculty/"
base="https://semte.engineering.asu.edu"
urltext=requests.get(url)
#pdb.set_trace()
soup=BeautifulSoup(urltext.text,"html5lib")
scholars={}
rawInfo=soup.findAll("div",attrs={"class":"imgHolder height1"})
#pdb.set_trace()

for ele in rawInfo:    
    #pdb.set_trace()
    info_personalurl=ele.a["href"]
    subhtml=requests.get(ele.a["href"])
    subbf=BeautifulSoup(subhtml.text,"html5lib")

    info_name=subbf.find("meta",attrs={"property":"og:title"})["content"]
    info_name=re.compile("[a-zA-Z]*,\s[a-zA-Z]*").findall(info_name)
    if info_name:
        info_name=info_name[0].encode('utf8')
    des=subbf.find("meta",attrs={"property":"og:description"})["content"] 
    info_email=re.compile("[a-zA-Z0-9]+\.?[a-zA-Z0-9]*@asu.edu").findall(des)
    if info_email:
        info_email=info_email[0].encode("utf8") 
    info_title=des.split(" ")
    if info_title:
        info_title=info_title[0]+info_title[1]
        info_title=info_title.encode("utf8")
    else:
        info_title="Unknown"
    info_tel=re.compile("\(?\d*\)?\d+-?\d*").findall(des)
    if info_tel:
        info_tel=info_tel[0].encode("utf8")
    else:
        info_tel="unknown"

    info_img=requests.get(subbf.find("meta",attrs={"property":"og:image"})["content"])
    info_tel="None"
    info_bio="None"
    #bios=info.findAll("p")
    #for i in range(len(bios)):
    #    if i>3:
    #        info_bio=info_bio+bios[i]   
    if info_email:
        with open(info_email+'.jpg', 'wb') as imghandle:
            for block in info_img.iter_content(1024):
                imghandle.write(block)
    #pdb.set_trace()
        scholars[info_email]=[info_name,info_title,info_tel,info_bio,"School for Engineering of Matter, Transport and Energy"]
    
with open("scholar.json",'w') as infohandle:
    json.dump(scholars,infohandle)
print "Got it!"

