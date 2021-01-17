import os
import shutil
from socket import gaierror
import re
import osudb
import ast
import serializer

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
    print(osupath + '\\' + "osu!.exe")
    try:
        if os.path.isfile(osupath + '\\' + "osu!.exe"):
            print("Success: folder contain osu.exe")
            osupathcheck = False
        else:
            print("Error: Folder doesn't contain osu.exe")

    except NameError:
        print("Error: Input isn't a path or the specified path is incorrect")

while Syncing:

    #---------------------------------------------------------------------------------------------------
    # Backup needed file to osu!MapSync

    collectionDB = osupath + '\\' + 'collection.db'
    scoresDB = osupath + '\\' + 'scores.db'
    osuDBm = osupath + '\\' + 'osu!.db'
    replays = osupath + '\\' + 'Data'
    songpath = osupath + "\\Songs"

    # Write all maps link to a txt file

    BMID_list = []
    MP_list = os.listdir(songpath)

    for ID in MP_list:
        match = re.match(r"(^\d*)",ID)
        BMID_list.append(match.group(0))

    cleaning = True
    e = 0
    while cleaning:
        try:
            for idx in range(len(BMID_list)):
                i = idx
                BMID_list[idx] = int(BMID_list[idx]) #converting them to int, if not an int, then it get removed
                BMID_list[idx] = str(BMID_list[idx]) #converting back to str when done cleaning
            cleaning = False
        except:
            print("removed: ",i+e," = ",'"',BMID_list[i],'"', "from the list since it's not a valid ID")
            BMID_list.remove(BMID_list[i])
            e += 1

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
    shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),"../osu!MapSync")))
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
        else:
            print("What the fuck is wrong with you?")

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
    cmd = 'bad.exe patch "./old osu!.db/osu!.db" "./old osu!.db/osu!_update.csv" "/new osu!.db/osu!.db"'
    s = os.system(cmd)

    print("Merging scores.db")

    parse = osudb.parse_score(r"./old osu!.db/scores.db")
    with open('./old osu!.db/scoresdb.txt', 'w') as f:
        for item in parse:
            print(type(item))
            f.write("%s\n" % item)

    parse = osudb.parse_score(r"./old osu!.db/scores_update.db")
    with open('./old osu!.db/scoresdb_update.txt', 'w') as f:
        for item in parse:
            f.write("%s\n" % item)
    parsed_files = ["./old osu!.db/scoresdb.txt", "./old osu!.db/scoresdb_update.txt"]


    scores_DB_list = []
    scores_DB_list_update = []
    scoreslistname = [scores_DB_list,scores_DB_list_update]

    def organization(original_txt_name, listname):
        with open(original_txt_name, 'r') as files:
            for i, line in enumerate(files):
                if i==2:
                    BSlist = ast.literal_eval(line)
                    for Map_list_scoresDB in BSlist:    
                        listname.append(Map_list_scoresDB)
                                
        return ""

    for index_parsed, score_list in zip(parsed_files, scoreslistname):
        task = organization(index_parsed, score_list)


    maplist_DB_list = []
    map_DB_update_list = []
    BM_md5_hash = []
    BM_md5_hash_update = []


    for maplist_scores_DB_list_update in scores_DB_list_update:

        map_DB_update_list.append(maplist_scores_DB_list_update)

        for index, hash in enumerate(maplist_scores_DB_list_update):
            BM_md5_hash.append(hash)


    for maplist_scores_DB_list in scores_DB_list:

        maplist_DB_list.append(maplist_scores_DB_list)

        for index, hash in enumerate(maplist_scores_DB_list):
            BM_md5_hash_update.append(hash)

    with open("./old osu!.db/scoresdb_update.txt", 'r') as f:
        for i, line in enumerate(f):
            if i==0:
                scoreversion = line
                break
    try:
        for map, hash in enumerate(BM_md5_hash_update):
            if map >= len(maplist_DB_list):
                break
            else:
                if hash in BM_md5_hash:
                    for scores in range(len(map_DB_update_list[map][2])):
                        if map_DB_update_list[map][2][scores][4] in maplist_DB_list[map][2][scores][4]:
                            print(map, scores, "match")
                        else:
                            maplist_DB_list[map][2].append(map_DB_update_list[map][2][scores])
                            print(hash, ": score added")
                            maplist_DB_list[map][1] = maplist_DB_list[map][1] + 1
                else:
                    maplist_DB_list.append(map_DB_update_list[map])
                    print("map added")
    except IndexError:
        print("Update file might be outdated or something else happened")


    newscoredb = [int(scoreversion), len(maplist_DB_list), (maplist_DB_list)]
    with open(r'./new osu!.db/scores.db.txt', 'w') as output:
        output.write(str(newscoredb))

    serializer.serialize_scoredb_data(r'./new osu!.db/scores.db.txt')

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

    print("Prompting user about file")

    asking = True
    while asking:
        i = input("Would you like to send the updated files to your osu! folder directly?")
        if i == "Yes" or i == "Y" or i == "yes" or i == "y":
            i = input("Would you like to backup your old osu! db files? (they will be located in",osupath,")","(recommended)") #send files to osu! folder
            if i == "Yes" or i == "Y" or i == "yes" or i == "y":
                shutil.copy(collectionDB, os.path.abspath(os.path.join(os.getcwd(),osupath+"\\Backup\\collection.db")))
                shutil.copy(scoresDB, os.path.abspath(os.path.join(os.getcwd(),osupath+"\\Backup\\scores.db")))
                shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),osupath+"\\Backup\\osu!.db")))

                shutil.unpack_archive("./download osu!MapSync/r.zip", osupath + "\\data\\r\\")
                shutil.copy("./new osu!.db/osu!.db", os.path.abspath(os.path.join(os.getcwd(),osuDBm)))
                shutil.copy("./new osu!.db/scores.db", os.path.abspath(os.path.join(os.getcwd(),scoresDB)))
                shutil.copy("./new osu!.db/osu!.db", os.path.abspath(os.path.join(os.getcwd(),collectionDB)))
                asking = False
            if i == "No" or i == "N" or i == "no" or i == "n":
                shutil.unpack_archive("./download osu!MapSync/r.zip", osupath + "\\data\\r\\")
                shutil.copy("./new osu!.db/osu!.db", os.path.abspath(os.path.join(os.getcwd(),osuDBm)))
                shutil.copy("./new osu!.db/scores.db", os.path.abspath(os.path.join(os.getcwd(),scoresDB)))
                shutil.copy("./new osu!.db/osu!.db", os.path.abspath(os.path.join(os.getcwd(),collectionDB)))
                asking = False
        if i == "No" or i == "N" or i == "no" or i == "n":
            print("New files are located in './new osu!.db/'")
            asking = False

    print("Collections, scores, recently played maps and replays have been Updated\nBeatmaps haven't been updated and will need to be downloaded manually for now\nuntil i implement a downloader")
    Update = False