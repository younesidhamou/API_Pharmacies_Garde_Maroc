import requests
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Comment
import json
coordonee=[]
adresse=[]
num=[]
etat=[]
pharmacies=[]
cle=[]
for ville in open('href.txt','r'):
            print(ville)
            req=Request("https://www.annuaire-gratuit.ma"+ville.replace('\n',''), headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup=BeautifulSoup(webpage,'lxml')
            input_tag = soup.find(attrs={"style" : "font-family: Arial, sans-serif, verdana; font-size:14px;"})
            article=input_tag.findChildren("a", recursive=False)
            perm=[]
            for a in article:
                    quartier=a.find("span",attrs={"itemprop":"addressLocality"}).text
                    name=a.get('title')
                    href=a.get('href')
                    pharmacies.append([name,href,quartier])
                    perm.append([name,href,quartier])
            for k in perm:
                print(k[0])
                cle.append("AIzaSyBnN118yXQmI6PseuR6rsSRJNZCOkiNJKQ")
                req=Request("https://www.annuaire-gratuit.ma/pharmacies"+k[1], headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                soup=BeautifulSoup(webpage,'lxml')
                try:
                        num.append(soup.find(attrs={"itemprop":"telephone"}).get('href').replace("tel:",''))
                except:
                        num.append("0000000000")
                etat.append(soup.find("table",attrs={"class":"pharma_history"}).find_all("tr")[-1].find_all("td")[-1].text.replace("Garde ",""))
                add=soup.find('address')
                try:
                        adresse.append(add.text)
                except:
                        adresse.append("")
                try:
                        coordonee.append(add.find('a').get('href').replace("http://maps.google.com/maps?q=",'').replace(",",', '))
                except:
                        coordonee.append("00.00000000, 0.00000000")
df=pd.DataFrame(pharmacies)
df[3]=adresse
df[4]=coordonee
df[5]=num
df[6]=etat
df[7]=cle
df.columns=['pharmacie', 'lien', 'quartier','adresse','coordonnee','telephone','etat','cle']
out="["+df.to_json(orient='records')[1:-1].replace('},{', '},{')+"]"
output=open('data1.json', 'w')
with output as f:
    f.write(out)
