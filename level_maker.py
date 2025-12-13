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
    # Id,Mid,Type,Lock,NeedLv,NeedGold,NeedRV,NeedDiamond,Musiclevel,RewarID,LocalMusicVer,Recommend,MusicCard,FavoriteRate,Playmark,Stylelabel,Fallingrate,TID,,GoldenSong,MusicTime,HomeOrder,VipMusicVersion,ProduceId,card_selection,FeatureDateRange

    Songs = [["Id","Mid","Type","Lock","NeedLv","NeedGold","NeedRV","NeedDiamond","Musiclevel","RewarID","LocalMusicVer","Recommend","MusicCard","FavoriteRate","Playmark","Stylelabel","Fallingrate","TID","","GoldenSong","MusicTime","HomeOrder","VipMusicVersion","ProduceId","card_selection","FeatureDateRange"],
            ["序号","唯一标识","歌曲类型:1=等级 2=购买 3=竞技场 10=班级歌曲 15=FB 16=流行","解锁方式 1等级 2金币 13钻石 14VIP 15FB 16视频 17等级歌音乐钥匙 18音乐钥匙 19内购解锁 22专辑解锁","所需等级","解锁需花费金币","Need to watch RV in hybrid unlock","解锁需要钻石数","X=（歌曲速度-60）/40","关卡100X 购买200X","判断是否为最新歌曲","推荐歌曲","对应头部卡片","热门指数","玩法备注：1黑块2长条3双黑4狂戳5滑块6爆裂块","风格备注：1民谣 2奏鸣曲 3练习曲 4艺术歌曲 5夜曲 6进行曲 7舞曲 8探戈歌曲 9钢琴小品 10交响曲 11变奏曲 12小奏鸣曲 13小夜曲 14回旋曲 15拉格泰姆 16歌剧序曲 17创意曲 18幽默曲 19组曲 20未知 21即兴曲 22管弦乐曲 23协奏曲 24狂想曲 25赋格 26前奏曲 27歌剧选段 28浪漫曲 29重奏曲 30大提琴组曲 31小佐达坎 32中国乐曲 33沉思曲 34安魂曲 35托卡塔 36梦幻曲 37间奏曲 38宗教歌曲 39康塔塔 40帕蒂塔 41随想曲 42沉重 43急促 44欢快 45活泼 46抒情 47中性 48忧伤 49明亮 50热烈 51清新","备注：X表示试玩片段降速的百分比""，0表示试玩片段不降速","","难度分档1：X<=300，2：300<X<=360，3：X>360","首页歌曲推荐标记（1 有效）","歌曲生效时间戳","Home页排序","VIP歌曲期数","商品id","内购歌曲卡",""]]
    ID = 0
    Mid = 100000

    for name in filenames:
        json_path = os.path.join(JSON_DIR, name)

        if not os.path.exists(json_path):
            print(f"Skipped: {name} can't find JSON.")
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as jf:
                ID += 1
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
                else:
                    Card = "song_tag_11" # Unplayable


                baseBeats = get_jsonInfo(data.get("musics", []), 0, "baseBeats")
                MusicName = name.replace(".json", "")

                creator = (f"{TPS} TPS ({firstTPS} / {secondTPS} / {thirdTPS})") # Write TPS in the song creator field
                # Add Table
                Songs.append([ID,Mid,2,2,"",0,"",0,1,1000,"","","",50,1,1,"",Card,1,"","",ID,"","","",""])


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
