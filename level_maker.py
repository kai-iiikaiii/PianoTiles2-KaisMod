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
    Id = 10000
    Mid = 1000000
    MenuOrder = 869

    with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Id += 1
            Mid += 1
            MenuOrder += 1
            TPS = float(row["avgTPS"])

            Card = ""
            if TPS < 1:
                Card = "song_tag_1" # Beginner
            elif TPS < 2:
                Card = "song_tag_2" # Very Easy
            elif TPS < 4: 
                Card = "song_tag_3" # Easy
            elif TPS < 5:
                Card = "song_tag_4" # Medium
            elif TPS < 6:
                Card = "song_tag_5" # Hard
            elif TPS < 8:
                    Card = "song_tag_6" # Difficult
            elif TPS < 10:
                Card = "song_tag_7" # Insane
            elif TPS < 12:
                Card = "song_tag_8" # Legendary
            elif TPS < 15:
                Card = "song_tag_9" # Pro
            elif TPS < 18:
                Card = "song_tag_10" # Impossible
            elif TPS < 20:
                Card = "song_tag_11" # Impossible+
            else:
                Card = "song_tag_12" # Unplayable

            output.append([Id,Mid,6,2,"",0,"","",0,1,"","","",500,2,"","",Card,1,"","",MenuOrder,"","","",""])

    # output table
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output)

    print(f"\n Finished: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
