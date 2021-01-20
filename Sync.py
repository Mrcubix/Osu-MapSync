import os
import shutil
import re
import osudb
import serializer
import subprocess
import sys

Syncing = False
Update = False
Prompt = True
while Prompt:
    print(" ")
    print("Commands availables:\n- Sync (or sync)\n- Update (or update)")
    print(" ")
    action = input("Run Command: ")

    if action == "Sync" or action == "sync":
        print(" ")
        Yn = input("Are you sure you want to Synchronize your map data? this will erase the data saved on the server with no possible recovery Y/n: ")
        if Yn == "Y" or Yn == "y":
            Prompt = False
            Syncing = True
    elif action == "Update" or action == "update":
        print(" ")
        Yn = input("Are you sure you want to Update your map data? this will erase the data saved on your hard drive with no possible recovery Y/n: ")
        if Yn == "Y" or Yn == "y":
            Prompt = False
            Update = True
    elif action == "help" or action == "Help" or action == "?":
        print("Commands availables:\n- Sync (or sync)\n- Update (or update)")
    else:
        print(action,"isn't a valid command")

print(" ")

# local file name you want to upload
path = os.path.abspath(os.path.join(os.getcwd(),"./new osu!.db"))
temppath = os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync.zip"))

osupathcheck = True
while osupathcheck:
    osupath = input("enter osu path here: ")
    print(os.path.abspath(osupath + '/osu!.exe'))
    try:
        if os.path.isfile(os.path.abspath(osupath + '/osu!.exe')):
            print("Success: folder contain osu.exe")
            osupathcheck = False
        else:
            print("Error: Folder doesn't contain osu.exe")

    except NameError:
        print("Error: Input isn't a path or the specified path is incorrect")

collectionDB = os.path.abspath(osupath + '/collection.db')
scoresDB = os.path.abspath(osupath + '/scores.db')
osuDBm = os.path.abspath(osupath + '/osu!.db')
replays = os.path.abspath(osupath + '/Data')
songpath = os.path.abspath(osupath + "/Songs")

def Song_ID():
    BMID_list = []
    MP_list = os.listdir(songpath)
    for ID in MP_list:
        BMID_list.append(re.match(r"(^\d*)",ID).group(0))
    for idx, ID in enumerate(BMID_list):
        if ID == "  " or ID == " " or ID == "":
            print("removed:", idx, "=", '"'+ID+'"', "from the list since it's not a valid ID" )
            BMID_list.remove(ID)
    return BMID_list

