import os
import json
import csv

# Settings
JSON_DIR = "C:/Users/user/OneDrive/Desktop/pianotiles/song"
LIST_FILE = "C:/Users/user/OneDrive/Desktop/pianotiles/songLists.txt"
OUTPUT_CSV = "C:/Users/user/OneDrive/Desktop/pianotiles/songs.csv"

def main():
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        filenames = [line.strip() for line in f if line.strip()]

    # Base CSV
    Songs = [["SongName", "BaseBPM", "first", "second", "third", "firstTPS", "secondTPS", "thirdTPS","avgTPS"]]

    for name in filenames:
        json_path = os.path.join(JSON_DIR, name)

        if not os.path.exists(json_path):
            print(f"Skipped: {name} can't find JSON.")
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as jf:
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
                # Add Table
                Songs.append([name, baseBpm, first, second, third, firstTPS, secondTPS, thirdTPS, TPS])


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
