import requests
import re
from fuzzywuzzy import fuzz,process
import pandas as pd


def get_nyaa_data(name,group):
    name_eng = re.sub('\(.*?\)','', name)
    from nyaa import Nyaa
    Nyaa=Nyaa()
    searching = Nyaa.search(keyword=group+" "+name, category=1)
    for torrent in searching:
        print("-----------------------------------------------------------")
        print("Title: "+str(torrent.name))
        print("Size: "+str(torrent.size))
        print("Date: "+str(torrent.date)+"\tSeeders: "+str(torrent.seeders))
        print("Nyaa Link: "+str(torrent.url))
        print("Download Link: "+str(torrent.download_url))
        print("Magnet Link: "+str(torrent.magnet))
        print("-----------------------------------------------------------")
        print()

"""
Network url is commented because we are using a local copy of it
Uncomment the network url, and comment the local file name line, to use it.
"""
sheet_url="index_seadex.csv"
#sheet_url="https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM/edit#gid=0"

#changing the google sheet link to get in csv format
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

#ignoring first line of the csv to use as headers
best_release_data = pd.read_csv(url_1,header=1,index_col=[0])
print("**WELCOME TO SEADEX TO NYAA FETCHER**")
user_anime_name = input("Please enter the name of the anime you want to search: ")
print('******************************************************')

#fuzzily matching the user input to index anime titles, and fetching 5 entries each from title and  alternate title
fuzzy_result_limit=5
best_matches = process.extract(user_anime_name, best_release_data['Title'].tolist(), limit = fuzzy_result_limit, )
best_matches.extend(process.extract(user_anime_name, best_release_data['Alternate Title'].tolist(), limit = fuzzy_result_limit, ))
for i in range(len(best_matches)):
    print(str(i+1)+". "+str(best_matches[i][0]))
print('******************************************************')
anime_id=int(input("Choose your anime by entering a number: "))
anime_id-=1

#Searching with both keys, title and alternate title
#Finally getting the japanese and english name, of the anime which user picked
if 0<=anime_id<=4:
    best_release_data.set_index("Title",inplace=True)
    chosen_row=best_release_data.loc[best_matches[anime_id][0]]
    anime_name=best_matches[anime_id][0]
    anime_name_jap=str(chosen_row["Alternate Title"])
elif 5<=anime_id<=9:
    best_release_data.set_index("Alternate Title",inplace=True)
    chosen_row=best_release_data.loc[best_matches[anime_id][0]]
    anime_name=str(chosen_row["Title"])
    anime_name_jap=str(best_matches[anime_id][0])
else:
    print("Given choice does not match any anime")
#Fetching the best and alternate releases from the index of the chosen anime
#Also, cleaning the result we get. Removing special symbols, taking care of season markers, splitting up multiple groups.
releases=[]
if(str(chosen_row["Best Release"]) != 'nan'):
    temp = str(chosen_row["Best Release"]).split()
    for s in temp:
        s = re.sub('\(.*?\)','', s)
        new_string = re.sub('[^A-z0-9:\-_\+]+', '', s)
        if(new_string != ''):
            #if()
            releases.append(new_string)

if(str(chosen_row["Alternate Release"]) != 'nan'):
    temp = str(chosen_row["Alternate Release"]).split()
    for s in temp:
        s = re.sub('\(.*?\)','', s)
        new_string = re.sub('[^A-z0-9:\-_\+]+', '', s)
        if(new_string != ''):
            releases.append(new_string)

#Parsing the season number / ova and release groups, and mapping them together.
#Splitting the release groups if there are multiple mentioned with a + symbol.
#Null string is mapped to release if no season/ova is specified.
season_ova=[]
group=[]
i=0
while(i < len(releases)):
    first = str(releases[i])
    multi=[]
    if ':' in first:
        #this is either season number or ova
        second=str(releases[i+1])
        if '+' in second:
            multi=second.split('+')
            for gr in multi:
                if gr!='':
                    gr.replace('+','')
                    season_ova.append(first)
                    group.append(gr)
        else:
            season_ova.append(first)
            group.append(second)
        i+=2
    else:
        #name of the release group without season reference
        if '+' in first:
            multi=first.split('+')
            for gr in multi:
                if gr!='':
                    gr.replace('+','')
                    season_ova.append('')
                    group.append(gr)
        else:
            season_ova.append('')
            group.append(first)
        i+=1

#Displaying user a list of fetched seasons/ova/empty to release group mapping, and asking for release group choice.
for i in range(len(season_ova)):
    print(str(i+1)+". "+str(season_ova[i])+"\t"+str(group[i]))
print('******************************************************')
final_choice=int(input("Choose the season / release group name: "))
final_choice-=1
print('******************************************************')
print("Fetching "+str(group[final_choice])+" release of "+str(anime_name_jap)+" / "+str(anime_name)+" from nyaa.")

get_nyaa_data(anime_name,group[final_choice])
get_nyaa_data(anime_name_jap,group[final_choice])
input()
