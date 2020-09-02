import requests
from bs4 import BeautifulSoup
import json
import io


baseUrl = "https://www.uludagsozluk.com/"
sixMonthsID = 38562000
f = open("date.txt", "r+")
lines = f.read().splitlines()
last_line = lines[-1]
curID = last_line.__str__()
#lastDate = lastDateFile.read()
emptyEntryCount = 0
data = []
while emptyEntryCount < 10000:
    curID = int(curID) + 1
    curID = curID.__str__()
    url = baseUrl + "e/" + curID
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    #print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    title = ""
    if(soup.find("h1", attrs={"class": "tekentry-baslik"}) != None):
        title = soup.find("h1", attrs={"class": "tekentry-baslik"}).text
        title = title.strip()
        print("Title: " + title)
        print(curID)
        f = open("date.txt", "w")
        f.write(curID)
    else:
        emptyEntryCount += 1
        continue
    entryList = soup.find_all("li", attrs={"class": "li_capsul_entry"})
    for entry in entryList:
        Text = entry.find("div", attrs={"class": "entry-p"}).text
        Text = Text.strip()
        Text = " ".join(Text.split())

        entryOptionsDIV = entry.find("div", attrs={"class": "entry-secenekleri"})
        if(entryOptionsDIV.find("span", attrs={"class": "oylar arti_sayi color-yesil"}) != None):
            NumberOfLikes = entryOptionsDIV.find("span", attrs={"class": "oylar arti_sayi color-yesil"}).text
            NumberOfLikes = NumberOfLikes.__str__().strip()
            NumberOfLikes = " ".join(NumberOfLikes.split())
        else:
            NumberOfLikes = "0"
        if (entryOptionsDIV.find("span", attrs={"class": "oylar eksi_sayi "}) != None):
            NumberOfDislikes = entryOptionsDIV.find("span", attrs={"class": "oylar eksi_sayi "}).text
            NumberOfDislikes = NumberOfDislikes.__str__().strip()
            NumberOfDislikes = " ".join(NumberOfDislikes.split())
        else:
            NumberOfDislikes = "0"

        if(NumberOfLikes.__len__() == 0):
            NumberOfLikes = "0"
        if(NumberOfDislikes.__len__() == 0):
            NumberOfDislikes = "0"


        entryDate = entryOptionsDIV.find("span", attrs={"class": "date-u"}).text
        entryDate = entryDate.__str__().strip()
        entryDate = " ".join(entryDate.split())
        entryDate = entryDate.split(".")
        entryDate[0] = entryDate[0].split()
        entryDate = entryDate[0][1] + "." + entryDate[1] + "." + entryDate[2]

        entryAuthor = entryOptionsDIV.find("a", attrs={"class": "alt-u yazar"}).text
        entryAuthor = entryAuthor.strip()
        entryAuthor = " ".join(entryAuthor.split())

        print("yorum: " + Text)
        print("like:" + NumberOfLikes)
        print("dislike:" + NumberOfDislikes)
        print("date:" + entryDate)
        print("author:" + entryAuthor)
        entry = {}
        entry['title'] = title
        entry['author'] = entryAuthor
        entry['comment'] = Text
        entry['date'] = entryDate
        entry['like'] = NumberOfLikes
        entry['dislike'] = NumberOfDislikes
        data.append(entry)
        if(data.__len__() % 20 == 0):
            with io.open('data.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False, separators=(',',':'), sort_keys=True))