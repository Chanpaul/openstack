import requests
import re
import pdb
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json
pictag={"td": ('class','views-field-field-profile-picture')}

taglist=['','','','']
attrlist=['row faculty-row','']

imgdir="gatech/ce/"
url="http://ssebe.engineering.asu.edu/people/faculty-and-lecturers.html"
base="http://ssebe.engineering.asu.edu"
#commonUrl="https://www.ece.gatech.edu/faculty-staff-directory/"
urltext=requests.get(url)
#pdb.set_trace()
soup=BeautifulSoup(urltext.text,"html5lib")
scholars={}
rawInfo=soup.findAll("div",attrs={"class":"quick-bio"}) 

for ele in rawInfo:    
    #pdb.set_trace()
    info_name=ele.find("div",attrs={"class":"name"}).string
    print info_name
    if info_name:
        info_name=info_name.encode("utf8")
    img_url=ele.find("div",attrs={"class":"quick-bio-pic"}).img["src"]
    if re.compile("^http://.*").findall(img_url):
        info_img=requests.get(img_url)
    else:
        info_img=requests.get(base+img_url.replace("../","/"))
    
    info_email=ele.find("a",attrs={"href":re.compile("^mailto:[a-zA-Z0-9]+\.?[a-zA-Z0-9]*@.*\.?asu.edu")})
    if info_email:
        info_email=info_email["href"][7:].encode("utf8")
    
          
    info_titles=ele.find("p",attrs={"class":"title"}).children
    for x in info_titles:
        info_title=x.encode("utf8")
        break
    
    info_tel="None"
    info_bio=""
    #pdb.set_trace()
    contact_info=ele.find("p",attrs={"class":"contact-info"})
    if contact_info:
        for x in contact_info.children:
            info_tel=x.encode("utf8")
            break
    if ele.li.string:
        info_bio=ele.li.string.encode("utf8")     
    if info_email:
        with open(info_email+'.jpeg', 'wb') as imghandle:
            for block in info_img.iter_content(1024):
                imghandle.write(block)
    #pdb.set_trace()
        scholars[info_email]=[info_name,info_title,info_tel,info_bio,"School of Electrical and Computer Engineering"]
    
with open("ece.gatech.json",'w') as infohandle:
    json.dump(scholars,infohandle)
print "Got it!"

