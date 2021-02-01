import osudb
import subprocess
import sys
import os
import re

def Song_ID(songpath):
    BMID_list = []
    MP_list = os.listdir(songpath)
    [BMID_list.append(re.match(r"(^\d*)",ID).group(0)) for ID in MP_list if re.match(r"(^\d*)",ID).group(0).isdigit()]
    return BMID_list

def Merge_scores(base, update):
        scDB_Base = osudb.parse_score(base)
        scDB_Update = osudb.parse_score(update)
        for i in range(0, len(scDB_Update)):
            found = False
            for bscores in scDB_Base[2]:
                if scDB_Update[2][i][0] in bscores:
                    found = True
                    oldlen = scDB_Base[2][scDB_Base[2].index(bscores)][1]
                    scDB_Base[2][scDB_Base[2].index(bscores)][2].extend(score for score in scDB_Update[2][i][2] if score not in scDB_Base[2][scDB_Base[2].index(bscores)][2])
                    scDB_Base[2][scDB_Base[2].index(bscores)][1] = len(scDB_Base[2][scDB_Base[2].index(bscores)][2])
                    inta = -(int(scDB_Base[2][scDB_Base[2].index(bscores)][1])-int(oldlen))
                    if inta < 0:
                        print("Added: "+str(scDB_Base[2][scDB_Base[2].index(bscores)][2][inta:][4])+" Type: Map")
            if not found:
                scDB_Base[2].append(scDB_Update[2][i])
                scDB_Base[1] += 1
                print("Added: "+str(scDB_Update[2][i])+" Type: Map")
        return scDB_Base

def Merge_collection(base, update):
        CDB_Base = osudb.parse_collection(base)
        CDB_Update = osudb.parse_collection(update)
        for i in range(0,len(CDB_Update[2])):
            found = False
            for bcollection in CDB_Base[2]:
                if CDB_Update[2][i][0] in bcollection:
                    found = True
                    CDB_Base[2][CDB_Base[2].index(bcollection)][2] = list(set(CDB_Base[2][CDB_Base[2].index(bcollection)][2]) | set(CDB_Update[2][i][2]))
                    CDB_Base[2][CDB_Base[2].index(bcollection)][1] = len(CDB_Base[2][CDB_Base[2].index(bcollection)][2])
            if not found: 
                CDB_Base[2].append(CDB_Update[2][i])
                CDB_Base[1] += 1
                print("Added:",CDB_Update[2][i],"(type:Collection)")
        return CDB_Base

def Download_Map(old_songs, songpath, osupath):  
        print("importing modules...")
        try: 
            import browser_cookie3
            import requests
            from bs4 import BeautifulSoup as BS
            print("successfully imported browser_cookie3, requests and bs4")
        except ImportError:
            promptm = True
            while promptm:
                i = input("browser_cookie3, requests and bs4 are required to download maps from this program, would you like to install these packages? (Require pip) Y/n: ")
                if i == "Y" or i == "y":
                    subprocess.call([sys.executable, "-m", "pip", "install", "browser_cookie3"])
                    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
                    subprocess.call([sys.executable, "-m", "pip", "install", "bs4"])
                    import browser_cookie3
                    import requests
                    from bs4 import BeautifulSoup as BS
                    print("successfully imported browser_cookie3, requests and bs4")
                    promptm = False
                if i == "N" or i == "n":
                    print("exiting...")
                    exit()

        BMID_list = Song_ID(songpath)
        for id in BMID_list:
            BMID_list[BMID_list.index(id)] = "https://osu.ppy.sh/beatmapsets/"+id+"\n"

        cj = browser_cookie3.load()
        print("Comparing map in osu!/Songs VS updated data")
        with open(old_songs, "r") as f:
            with open("./download osu!mapSync/NewSongs.txt", "w") as otp:
                [otp.write(link) for link in f.readlines() if link not in BMID_list]

        os.remove(old_songs)

        with open("./download osu!mapSync/NewSongs.txt", "r") as f:
            for link in f:            
                print("Downloading", link.strip("\n"))
                headers = {"referer": link.strip("\n")}
                with requests.get(link.strip("\n")) as r:
                    t = BS(r.text, 'html.parser').title.text.split("·")[0]
                with requests.get(link.strip("\n")+"/download", stream=True, cookies=cj, headers=headers) as r:
                    if r.status_code == 200:
                        try:
                            id = re.sub("[^0-9]", "", link)
                            with open(os.path.abspath(osupath+"/Songs/"+id+" "+t+".osz"), "wb") as otp:
                                otp.write(r.content)
                        except:
                            print("You either aren't connected on osu!'s website or you're limited by the API, in which case you now have to wait 1h and then try again.")

