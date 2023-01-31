from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import numpy as np
import xlsxwriter

pages = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

firstNames = []
secondNames = []
heights = []
weights = []
wins = []
losses = []
intWins = []
intLosses = []
unique_heights = []

#Each page of stats is categorized by the first letter of fighter's last name
#Data scraping is iterated through each page of fighters
for i in pages:
    website = f'http://www.ufcstats.com/statistics/fighters?char={i}&page=all'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content,features="html.parser")

    fighterFirstNames = soup.find_all('td', class_='b-statistics__table-col')[0::11] #Because there are 11 columns total in each row for fighter data,
    for i in fighterFirstNames:                                                      #11 columns must be skipped to get the desired column's data in the next row
        firstNames.append(i.text.strip())

    fighterSecondNames = soup.find_all('td', class_='b-statistics__table-col')[1::11]
    for i in fighterSecondNames:
        secondNames.append(i.text.strip())

    fighterHeights = soup.find_all('td', class_='b-statistics__table-col')[3::11]
    for i in fighterHeights:
        heights.append(i.text.strip())

    fighterWeights = soup.find_all('td', class_='b-statistics__table-col')[4::11]
    for i in fighterWeights:
        i = i.text.strip()
        j = re.sub('[ lbs.,--]','',i)
        if j != '':
            weights.append(int(j))
        else:
            weights.append(500) #Because columns cannot contain missing data among dataframe creation, blank space
                                #is converted to an impossibly high weight and the row is later deleted in line 71

    fighterWins = soup.find_all('td', class_='b-statistics__table-col')[7::11]
    for i in fighterWins:
        wins.append(i.text.strip())

    fighterLosses = soup.find_all('td', class_='b-statistics__table-col')[8::11]
    for i in fighterLosses:
        losses.append(i.text.strip())

#This loop was used to find each height to assist in making the x labels in the desired order
for i in heights:
    if i not in unique_heights:
        unique_heights.append(i)

intWins = [eval(i) for i in wins]
intLosses = [eval(i) for i in losses]

df = pd.DataFrame({"First Name":firstNames, "Second Name":secondNames,"Height":heights, "Weight":weights, "Wins":intWins, "Losses":intLosses})
df = df.loc[df["Weight"] < 265]
df = df.loc[df["Height"]!="--"] #Empty data is represented by UFCstats.com by '--'. Rows with missing data for height and/or weight are deleted
df["Win Percentage"] = df["Wins"]/(df["Wins"] + df["Losses"])
print(df)

plt.figure(figsize=(7, 7))
sns.boxplot(x='Weight', y='Height', data=df,order=['6\' 10"', '6\' 9"', '6\' 8"', '6\' 7"', '6\' 6"', '6\' 5"', 
'6\' 4"', '6\' 3"', '6\' 2"', '6\' 1"', '6\' 0"', '5\' 11"', '5\' 10"',
  '5\' 9"', '5\' 8"', '5\' 7"', '5\' 6"', '5\' 5"', '5\' 4"', '5\' 3"', 
  '5\' 2"',   '5\' 1"', '5\' 0"'])
plt.xticks(np.arange(min(df['Weight']), max(df['Weight']+5), 5.0))
plt.title("UFC Fighter Heights By Weight")
plt.xticks(rotation=45)
plt.xlabel('Weight(Lbs.)')
plt.ylabel('Height')
plt.tight_layout()
plt.grid(True)
 
plt.show()