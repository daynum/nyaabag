import requests
import re
from fuzzywuzzy import fuzz,process
import pandas as pd
def get_nyaa_data(name_eng,name_jap,group):
    name_eng = re.sub('\(.*?\)','', name_eng)
    name_jap = re.sub('\(.*?\)','', name_jap)
    from nyaa import Nyaa
    Nyaa=Nyaa()
    searching = Nyaa.search(keyword=group+" "+name_eng, category=1)
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


#sheet_url="https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM/edit#gid=0"
sheet_url="index_seadex.csv"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
best_release_data = pd.read_csv(url_1,header=1,index_col=[0])
print("**WELCOME TO SEADEX TO NYAA FETCHER**")
user_anime_name = input("Please enter the name of the anime you want to search: ")
print('******************************************************')
best_matches = process.extract(user_anime_name, best_release_data['Title'].tolist(), limit = 5, )
for i in range(len(best_matches)):
    print(str(i+1)+". "+best_matches[i][0])
print('******************************************************')
anime_id=int(input("Choose your anime by entering a number: "))
anime_id-=1
anime_name=best_matches[anime_id][0]

best_release_data.set_index("Title",inplace=True)
chosen_row=best_release_data.loc[best_matches[anime_id][0]]
anime_name_jap=str(chosen_row["Alternate Title"])
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
#Now we have to extract the release group name from releases list
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

for i in range(len(season_ova)):
    print(str(i+1)+". "+str(season_ova[i])+"\t"+group[i])
print('******************************************************')
final_choice=int(input("Choose the season / release group name: "))
final_choice-=1
print('******************************************************')
print("Fetching "+group[final_choice]+" release of "+str(anime_name_jap)+" / "+anime_name+" from nyaa.")

get_nyaa_data(anime_name,anime_name_jap,group[final_choice])