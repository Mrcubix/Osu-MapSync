from ftplib import FTP
import os
import shutil
from socket import gaierror
import re
import osudb

FTP_HOST = '192.168.43.1'
FTP_USER = 'admin'
FTP_PASS = 'WideHard'
FTP_PORT = 1024
ftp = FTP()
Syncing = False
Update = False
Prompt = True
while Prompt:
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
    else:
        print(action,"isn't a valid command")


print(" ")
# connect to the FTP server
connecting = True
inputpip = True
while connecting:
    
    while inputpip:
        FTP_HOST = input("Enter your FTP server IP here: ")
        FTP_PORT = input("Enter your FTP serveur Port here: ")
        try:
            FTP_PORT = int(FTP_PORT)
            inputpip = False
        except NameError:
            print("Error: input isn't a port")
        except ValueError:
            print("Error: input isn't a port")

    try:
        connect = ftp.connect(FTP_HOST,FTP_PORT)
        if connect == '220 Service ready for new user.':
            ftp.login(FTP_USER,FTP_PASS)
            print("FTP: Connected as " + FTP_USER)
            connecting = False
        else:
            print("Error: URL isn't associated with an FTP server")
    except gaierror:
        print("Error: URL is somehow invalid or isn't an URL at all")
    except TimeoutError:
        print("Error: Connection timed out due to wrong Port or IP")
        inputpip = True

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

    dirlist = ftp.nlst()
    osusyncing = True
    while osusyncing:
        osusyncpath = input("Enter osu!MapSync Path: ")

        #
        # storage/6133-3734/
        #

        try:
            if any("osu!MapSync" in s for s in dirlist):
                print("Info: found osu!MapSync")
                cmd = 'adb connect ' + FTP_HOST + ':5555'
                s = os.system(cmd)
                cmd = 'adb -s ' + FTP_HOST + ':5555'' shell rm -f ' + osusyncpath + '/osu!MapSync/osu!MapSync.zip' 
                print("Info: Removing Previous version of synchronized map Data")
                s = os.system(cmd)
                ftp.cwd("osu!MapSync")
                print("Info: Uploading updated Map Data...")
                osuDB = open(temppath,"rb")
                ftp.storbinary("STOR osu!MapSync.zip", osuDB)
                osuDB.close()

                print("Success: Map Data uploaded")
                osusyncing = False
                Syncing = False

            else:
                print("Info: Creating a new folder")
                cmd = 'adb connect ' + FTP_HOST + ':5555'
                s = os.system(cmd)
                cmd = 'adb -s ' + FTP_HOST + ':5555'' shell mkdir ' + osusyncpath + 'osu!MapSync'
                print("Info: osu!MapSync folder created")
                s = os.system(cmd)
                cmd = 'adb connect ' + FTP_HOST + ':5555'
                s = os.system(cmd)
                cmd = 'adb -s ' + FTP_HOST + ':5555'' shell rm -f ' + osusyncpath + '/osu!MapSync/osu!MapSync.zip' 
                print("Info: Removing Previous version of synchronized map Data")
                s = os.system(cmd)
                ftp.cwd("osu!MapSync")

                osuDB = open(temppath,"rb")
                ftp.storbinary("STOR osu!MapSync.zip", osuDB)
                osuDB.close()

                print("Success: Map Data uploaded")
                osusyncing = False
                Syncing = False
        except NameError:
            print("Error: Input isn't a path or the specified path is incorrect")

    ftp.quit()

    backup = True
    while backup:
        delete = input("Would you like to delete the backup of osu!MapSync (osu!MapSync.zip)(Containing most of you map data)? Y/n ")
        if delete == "Y" or Yn == "y":
            shutil.copy('./osu!MapSync.zip', os.path.abspath(os.path.join(os.getcwd(),"./Backup")))
            backup = False
        elif delete == "N" or Yn == "n":
            os.remove("osu!MapSync.zip")
            backup = False
        else:
            print("What the fuck is wrong with you?")

while Update:

    #TODO list:
    #   - Parse and merge dekstop and laptop DB file
    #       ---> osu!.db Done
    #       
    #   - Backup old db file in osu folder
    #   - Merge them together and send to osu! folder

    ftp.cwd("osu!MapSync")
    
    print("Info: Downloading Updated map data...")
    with open("./download osu!MapSync/osu!MapSync.zip","wb") as f:
        ftp.retrbinary("RETR osu!MapSync.zip", f.write)

    print("Info: Extracting content...")

    shutil.unpack_archive("./download osu!MapSync/osu!MapSync.zip", "./download osu!MapSync/")
    shutil.unpack_archive("./download osu!MapSync/r.zip", osupath + "\\data\\r\\")
    shutil.copy("./download osu!MapSync/collection.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/collection_update.db")))
    shutil.copy("./download osu!MapSync/scores.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/scores_update.db")))
    shutil.copy("./download osu!MapSync/osu!.db", os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/osu!_update.db")))
    shutil.copy(collectionDB, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/collection.db")))
    shutil.copy(scoresDB, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/scores.db")))
    shutil.copy(osuDBm, os.path.abspath(os.path.join(os.getcwd(),"./old osu!.db/osu!.db")))

    cmd = 'bad.exe dump "./old osu!.db/osu!_update.db" "./old osu!.db/osu!_update.csv"'
    s = os.system(cmd)
    cmd = 'bad.exe patch "./old osu!.db/osu!.db" "./old osu!.db/osu!_update.csv" "/new osu!.db/osu!.db"'
    s = os.system(cmd)

    Update = False