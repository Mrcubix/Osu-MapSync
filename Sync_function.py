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
    for map_u in scDB_Update[2]:
        for idx, map_b in enumerate(scDB_Base[2]):
            if map_u[0] in map_b:
                for scores_u in map_u[2]:
                    if not scores_u in map_b[2]:
                        scDB_Base[2][idx][2].append(scores_u)
                        scDB_Base[2][idx][1] += 1
                        print("Added: "+str(scores_u)+" Type: Scores")
    listmap = []
    [listmap.append(map_b[0]) for map_b in scDB_Base[2]]
    for map_u in scDB_Update[2]:
        if not map_u[0] in listmap:
            scDB_Base[2].append(map_u)
            scDB_Base[1] += 1
            print("Added: "+str(map_u[0])+" Type: Maps")
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
        promptm = True
        while promptm:
            i = input("Would you like to download video on all maps when possible? Y/n : ")
            if i == "Y" or i == "y":
                option = ""
                promptm = False
            if i == "N" or i == "n":
                option = "?noVideo=1"
                promptm = False
        BMID_list = Song_ID(songpath)
        for id in BMID_list:
            BMID_list[BMID_list.index(id)] = "https://osu.ppy.sh/beatmapsets/"+id+"\n"

        cj = browser_cookie3.load()
        print("Info: Comparing map in osu!/Songs VS updated data" + "\n")
        with open(old_songs, "r") as f:
            with open("./download osu!mapSync/NewSongs.txt", "w") as otp:
                [otp.write(link) for link in f.readlines() if link not in BMID_list]

        os.remove(old_songs)

        with open("./download osu!mapSync/NewSongs.txt", "r") as f:
            data = [i.strip("\n") for i in f]
            for idx, link in enumerate(data):            
                print("Info: Downloading", link)
                headers = {"referer": link}
                with requests.get(link) as r:
                    t = BS(r.text, 'html.parser').title.text.split("·")[0]
                    sign = ['*', '"', '/', '\\', ':', ';', '|', '?', '<', '>']
                    for s in sign:
                        t = t.replace(s,"_")
                with requests.get(link+"/download"+option, stream=True, cookies=cj, headers=headers) as r:
                    if r.status_code == 200:
                        try:
                            id = re.sub("[^0-9]", "", link)
                            with open(os.path.abspath(osupath+"/Songs/"+id+" "+t+".osz"), "wb") as otp:
                                otp.write(r.content)
                            print("Success: Done downloading "+t+" "+str(idx+1)+"/"+ str(len(data)) + "\n")
                            continue
                        except:
                            print("You either aren't connected on osu!'s website or you're limited by the API, in which case you now have to wait 1h and then try again.")
                    if r.status_code == 404:
                        with requests.get(link+"/download", stream=True, cookies=cj, headers=headers) as rn:
                            try:
                                id = re.sub("[^0-9]", "", link)
                                with open(os.path.abspath(osupath+"/Songs/"+id+" "+t+".osz"), "wb") as otp:
                                    otp.write(rn.content)
                                print("Success: Done downloading "+t+" "+str(idx+1)+"/"+ str(len(data)) + "\n")
                                continue
                            except:
                                print("You either aren't connected on osu!'s website or you're limited by the API, in which case you now have to wait 1h and then try again.")