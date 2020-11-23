from ftplib import FTP
import os
import re
import ast

FTP_HOST = '192.168.43.1'
FTP_USER = 'admin'
FTP_PASS = 'WideHard'
FTP_PORT = 1024
ftp = FTP()

# connect to the FTP server
#ftp.connect('192.168.43.1',FTP_PORT)
#ftp.login(FTP_USER,FTP_PASS)

Toggle_osupath = True
while Toggle_osupath:
    Toggle = input("insert osupath? Y/n: ")
    if Toggle == 'Y' or Toggle == 'y':
        osupathcheck = True
        Toggle_osupath = False
    elif Toggle == 'N' or Toggle == 'n':
        osupathcheck = False
        Toggle_osupath = False


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

#songpath = osupath + "\\Songs"
#MP_list = os.listdir(songpath)

# D:\Program Files (x86)\osu!

import osudb

parse = osudb.parse_score(r"./old osu!.db/scores.db")
with open('./old osu!.db/output.txt', 'w') as f:
    for item in parse:
        print(type(item))
        f.write("%s\n" % item)

with open('./Backup/output.txt', 'w', encoding='utf-8') as f:
    f.write(str(parse))

parse = osudb.parse_score(r"./old osu!.db/scores_update.db")
with open('./old osu!.db/output_update.txt', 'w') as f:
    for item in parse:
        f.write("%s\n" % item)
#
parsed_files = ["./old osu!.db/output.txt", "./old osu!.db/output_update.txt"]

organized_files = []
for some_file_name in parsed_files:
    organized_files.append(some_file_name + "_organized.txt")

scores_DB_list = []
scores_DB_list_update = []
scoreslistname = [scores_DB_list,scores_DB_list_update]

def organization(original_txt_name, organized_txt_name, listname):
    with open(original_txt_name, 'r') as files:
        with open(organized_txt_name, 'w+') as f:
            for i, line in enumerate(files):
                if i==2:
                    BSlist = ast.literal_eval(line)
                    for Map_list_scoresDB in BSlist:
                        if type(Map_list_scoresDB) is list:
                            for map in Map_list_scoresDB:
                                if type(map) is list:
                                    for scores in map:
                                        f.write("%s\n" % scores)
                                else:
                                    f.write("%s\n" % map)        
                        else:    
                            f.write(Map_list_scoresDB)

                        listname.append(Map_list_scoresDB)
                            
    return ""

for index_parsed, index_organized, score_list in zip(parsed_files, organized_files, scoreslistname):
    task = organization(index_parsed, index_organized, score_list)


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

import time

print(len(maplist_DB_list))

with open("./old osu!.db/output_update.txt", 'r') as f:
    for i, line in enumerate(f):
        if i==0:
            scoreversion = line
            break

print(scoreversion)

for map, hash in enumerate(BM_md5_hash_update):
    if map >= len(maplist_DB_list):
        break
    else:
        if hash in BM_md5_hash:
            print(map)
            for scores in range(len(maplist_DB_list[map][2])):
                if map_DB_update_list[map][2][scores][4] in maplist_DB_list[map][2][scores][4]:
                    print(map, scores, "match")
                else:
                    maplist_DB_list[map][2].append(map_DB_update_list[map][2][scores])
                    print(hash, ": score added")
                    maplist_DB_list[map][1] = maplist_DB_list[map][1] + 1
                    time.sleep(0.1)
        else:
            maplist_DB_list.append(map_DB_update_list[map])
            print("map added")

print(len(maplist_DB_list))
print("list size: ",len(maplist_DB_list[1][2]))
print(scoreversion)

newscoredb = [int(scoreversion), len(maplist_DB_list), (maplist_DB_list)]
with open(r'./new osu!.db/scores.db.txt', 'w') as output:
    output.write(str(newscoredb))

newscoredb_serialize = osudb.Serialize_score(r"./new osu!.db/scores.db.txt")
with open(r'./new osu!.db/scores.db', 'w') as db:
    db.write(newscoredb_serialize)

#print(maplist_DB_list[0][2][0][4])
#print(maplist_scores_DB_list)

#------------------------------------------------------------------------------------------------------------------

#import time

#index_match_DB = []
#index_match_DB_update = []
#test = []
#test1 = []

#for maplist_scores_DB_list, maplist_scores_DB_list_update in zip(scores_DB_list, scores_DB_list_update):
    #if type(maplist_scores_DB_list) and type(maplist_scores_DB_list_update) is list:
        #for index_map_scores_DB_list, map_scores_DB_list in enumerate(maplist_scores_DB_list):
            #test.append(map_scores_DB_list)
            #for index_map_scores_DB_list_update, map_scores_DB_list_update in enumerate(maplist_scores_DB_list_update):
                #test1.append(map_scores_DB_list_update)
                #if map_scores_DB_list[index_map_scores_DB_list] = map_scores_DB_list_update[index_map_scores_DB_list_update]:
                    #index_match_DB.append(index_map_scores_DB_list)
                    #index_match_DB_update.append(index_map_scores_DB_list_update)
                    #continue
                #else:
                    #for index_for_scores_DB_list, for_scores_DB_list in enumerate(map_scores_DB_list):
                        #for index_for_scores_DB_list_update, for_scores_DB_list_update in enumerate(map_scores_DB_list_update):
                            #if maplist_scores_DB_list[4] = maplist_scores_DB_list_update[4]:
                                #pass
                            #else:

    
#print("Début de test: \n \n", test)
#print("Début de test1: \n \n", test1)

#        all = files.readlines()
#        all = str(all)
#        BM_list_scoreDB = re.match(r"\[(.*)",all)
#        f.write(BM_list_scoreDB.group(0))

#---------------------------------------------------------------------------------------------------

#BMID_list = []

#for ID in MP_list:
#    match = re.match(r"(^\d*)",ID)
#    BMID_list.append(match.group(0))

#cleaning = True
#e = 0
#while cleaning:
#    try:
#        for idx in range(len(BMID_list)):
#            i = idx
#            BMID_list[idx] = int(BMID_list[idx])
#        cleaning = False
#    except:
#        print("removed: ",i+e," = ", BMID_list[i], "from the list since it's not an integer")
#        BMID_list.remove(BMID_list[i])
#        e += 1

#print (" ")

#print("Syncing", len(BMID_list),"beatmaps from Songs folder")


#---------------------------------------------------------------------------------------------------
# Dir List FTP

#dirlist = ftp.nlst()
#print(type(dirlist))

#if any("osu!Sync" in s for s in dirlist):
#    print("found osu!Sync")

#---------------------------------------------------------------------------------------------------

#path = os.path.abspath(os.path.join(os.getcwd(),"./new osu!.db"))
#filename = path + '\\' + 'osu!.db'
#print(filename)
#print("")

#---------------------------------------------------------------------------------------------------
