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
    Id = 1186

    with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Id += 1

            def calcTPS(bpm, BaseBeats):
                TPS = (float(bpm) / float(BaseBeats)) / 60
                return round(TPS, 2)

            firstTPS = calcTPS(row["first"], row["firstBB"])
            secondTPS = calcTPS(row["second"], row["secondBB"])
            thirdTPS = calcTPS(row["third"], row["thirdBB"])


            TPS = round(((firstTPS + secondTPS + thirdTPS) / 3), 2)
            creator = (f"{TPS} TPS ({firstTPS} / {secondTPS} / {thirdTPS})")

            SongName = row["SongName"].replace('.json', '')


            output.append([Id,SongName,SongName,"","","","","","","","","","","","","","","","","","","","","","","","","",""])
            Id += 1
            output.append([Id,creator,creator,"","","","","","","","","","","","","","","","","","","","","","","","","",""])

    # output table
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output)

    print(f"\n Finished: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
