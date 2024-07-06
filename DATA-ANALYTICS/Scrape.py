from bs4 import BeautifulSoup
import requests
import csv
import re

url="https://www.imdb.com/chart/top/"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=url, headers=headers) 
soup = BeautifulSoup(r.content, 'html5lib') 

movies=[]

table=soup.find_all("li",class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent")

def returnpairs(string):
    
    matches = re.findall(r'[\d\.]+[a-zA-Z]?', string)
    rating = matches[0]  
    votes = matches[1]
    return (rating,votes)

for item in table:
    
    title=item.find('h3',class_="ipc-title__text").text
    title = re.sub(r'^\d+\.\s*', '', title)
    
   
    temp=item.find_all('span',class_="sc-b189961a-8 kLaxqf cli-title-metadata-item")
    year = temp[0].text.strip()  # Extract year
    dur = temp[1].text.strip()   # Extract duration
    censor=temp[2].text.strip()
    rv=item.find('span',class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text
    ratings,votes=returnpairs(rv)
   
    movies.append({"Title":title,"Year":year,"RunTime":dur,"Censor":censor,"UserRatings":ratings,"Votes":votes})
    
filename="IMBD_DETAILS.csv"
fields = ['Title', 'Year', 'RunTime', 'Censor','UserRatings','Votes']
with open(filename, 'w') as csvfile:
    
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    
    writer.writeheader()

    
    writer.writerows(movies)






