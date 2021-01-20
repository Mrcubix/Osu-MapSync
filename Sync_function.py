import osudb
import subprocess
import sys
import os
import re

def Song_ID(songpath):
    BMID_list = []
    MP_list = os.listdir(songpath)
    for ID in MP_list:
        BMID_list.append(re.match(r"(^\d*)",ID).group(0))
    for idx, ID in enumerate(BMID_list):
        if ID == "  " or ID == " " or ID == "":
            print("removed:", idx, "=", '"'+ID+'"', "from the list since it's not a valid ID" )
            BMID_list.remove(ID)
    return BMID_list

def Merge_scores(base, update):
        scDB_Base = osudb.parse_score(base)
        scDB_Update = osudb.parse_score(update)
        for map_u in scDB_Update[2]: #  [int,int,[Maps]]
            if map_u in scDB_Base[2]:
                    for score_u in map_u[2]:    #   [int, int,[scores]]
                        if score_u in scDB_Base[2][scDB_Base[2].index(map_u)][2]:
                            continue
                        else:
                            scDB_Base[2][scDB_Base[2].index(map_u)][2].append(score_u)
                            scDB_Base[2][scDB_Base[2].index(map_u)][1] += 1
                            print("Added: "+score_u+" Type: Score")
            else:
                scDB_Base[2].append(map_u)
                scDB_Base[1] += 1
                print("Added: "+map_u+" Type: Map")
        scDB_Base[0] = scDB_Update[0]
        return scDB_Base

def Merge_collection(base, update):
        files = [base, update]
        obj = {}
        added_elements = 0
        for idx, f in enumerate(files):
            parse = osudb.parse_collection(f)
            obj["collection"+str(idx)] = [parse][0]
        for idx, collection in enumerate(obj["collection1"][2]):
            if collection in obj["collection0"][2]:
                for hash in collection[2]:
                    if hash in obj["collection0"][2][idx][2]:
                        continue
                    else:
                        obj["collection0"][2][idx][2].append(hash)
                        obj["collection0"][2][idx][1] += 1
                        print("Added:",hash,"(type:Hash)","(Collection:",collection[0],")")
            else: 
                obj["collection0"][2].append(collection)
                obj["collection0"][1] += 1
                print("Added:",collection,"(type:Collection)")
        if added_elements == 0:
            print("no elements added")
        return obj["collection0"]

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
                for link in f.readlines():
                    if link not in BMID_list:
                        otp.write(link)

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

