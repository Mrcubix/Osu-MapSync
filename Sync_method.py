#
#   sFTP : pysftp
#   smb
#   
#
import subprocess
import sys
from ftplib import FTP, error_perm
from socket import gaierror
import os
import shutil

def Join(Folder, method, method_conn):
    if method == "FTP":
        ftp = method_conn
        while Folder != "":
            try:
                ftp.cwd(Folder)
                return "Folder found"
            except error_perm:
                ftp.mkd(Folder)
                ftp.cwd(Folder)
                return  "A new folder has been created"
    if method == "localfile":
        while Folder != "":
            try:
                os.path.join(Folder)
                return "Folder found"
            except:
                os.mkdir(Folder)
                os.path.join(Folder)
                return  "A new folder has been created"

def promptID():
    NSID = []
    NSID.append(input("Host: "))
    NSID.append(input("Username: "))
    NSID.append(input("Password: "))
    for id in NSID:
        if id == "":
            NSID[NSID.index(id)] = None
    return NSID

def IDlog(method):
    prompt = True
    while prompt:
        NSID = promptID()
        print(method)
        if method == "SSH":
            print("importing modules...")
            try: 
                import paramiko
                from scp import SCPClient as scp
                print("scp and paramiko imported successfully")
            except ImportError:
                    promptm = True
                    while promptm:
                        i = input("scp is required to use SSH, would you like to install the package? (Require pip) Y/n: ")
                        if i == "Y" or i == "y":
                            subprocess.call([sys.executable, "-m", "pip", "install", "scp"])
                            import paramiko
                            from scp import SCPClient as scp
                            print("successfully imported scp and paramiko")
                            promptm = False
                        if i == "N" or i == "n":
                            print("exiting...")
                            exit()

            portp = True
            while portp:                
                port = input("Port: ")
                try:
                    int(port)
                    portp = False
                except:
                    print("Invalid port")

            try:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(NSID[0], port, NSID[1], NSID[2])
                scp = scp(ssh.get_transport())
                print("connected on", NSID[0], "as", NSID[1])
                return scp
            except TimeoutError:
                print("Error: Connection timed out, probably due to wrong Port or IP")
            except TypeError:
                print("Invalid character in one of the input")
            except paramiko.ssh_exception.SSHException:
                print("Invalid identifiers")
            except gaierror:
                print("Error: URL is somehow invalid or isn't an URL at all")

        if method == "FTP":
            ftp = FTP()
            port = input("port: ")
            try:
                port = int(port)
            except NameError:
                print("Error: input isn't a port")
            except ValueError:
                print("Error: input isn't a valid port")

            try:
                connect = ftp.connect(NSID[0], port)
                if connect == '220 Service ready for new user.':
                    ftp.login(NSID[1],NSID[2])
                    print("connected on", NSID[0], "as", NSID[1])
                    prompt = False
                    return ftp
                else:
                    print("Error: URL isn't associated with an FTP server")
            except gaierror:
                print("Error: URL is somehow invalid or isn't an URL at all")
            except TimeoutError:
                print("Error: Connection timed out due to wrong Port or IP")
            except error_perm:
                print("Identifiers provided invalid")
            except TypeError:
                print("Invalid character in one of the input")

def Upload_Method(method):
    path = "./osu!MapSync.zip"
    if method == "FTP":
        ftp = IDlog("FTP")
        print(Join("osu!MapSync", "FTP", ftp))
        print("Sending file to FTP server")
        with open(path,"rb") as f:
            ftp.storbinary(f"STOR {path}", f)
        print("Upload done")
        ftp.quit()
    if method == "SSH":
        scp = IDlog("SSH")
        path = input("Input folder's path where you want the data to be uploaded to: ")
        scp.put("./osu!MapSync.zip", path+"/osu!MapSync.zip")
        scp.close()
    if method == "localfile":
        path = input("Input folder's path where you want the data to be exported to: ")
        print(Join(path,"localfile",None))
        print("Sending file to",path)
        shutil.copy("./osu!MapSync.zip", path+"\osu!MapSync.zip")


def Update_Method(method):
    if method == "FTP":
        ftp = IDlog("FTP")
        ftp.cwd("osu!MapSync")
        if ftp.dir() == None:
            print("No synced data, exiting...")
            ftp.quit()
            exit()
        else:
            print("Info: Downloading Updated map data...")
            with open("./download osu!MapSync/osu!MapSync.zip","wb") as f:
                ftp.retrbinary("RETR osu!MapSync.zip", f.write)
    if method == "localfile":
        prompt = True
        while prompt:
            path = input("Input folder's path where you want the data to be imported from: ")
            print(Join(path,"localfile",None))
            try:
                print("Receiving files from",path)
                print(__file__)
                shutil.copy(path+"\osu!MapSync.zip", __file__.split('Sync_method.py', 1)[0]+"\download osu!MapSync\osu!MapSync.zip")
                prompt = False
            except:
                print("path or folder not found or OS is pepega")
    if method == "SSH":
        scp = IDlog("SSH")
        prompt = True
        while prompt:
            path = input("Input folder's path where you want the data to be downloaded from: ")
            try:
                print("Info: Downloading Updated map data...")
                scp.get(path+"/osu!MapSync.zip", __file__.split('Sync_method.py', 1)[0]+"\download osu!MapSync\osu!MapSync.zip")
                prompt = False
                scp.close()
            except:
                print("path or folder not found or OS is pepega")

def Update():
    prompt = True
    while prompt:
        print("\nMethods availables : FTP, SSH, localfile\n")
        method = input("Choose a method from the list: ")
        try:
            Update_Method(method)
            prompt = False
        except:
            print("Method not available")

def Upload():
    prompt = True
    while prompt:
        print("\nMethods availables : FTP, SSH, localfile\n")
        method = input("Choose a method from the list: ")
        try:
            Upload_Method(method)
            prompt = False
        except:
            print("Method not available")
