"""Generate wordcloud JSON files under data/wordcloud."""

from __future__ import annotations

import json
from pathlib import Path

PALETTE = ["#2f7df6", "#7367f0", "#00a6d8", "#2aa36b", "#d7881d", "#c95757", "#3d8cff", "#8a63ff"]
BASE_DIR = Path(__file__).resolve().parent


def build_items(words: list[str], start_score: int = 160, min_score: int = 10, target_count: int = 100) -> list[dict]:
    items: list[dict] = []
    if not words:
        words = ["词条"]
    for idx in range(target_count):
        seed = words[idx % len(words)]
        turn = idx // len(words)
        name = seed if turn == 0 else f"{seed}{turn + 1}"
        score = max(min_score, start_score - idx * 2)
        color = PALETTE[idx % len(PALETTE)]
        items.append({"name": name, "score": score, "color": color})
    return items


def write_json(filename: str, category: str, name: str, words: list[str], start_score: int) -> None:
    payload = {
        "category": category,
        "name": name,
        "items": build_items(words, start_score=start_score),
    }
    path = BASE_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"generated {path.name}: {len(payload['items'])} items")


CI_WORDS = [
    "明月", "春风", "江南", "归来", "相思", "天涯", "烟雨", "兰舟", "斜阳", "长亭",
    "柳岸", "残照", "潮声", "夜雨", "玉笛", "孤鸿", "清梦", "落花", "楼台", "秋水",
]
TANG_WORDS = [
    "长安", "春风", "明月", "黄河", "故人", "青山", "万里", "白云", "江城", "边塞",
    "秋风", "归舟", "渔火", "玉关", "芳草", "胡马", "天门", "寒山", "大漠", "羌笛",
]
SONG_PEOPLE_WORDS = [
    "苏轼", "陆游", "辛弃疾", "杨万里", "范成大", "梅尧臣", "王安石", "欧阳修", "黄庭坚", "晏殊",
    "曾巩", "秦观", "周邦彦", "姜夔", "贺铸", "张耒", "陈与义", "文天祥", "朱熹", "司马光",
]
CI_PAI_WORDS = [
    "水调歌头", "念奴娇", "沁园春", "满江红", "临江仙", "西江月", "鹧鸪天", "菩萨蛮", "蝶恋花", "虞美人",
    "青玉案", "如梦令", "清平乐", "南乡子", "卜算子", "醉花阴", "定风波", "摸鱼儿", "永遇乐", "八声甘州",
    "声声慢", "木兰花", "减字木兰花", "渔家傲", "苏幕遮", "踏莎行", "浣溪沙", "采桑子", "鹊桥仙", "浪淘沙",
    "行香子", "江城子", "贺新郎", "雨霖铃", "玉楼春", "诉衷情", "点绛唇", "相见欢", "好事近", "千秋岁",
    "破阵子", "凤凰台上忆吹箫", "祝英台近", "齐天乐", "绮罗香", "兰陵王", "金缕曲", "扬州慢", "风入松", "木兰花慢",
]


if __name__ == "__main__":
    write_json("ci.json", "ci", "宋词高频词", CI_WORDS, start_score=160)
    write_json("tang.json", "tang", "唐诗高频词", TANG_WORDS, start_score=160)
    write_json("song_people.json", "song_people", "宋诗人名云", SONG_PEOPLE_WORDS, start_score=160)
    write_json("ci_pai.json", "ci_pai", "词牌名词云", CI_PAI_WORDS, start_score=180)
