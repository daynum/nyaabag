# Nyaa - Smoke's index torrent fetcher

## Description
This script parses SeaSmoke's local (or [online]) anime release index (csv format). 
And uses it to help users find the best releases on nyaa.  
The script can fuzzy match the name of anime entered, so there's no need to type it exactly or completely, try it!  
You can search in both, english and japanese name of the anime.

## Python libraries used
- Pandas  
- fuzzywuzzy  
- requests  
- lxml  

## Usage
Open up your terminal/cmd and navigate to the nyaabag directory.  
Run this command first to ensure the installation of required libraries with your python.  
```
python -m pip install -r requirements.txt
```  
After that, just open a terminal/cmd window in the nyaabag directory, and run nyaabag.py file with python like this.  
```
python main.py
```  

### Credits
JuanjoSalvador's [Nyaapy](https://github.com/JuanjoSalvador/NyaaPy)
SeaSmoke's anime release [index](https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM/htmlview)