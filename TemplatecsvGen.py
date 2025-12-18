import os
import json
import csv

# Settings
JSON_DIR = "./song"
LIST_FILE = "./songLists.txt"
OUTPUT_CSV = "./songs.csv"

def main():
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        filenames = [line.strip() for line in f if line.strip()]

    # Base CSV
    Songs = [["SongName", "BaseBPM", "first", "second", "third", "firstBB", "secondBB", "thirdBB", "firstTPS", "secondTPS", "thirdTPS","avgTPS"]]

    print("Start finding bpm...")
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
                first_bb = get_jsonInfo(data.get("musics", []), 0, "baseBeats")
                second_bb = get_jsonInfo(data.get("musics", []), 1, "baseBeats")
                third_bb = get_jsonInfo(data.get("musics", []), 2, "baseBeats")
                firstTPS = calcTPS(first, first_bb)
                secondTPS = calcTPS(second, second_bb)
                thirdTPS = calcTPS(third, third_bb)
                if first == 19950619:
                    print(f"nuh uh: {name}")

                TPS = round(((firstTPS + secondTPS + thirdTPS) / 3), 2)
                # Add Table
                Songs.append([name, baseBpm, first, second, third, first_bb, second_bb, third_bb, firstTPS, secondTPS, thirdTPS, TPS])


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
