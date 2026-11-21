"""爱奇艺 API 示例（iQIYI API in Python）。

  python main.py search 纪录片 --out videos.csv      # 按关键词搜视频 / search videos
  python main.py video "<视频链接>" --out video.json # 视频详情 / video detail
  python main.py album 苍兰诀 --out album.json       # 按剧名查专辑 / series by title
"""
import argparse

from everyinfra import fetch, report

SORTS = ["relevance", "newest", "popular"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜视频 / search videos by keyword")
    s.add_argument("keyword")
    s.add_argument("--sort", choices=SORTS, help="排序 / sort order")
    v = sub.add_parser("video", help="视频详情 / one video")
    v.add_argument("url")
    al = sub.add_parser("album", help="按剧名查专辑 / look up a series by title")
    al.add_argument("keyword")
    for x in (s, v, al):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "video":
        rows, charged = fetch("video", {"url": a.url})
    else:
        rows, charged = fetch("album", {"keyword": a.keyword})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
