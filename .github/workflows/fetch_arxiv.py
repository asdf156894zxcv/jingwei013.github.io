#!/usr/bin/env python3
"""从 ArXiv 获取具身导航相关最新论文 - 日更版 v2.0"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import re
from datetime import datetime, timedelta

# 前沿方向关键词 - 2026版
QUERIES = [
    # 核心方向
    "vision+language+navigation",
    "embodied+navigation",
    "object+goal+navigation",
    # 世界模型方向（WMA/WMNav）
    "world+model+robot+navigation",
    "WMNav+navigation",
    "embodied+world+model",
    # VLA方向
    "VLA+robot+navigation",
    "vision+language+action+navigation",
    "mobility+VLA",
    # LLM赋能导航
    "LLM+embodied+navigation",
    "NavGPT+navigation",
    # 零样本/开放词汇
    "zero+shot+object+navigation",
    "open+vocabulary+navigation",
    # 3D记忆与场景理解
    "3D+scene+memory+navigation",
    "semantic+scene+graph+navigation",
]

def fetch_papers_for_query(query, max_results=5):
    url = (
        f"https://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&start=0&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Jingwei013-Bot"})
        response = urllib.request.urlopen(req, timeout=30)
        content = response.read().decode("utf-8")
        root = ET.fromstring(content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            pub_el = entry.find("atom:published", ns)
            id_el = entry.find("atom:id", ns)
            abs_el = entry.find("atom:summary", ns)
            if title_el is None or pub_el is None or id_el is None:
                continue
            paper_id = id_el.text.split("/")[-1]
            papers.append({
                "title": title_el.text.replace("\n", " ").strip(),
                "date": pub_el.text[:10],
                "id": paper_id,
                "abstract": (abs_el.text or "").replace("\n", " ").strip()[:200] if abs_el is not None else "",
                "url": f"https://arxiv.org/abs/{paper_id}",
            })
        return papers
    except Exception as e:
        print(f"  [ERROR] 查询 '{query[:30]}' 失败: {e}")
        return []

def deduplicate(papers):
    seen = set()
    result = []
    for p in papers:
        if p["id"] not in seen:
            seen.add(p["id"])
            result.append(p)
    return result

def fetch_all_papers():
    print(f"[ArXiv日更] 开始抓取 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_papers = []
    for q in QUERIES:
        papers = fetch_papers_for_query(q, max_results=3)
        all_papers.extend(papers)
        print(f"  [OK] '{q[:40]}' → {len(papers)} 篇")

    all_papers = deduplicate(all_papers)
    # 按日期倒序
    all_papers.sort(key=lambda p: p["date"], reverse=True)

    cutoff = datetime.now() - timedelta(days=1)
    today_papers = [
        p for p in all_papers
        if datetime.strptime(p["date"], "%Y-%m-%d") >= cutoff
    ]

    print(f"\n[ArXiv日更] 总计去重 {len(all_papers)} 篇，今日新增 {len(today_papers)} 篇")

    if today_papers:
        print(f"\n🔥 今日新论文：")
        for p in today_papers[:10]:
            print(f"  [{p['date']}] {p['title'][:80]}")
            print(f"    → {p['url']}")
    else:
        print("[ArXiv日更] 今日暂无新论文")

    # 写入 JSON 供网站读取
    output_path = os.path.join(os.path.dirname(__file__), "../../papers_latest.json")
    output_path = os.path.normpath(output_path)
    data = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        "total": len(all_papers),
        "today_count": len(today_papers),
        "papers": all_papers[:50],  # 最新50篇
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[ArXiv日更] 数据已写入 → papers_latest.json ({len(all_papers[:50])} 篇)")

    return all_papers

if __name__ == "__main__":
    fetch_all_papers()
