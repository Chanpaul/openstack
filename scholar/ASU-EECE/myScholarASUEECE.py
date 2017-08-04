import requests
import re
import pdb
#from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json
pictag={"td": ('class','views-field-field-profile-picture')}

taglist=['','','','']
attrlist=['row faculty-row','']

#urllist=['','']

#for url in urllist:
#url="https://www.ece.gatech.edu/faculty-staff-directory?field_group_filter_value=1"
imgdir="gatech/ce/"
url="http://ecee.engineering.asu.edu/faculty-by-research-area/"
base="http://ecee.engineering.asu.edu"
#commonUrl="https://www.ece.gatech.edu/faculty-staff-directory/"
urltext=requests.get(url)
#pdb.set_trace()
soup=BeautifulSoup(urltext.text,"html5lib")
scholars={}
rawInfo=soup.findAll("span",attrs={"style":"color: #808080;"})
#rawInfo=soup.findAll('span',attrs={"href":re.compile("http://ecee.engineering.asu.edu/people/.+")})
#pdb.set_trace()

for ele in rawInfo:    
    #pdb.set_trace()
    info_personalurl=ele.a["href"]
    
    info_name=ele.a.string.encode('utf8')
    print info_name
    subhtml=requests.get(ele.a["href"])
    subbf=BeautifulSoup(subhtml.text,"html5lib")
    
    info=subbf.find("div",attrs={"id":"main-content"})   
    if info: 
        if re.compile("^http://.*").findall(info.img["src"]):
            info_img=requests.get(info.img["src"]) 
        else:
            info_img=requests.get(base+info.img["src"])
        info_email=""
        info_tel="None"
        temp=info.p.children
        for x in temp:
            info_title=x.encode("utf8")
            break
    #info_title=info.p.a.previous_sibling.previous_sibling.previous_sibling.encode("utf8")
    
        info_email_tag=info.find("a",attrs={"href":re.compile("^mailto:[a-zA-Z0-9]+\.?[a-zA-Z0-9]*@.*\.?asu.edu")})

        if info_email_tag:
            info_email=info_email_tag["href"][7:].encode("utf8")
        #info_tel=info_email_tag.next_sibling.next_sibling.encode("utf8")[1:]
    
    #pdb.set_trace()
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
            scholars[info_email]=[info_name,info_title,info_tel,info_bio,"School of Electrical and Computer Engineering"]
    
with open("eecs.asu.json",'w') as infohandle:
    json.dump(scholars,infohandle)
print "Got it!"

