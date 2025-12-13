import os
import json
import csv

# Settings
JSON_DIR = "C:/Users/user/OneDrive/Desktop/pianotiles/song"
LIST_FILE = "C:/Users/user/OneDrive/Desktop/pianotiles/songLists.txt"
OUTPUT_CSV = "C:/Users/user/OneDrive/Desktop/pianotiles/output.csv"

def main():
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        filenames = [line.strip() for line in f if line.strip()]

    # Base CSV
    Songs = [["","TID","English","Arabic","Chinese Simplified","Chinese Traditional","Dutch","Filipino","Finnish","French","German","Hindi","Indonesian","Italian","Korean","Japanese","Malay","Norwegian","Polish","Portuguese","Portuguese Brazil","Russian","Spanish","Swedish","Thai","Turkish (old)","Turkish","Vietnamese"],
            ["","","en","ar","zh-CN","zh-TW","nl","fil","fi","fr","de","hi","id","it","ko","ja","ms","no","pl","pt","pt","ru","es","sv","th","tr","tr","vi"]]
    Mid = 0

    for name in filenames:
        json_path = os.path.join(JSON_DIR, name)

        if not os.path.exists(json_path):
            print(f"Skipped: {name} can't find JSON.")
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as jf:
                Mid += 1
                data = json.load(jf)
                baseBpm = data.get("baseBpm", 0)

                def get_jsonInfo(musics, index, element):
                    if len(musics) > index and isinstance(musics[index], dict):
                        return musics[index].get(element, baseBpm)
                    return baseBpm
                def calcTPS(bpm, BaseBeats):
                    TPS = (bpm / BaseBeats) / 60
                    return round(TPS, 2)

                first = get_jsonInfo(data.get("musics", []), 0, "bpm")
                second = get_jsonInfo(data.get("musics", []), 1, "bpm")
                third = get_jsonInfo(data.get("musics", []), 2, "bpm")
                firstTPS = calcTPS(first, get_jsonInfo(data.get("musics", []), 0, "baseBeats"))
                secondTPS = calcTPS(second, get_jsonInfo(data.get("musics", []), 0, "baseBeats"))
                thirdTPS = calcTPS(third, get_jsonInfo(data.get("musics", []), 0, "baseBeats"))
                
                TPS = round(((firstTPS + secondTPS + thirdTPS) / 3), 2)

                baseBeats = get_jsonInfo(data.get("musics", []), 0, "baseBeats")
                MusicName = name.replace(".json", "")

                creator = (f"{TPS} TPS ({firstTPS} / {secondTPS} / {thirdTPS})") # Write TPS in the song creator field
                # Add Table
                Songs.append([Mid,MusicName,MusicName,"","","","","","","","","","","","","","","","","","","","","","","","",""])

                Mid += 1
                Songs.append([Mid,creator,creator,"","","","","","","","","","","","","","","","","","","","","","","","",""])

        except json.JSONDecodeError:
            print(f"Error: {name} is invalid JSON.")
            Songs.append([f"{name} (BROKEN)", 0, 0, 0, 0])
        except Exception as e:
            print(f"Error: {name} unknown error. → {e}")
            Songs.append([f"{name} (BROKEN)", 0, 0, 0, 0])

    # output table
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(Songs)

    print(f"\n Finished: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
