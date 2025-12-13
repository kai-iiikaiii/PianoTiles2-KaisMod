import os

JSON_DIR = "C:/Users/user/OneDrive/Desktop/pianotiles/song"

def main():
    for filename in os.listdir(JSON_DIR):

        if "," in filename:
            new_filename = filename.replace(",", ".")
            old_path = os.path.join(JSON_DIR, filename)
            new_path = os.path.join(JSON_DIR, new_filename)

            # ファイル名を変更
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")

if __name__ == "__main__":
    main()