while Syncing:

    #---------------------------------------------------------------------------------------------------
    # Backup needed file to osu!MapSync
    #---------------------------------------------------------------------------------------------------

    # Write all maps link to a txt file

    BMID_list = Song_ID()

    print (" ")

    # Write all the map links in a txt file

    print("Syncing", len(BMID_list),"beatmaps from Songs folder")
    with open('Songs.txt', 'w') as file:
        for maps in BMID_list:
            file.write("https://osu.ppy.sh/beatmapsets/"+maps+"\n")

    # Zip all replays for simplicity sake

    print("Info: Zipping replays...")
    shutil.make_archive('r', 'zip', replays + '\\r')

    # Move all files to osu!MapSync
    shutil.copy(collectionDB, os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync")))
    shutil.copy(scoresDB, os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync")))
    shutil.copy('./r.zip', os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync")))
    os.remove("r.zip")
    shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync")))
    shutil.copy('./Songs.txt', os.path.abspath(os.path.join(os.getcwd(),"./osu!MapSync")))
    os.remove("Songs.txt")


    # Zip them all together
    shutil.make_archive('osu!MapSync', 'zip', './osu!MapSync')

    #---------------------------------------------------------------------------------------------------

    #
    # TBA: Dropbox support
    #

    import Sync_method as Sm
    Sm.Upload()

    backup = True
    while backup:
        delete = input("Would you like to delete the backup of osu!MapSync (osu!MapSync.zip)(Containing most of you map data)? Y/n ")
        if delete == "Y" or delete == "y":
            shutil.copy('./osu!MapSync.zip', os.path.abspath(os.path.join(os.getcwd(),"./Backup")))
            backup = False
        elif delete == "N" or delete == "n":
            os.remove("osu!MapSync.zip")
            backup = False

    input("Sync Successful, press enter to quit")

    Syncing = False

while Update:

    import Sync_method as Sm
    Sm.Update()
    
    print("Info: Extracting content...")

    shutil.unpack_archive("./download osu!MapSync/osu!MapSync.zip", "./download osu!MapSync/")
    shutil.copy("./download osu!MapSync/collection.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/collection_update.db")))
    shutil.copy("./download osu!MapSync/scores.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/scores_update.db")))
    shutil.copy("./download osu!MapSync/osu!.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/osu!_update.db")))
    shutil.copy(collectionDB, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/collection.db")))
    shutil.copy(scoresDB, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/scores.db")))
    shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/osu!.db")))

    print("patching osu!.db...")

    cmd = 'bad.exe dump "./old osu!.db/osu!_update.db" "./old osu!.db/osu!_update.csv"'
    s = os.system(cmd)
    cmd = 'bad.exe patch "./old osu!.db/osu!.db" "./old osu!.db/osu!_update.csv" "./new osu!.db/osu!.db"'
    s = os.system(cmd)

    print("Merging scores.db")

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

    serializer.serialize_scoredb_data(Merge_scores("./old osu!.db/scores.db","./old osu!.db/scores_update.db"))

    print("Merging collection.db")

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

    collection_output = Merge_collection("./old osu!.db/collection.db", "./old osu!.db/collection_update.db")
    serializer.serialize_collection_data(collection_output)

    print("Prompting user about unsynced maps...")

    def Download_Map(old_songs):  
        print("importing modules...")
        try: 
            import browser_cookie3
            import requests
            print("successfully imported browser_cookie3 and requests")
        except ImportError:
            promptm = True
            while promptm:
                i = input("browser_cookie3 and requests are required to download maps from this program, would you like to install these packages? (Require pip) Y/n: ")
                if i == "Y" or i == "y":
                    subprocess.call([sys.executable, "-m", "pip", "install", "browser_cookie3"])
                    subprocess.call([sys.executable, "-m", "pip", "install", "requests"])
                    import browser_cookie3
                    import requests
                    print("successfully imported browser_cookie3 and requests")
                    promptm = False
                if i == "N" or i == "n":
                    print("exiting...")
                    exit()

        BMID_list = Song_ID()
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
                with requests.get(link.strip("\n")+"/download", stream=True, cookies=cj, headers=headers) as r:
                    if r.status_code == 200:
                        try:
                            id = re.sub("[^0-9]", "", link)
                            with open(os.path.abspath(osupath+"/Songs/"+id+".osz"), "wb") as otp:
                                otp.write(r.content)
                        except:
                            print("You either aren't connected on osu!'s website or you're limited by the API, in which case you now have to wait 1h and then try again.")

    asking = True
    while asking:
        i = input("Would you like to download unsynced map now? (You need to log into your account before you attempt to download maps) Y/n ")
        if i == "Yes" or i == "yes" or i == "Y" or i == "y":
            print("Downloading unsynced maps now...")
            Download_Map("./download osu!mapSync/Songs.txt")
            asking = False
        if i == "No" or i == "no" or i == "N" or i == "n":
            print("Unsorted map links list in ./download osu!MapSync/Songs.txt")
            asking = False
        
    print("Prompting user about file")

    asking = True
    while asking:
        i = input("Would you like to send the updated files to your osu! folder directly? Y/n ")
        if i == "Yes" or i == "Y" or i == "yes" or i == "y":
            i = input("Would you like to backup your old osu! db files? (they will be located in "+os.path.abspath(osupath+"/Backup")+") (recommended) Y/n ") #send files to osu! folder
            if i == "Yes" or i == "Y" or i == "yes" or i == "y":
                shutil.copy(collectionDB, os.path.abspath(os.path.join(os.getcwd(),osupath+"/Backup/collection.db")))
                shutil.copy(scoresDB, os.path.abspath(os.path.join(os.getcwd(),osupath+"/Backup/scores.db")))
                shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),osupath+"/Backup/osu!.db")))
            if i == "No" or i == "N" or i == "no" or i == "n" or i == "Yes" or i == "Y" or i == "yes" or i == "y":
                print("Extracting replays...")
                shutil.unpack_archive("./download osu!MapSync/r.zip", os.path.abspath(osupath + "/data/r/"))
                print("Moving DB files...")
                shutil.copy("./new osu!.db/osu!.db", os.path.abspath(os.path.join(os.getcwd(),osuDBm)))
                shutil.copy("./new osu!.db/scores.db", os.path.abspath(os.path.join(os.getcwd(),scoresDB)))
                shutil.copy("./new osu!.db/collection.db", os.path.abspath(os.path.join(os.getcwd(),collectionDB)))
                asking = False
        if i == "No" or i == "N" or i == "no" or i == "n":
            print("New files are located in './new osu!.db/'")
            asking = False

    print("Collections, scores, recently played maps and replays have been Updated.\nMaps may have been updated or not depending on user's choice")
    Update = False