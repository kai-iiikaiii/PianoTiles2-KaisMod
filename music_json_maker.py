import os
import json
import csv

# Settings
JSON_DIR = "./song"
LIST_FILE = "./songLists.txt"
OUTPUT_CSV = "./output.csv"
INPUT_CSV = "./songs.csv"

    

def main():

    output = []
    Id = 1000000
    Mid = 1000000
    with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            SongName_Id = row["SongName"]
 #           print(SongName_Id)
            Id += 1
            Mid += 1

            SongName = row["SongName"].replace('.json', '')

            def calcTPS(bpm, BaseBeats):
                TPS = (float(bpm) / float(BaseBeats)) / 60
                return round(TPS, 2)

            firstTPS = calcTPS(row["first"], row["firstBB"])
            secondTPS = calcTPS(row["second"], row["secondBB"])
            thirdTPS = calcTPS(row["third"], row["thirdBB"])


            TPS = round(((firstTPS + secondTPS + thirdTPS) / 3), 2)
            creator = (f"{TPS} TPS ({firstTPS} / {secondTPS} / {thirdTPS})") # Write TPS in the song creator field
 
            output.append([
                Id,
                Mid,
                float(row["first"]),
                float(row["firstBB"]),
                round(float(row["first"]) / float(row["firstBB"])),
                SongName,
                creator,
                "",
                "",
                ""
            ])
            Id += 1
            output.append([
                Id,
                Mid,
                float(row["second"]),
                float(row["secondBB"]),
                round(float(row["second"]) / float(row["secondBB"])),
                SongName,
                "",
                "",
                "",
                ""
            ])
            Id += 1
            output.append([
                Id,
                Mid,
                float(row["third"]),
                float(row["thirdBB"]),
                round(float(row["third"]) / float(row["thirdBB"])),
                SongName,
                "",
                "",
                "",
                ""
            ])
            Id += 97
#            output.append([ID,Mid,2,2,"",0,"",0,1,1000,"","","",50,1,1,"",Card,1,"","",ID,"","","",""])
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output)

    print(f"\n Finished: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
