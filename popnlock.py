import mysql.connector as sql
from playsound import playsound as ps
from pytube import YouTube
import os
import time
import random

print("*" * 50,"Pop N Lock","*" * 50)

pwd = input("Please enter your MySQL password: ")
con = sql.connect(host = "localhost", user = "root", password = pwd)
cursor = con.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS pkg;")
cursor.execute("USE pkg;")

ren = True
while ren:
    print("  Menu:\n\t[1] Play your playlists\n\t[2] Create a new playlist\n\t[3] Delete a playlist\n\t[4] Add songs to existing playlist\n\t[5] Remove songs from an existing playlist\n\t[6] Exit\n")
    time.sleep(0.5)
    choice = (input("Enter your choice: "))

    if choice == "1":

        cursor.execute("SHOW TABLES;")
        pl = cursor.fetchall()

        
        pll = []
        for i in pl:
            pll.append(i[0])

        if pll == []:
            print("There are no playlists. You have to create one first.")
            time.sleep(1)
            continue
            
        for i in range(len(pl)):
            print("["+str(i+1)+"]",pl[i][0])

        plc = input("Which playlist do you wanna play: ")
        
        if plc in pll:
            cursor.execute("SELECT Name FROM {}".format(plc))
            songs = cursor.fetchall()
            if songs != []:
                sl = []
                for j in songs:
                    sn = j[0]
                    sl.append(sn)
                dn = input("Do you want to shuffle play(y/n): ")
                if dn == "y":
                    sr = random.sample(sl,len(sl))
                    for m in sr:
                        ps(m)
                elif dn == "n":
                    for m in sl:
                        ps(m)
                else:
                    print("Invalid Input ...")
            else:
                print("There are no songs in this playlist. You have to add one.")
                time.sleep(1)
                continue
        else:
            print("Enter a valid playlist name (It is case-sensitive) ....") 
            time.sleep(1)

    elif choice == "2":

        pln = input("Enter the name of the playlist: ")
        cursor.execute("SHOW TABLES;")
        pl = cursor.fetchall()

        for i in range(len(pl)):
            if pln == pl[i][0]:
                print("Playlist already exists ....")
                time.sleep(1)
                break
        else:
            cursor.execute("CREATE TABLE {}(Name VARCHAR(300));".format(pln))
            con.commit()            
            print("Playlist created")
            time.sleep(1)
            
    elif choice == "3":

        cursor.execute("SHOW TABLES;")
        pl = cursor.fetchall()
        pll = []
        for i in pl:
            pll.append(i[0])

        for p in range(len(pll)):
            print("["+str(p+1)+"]",pll[p])

        pln = input("Enter the name of the playlist: ")    

        if pln in pll:
            cursor.execute("DROP TABLE {};".format(pln))
            con.commit()
            print("Playlist deleted")
            time.sleep(1)
        else:
            print("Enter a valid playlist name (It is case-sensitive) ....")
            time.sleep(1)

    elif choice == "4":

        cursor.execute("SHOW TABLES;")
        pl = cursor.fetchall()
        
        for i in range(len(pl)):
            print("["+str(i+1)+"]",pl[i][0])

        pll = []
        for i in pl:
            pll.append(i[0])
        pln = input("Enter the name of the playlist: ")
        time.sleep(0.5)
        if pln in pll:
            while True:
                url = input("Enter the url of the song on YouTube: ")
                yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
                ad = yt.streams.filter(only_audio=True).first()
                filename = yt.title+".mp3"
                ad.download(filename = filename)
                cursor.execute("INSERT INTO {} VALUES(\"{}\");".format(pln,filename))
                con.commit()
                ch = input("Do you want to add another song(y/n): ")
                if ch == "n":
                    break 
                else:
                    pass              
        
    elif choice == "5":

        cursor.execute("SHOW TABLES;")
        pl = cursor.fetchall()
                
        for i in range(len(pl)):
            print("["+str(i+1)+"]",pl[i][0])

        pll = []
        for i in pl:
            pll.append(i[0])
        pln = input("Enter the name of the playlist: ")
        time.sleep(0.5)

        if pln in pll:
            cursor.execute("SELECT Name FROM {}".format(pln))
            plq = cursor.fetchall()

            for q in range(len(plq)):
                print("["+str(q+1)+"]",plq[q][0])

            chd = int(input("Which song do you wanna delete (Enter the song number): ")) - 1
            nme = plq[chd][0]
            cursor.execute("DELETE FROM {} WHERE Name = \"{}\"".format(pln,nme))
            con.commit()
            os.remove(nme)
            print("The song has been deleted")
            time.sleep(1)    

    elif choice == "6":
        ren =False

    else:
        print("Please enter a valid choice like 1, 2 or 3 ....")
        time.sleep(1)

print("*" * 40, "Thanks for using Pop N Lock", "*" * 40)
