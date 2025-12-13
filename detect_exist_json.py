import os

# 設定
JSON_DIR = "C:/Users/user/OneDrive/Desktop/pianotiles/song"
LIST_FILE = "C:/Users/user/OneDrive/Desktop/pianotiles/ULTIMATESONGS.txt"

def main():
    # 読み込み
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        filenames = [line.strip() for line in f if line.strip()]

    # 存在チェック
    valid_files = []
    for name in filenames:
        json_path = os.path.join(JSON_DIR, name)
        if os.path.exists(json_path):
            valid_files.append(name)

    # 上書き保存
    with open(LIST_FILE, "w", encoding="utf-8") as f:
        for name in valid_files:
            f.write(name + "\n")

    print(f"{len(valid_files)} 件のファイルを残しました。")

if __name__ == "__main__":
    main()
