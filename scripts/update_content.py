#!/usr/bin/env python3
"""
Update script for Yasser Ouaftouh's personal website.
Fetches the latest:
  1. YouTube drone videos from @eirefly (via RSS with direct channel fallback)
  2. Chess.com blog posts from yasser-blog via Chess.com member activity API
     (with date-based reverse sorting and fallback preservation)
and updates the corresponding YAML files in _data/.

Run anytime with:
    python3 scripts/update_content.py
"""

import sys
import os
import re
import json
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "_data")
DRONE_FILE = os.path.join(DATA_DIR, "drone_videos.yml")
CHESS_FILE = os.path.join(DATA_DIR, "chess_blogs.yml")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}
API_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}

KNOWN_DRONE_LOCATIONS = {
    "iMlPiBvgdKE": "Co. Wexford, Ireland",
    "b7JBlVZCg8w": "Nador, Morocco",
    "HaqDH3Xhlmk": "Cologne, Germany",
    "kEUDAkEFlDI": "Co. Wicklow, Ireland",
    "6UgYkR3rRdk": "Łochów, Poland",
    "2OM9ucFEG2E": "Nador, Morocco",
    "TCStNOvfqFg": "Dublin, Ireland",
    "8RN9peu5Y2k": "Dublin, Ireland",
    "VEHnEv2_DXo": "Dublin, Ireland",
    "YkI4yjkr1Q8": "Dublin, Ireland",
    "mAT62iYsP9I": "Cologne, Germany",
}

MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def infer_location(title, vid_id=""):
    if vid_id in KNOWN_DRONE_LOCATIONS:
        return KNOWN_DRONE_LOCATIONS[vid_id]
    if any(k in title for k in ["IE", "Ireland", "Wexford", "Wicklow", "Dublin", "Park", "Cliff"]):
        return "Ireland"
    if any(k in title for k in ["Cologne", "Germany", "Rhein"]):
        return "Germany"
    if any(k in title for k in ["Nador", "Morocco", "الناظور"]):
        return "Morocco"
    if "Poland" in title:
        return "Poland"
    return "Aerial Film"


def update_drone_videos():
    print("-> Fetching latest drone videos from @eirefly...")
    channel_id = "UCMkm8dHQ2chmNv6m4NP9rvA"
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    videos = []
    feed_success = False

    # 1. Try YouTube RSS feed
    try:
        req = urllib.request.Request(feed_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "media": "http://search.yahoo.com/mrss/",
            }
            entries = root.findall("atom:entry", ns)
            if entries:
                for entry in entries:
                    vid_id = entry.find("yt:videoId", ns).text
                    title = entry.find("atom:title", ns).text
                    published = entry.find("atom:published", ns).text
                    media_group = entry.find("media:group", ns)
                    thumb = f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"
                    if media_group is not None:
                        thumb_elem = media_group.find("media:thumbnail", ns)
                        if thumb_elem is not None and "url" in thumb_elem.attrib:
                            thumb = thumb_elem.attrib["url"]

                    date_str = published
                    try:
                        parts = published.split("T")[0].split("-")
                        year = parts[0]
                        month = MONTH_NAMES[int(parts[1]) - 1]
                        date_str = f"{month} {year}"
                    except Exception:
                        pass

                    videos.append({
                        "id": vid_id,
                        "title": title,
                        "thumbnail": thumb,
                        "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
                        "location": infer_location(title, vid_id),
                        "date": date_str
                    })
                feed_success = True
                print(f"✓ Retrieved {len(videos)} videos from RSS feed.")
    except Exception as e:
        print(f"Notice: RSS feed retrieval returned: {e}")

    # 2. Fallback: scrape directly from channel page if RSS failed or was empty
    if not feed_success or not videos:
        print("-> Using fallback: scraping @eirefly channel page directly...")
        try:
            chan_url = "https://www.youtube.com/@eirefly/videos"
            req = urllib.request.Request(chan_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                matches = re.findall(r'\"videoId\":\"([a-zA-Z0-9_\-]{11})\".*?\"lockupMetadataViewModel\":\{\"title\":\{\"content\":\"([^\"]+)\"\}', html)
                seen_ids = set()
                for vid_id, title in matches:
                    if vid_id not in seen_ids:
                        seen_ids.add(vid_id)
                        clean_title = title.replace("\\u0026", "&").replace("&quot;", '"').replace("&#39;", "'")
                        videos.append({
                            "id": vid_id,
                            "title": clean_title,
                            "thumbnail": f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg",
                            "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
                            "location": infer_location(clean_title, vid_id),
                            "date": "Aerial Film"
                        })
                if videos:
                    print(f"✓ Scraped {len(videos)} videos from channel page.")
        except Exception as e:
            print(f"Notice: Direct channel scrape failed: {e}")

    if videos:
        yaml_lines = ["# Drone videos from @eirefly YouTube channel (https://www.youtube.com/@eirefly/videos)"]
        for v in videos:
            clean_title = v["title"].replace('"', '\\"')
            yaml_lines.append(f'- id: "{clean_title}"' if False else f'- id: "{v["id"]}"')
            yaml_lines.append(f'  title: "{clean_title}"')
            yaml_lines.append(f'  thumbnail: "{v["thumbnail"]}"')
            yaml_lines.append(f'  youtube_url: "{v["youtube_url"]}"')
            yaml_lines.append(f'  location: "{v["location"]}"')
            yaml_lines.append(f'  date: "{v["date"]}"')
            yaml_lines.append("")

        with open(DRONE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines).strip() + "\n")
        print(f"✓ Updated {DRONE_FILE} with {len(videos)} videos.")
    else:
        print(f"Kept existing {DRONE_FILE} (no new video updates retrieved).")


def clean_text(text):
    if not text:
        return ""
    text = text.replace("&quot;", '"').replace("&#039;", "'").replace("&#39;", "'").replace("&amp;", "&")
    text = text.replace("&nbsp;", " ").replace("\u00a0", " ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def update_chess_blogs():
    print("-> Fetching Chess.com blogs from yasser-blog...")
    username = "yasseruski"
    posts = []
    seen_urls = set()

    # 1. Primary Method: Fetch from Chess.com member activity endpoint (paginated)
    # This officially indexes all blog posts published by the user in chronological order.
    try:
        for page in range(1, 10):
            api_url = f"https://www.chess.com/callback/member/activity/{username}?page={page}"
            req = urllib.request.Request(api_url, headers=API_HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("recentContents", [])
                if not items:
                    break
                page_blogs = [it for it in items if it.get("type") == "blog"]
                if not page_blogs and page > 1:
                    break
                for b in page_blogs:
                    sub_url = b.get("url", "")
                    if not sub_url:
                        continue
                    full_url = f"https://www.chess.com/blog/{sub_url}" if not sub_url.startswith("http") else sub_url
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        raw_title = b.get("title", "") or "Chess Blog Post"
                        raw_body = b.get("body", "") or ""
                        raw_img = b.get("image", "") or ""
                        date_str = b.get("localized_date", "") or "Chess.com Blog"
                        sort_key = b.get("create_date", "") or ""

                        # Clean excerpt
                        excerpt = clean_text(raw_body)
                        if len(excerpt) > 280:
                            excerpt = excerpt[:277] + "..."

                        posts.append({
                            "id": b.get("id"),
                            "title": clean_text(raw_title),
                            "url": full_url,
                            "thumbnail": raw_img,
                            "date": date_str,
                            "sort_key": sort_key,
                            "excerpt": excerpt
                        })
    except Exception as e:
        print(f"Notice: Chess.com member activity API error: {e}")

    # 2. Check any existing entries in _data/chess_blogs.yml to preserve older/existing entries
    existing_entries = {}
    if os.path.exists(CHESS_FILE):
        try:
            with open(CHESS_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = content.split("- title:")
            for b in blocks[1:]:
                block_text = "- title:" + b
                u_m = re.search(r'url:\s*\"([^\"]+)\"', block_text)
                t_m = re.search(r'- title:\s*\"([^\"]+)\"', block_text)
                img_m = re.search(r'thumbnail:\s*\"([^\"]+)\"', block_text)
                d_m = re.search(r'date:\s*\"([^\"]+)\"', block_text)
                e_m = re.search(r'excerpt:\s*\"([^\"]+)\"', block_text)
                if u_m and t_m:
                    existing_entries[u_m.group(1)] = {
                        "title": t_m.group(1),
                        "url": u_m.group(1),
                        "thumbnail": img_m.group(1) if img_m else "",
                        "date": d_m.group(1) if d_m else "Chess.com Blog",
                        "sort_key": d_m.group(1) if d_m else "",
                        "excerpt": e_m.group(1) if e_m else ""
                    }
        except Exception as e:
            print(f"Notice: Reading existing chess file: {e}")

    # 3. For any post where thumbnail is missing, fetch article page og:image
    for p in posts:
        if not p["thumbnail"]:
            try:
                req = urllib.request.Request(p["url"], headers=HEADERS)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                    img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                    if img:
                        p["thumbnail"] = img.group(1)
            except Exception as e:
                print(f"Notice: fetching og:image for {p['url']}: {e}")

    # 4. If any existing entry wasn't returned by API, keep it
    for u, entry in existing_entries.items():
        if u not in seen_urls:
            seen_urls.add(u)
            posts.append(entry)

    if posts:
        # Sort in reverse chronological order (newest first)
        posts.sort(key=lambda p: p.get("sort_key", ""), reverse=True)

        yaml_lines = ["# Chess.com blogs by Yasser (yasser-blog / yasseruski)"]
        for p in posts:
            clean_title = p["title"].replace('"', '\\"')
            clean_excerpt = p["excerpt"].replace('"', '\\"')
            yaml_lines.append(f'- title: "{clean_title}"')
            yaml_lines.append(f'  url: "{p["url"]}"')
            yaml_lines.append(f'  thumbnail: "{p["thumbnail"]}"')
            yaml_lines.append(f'  date: "{p["date"]}"')
            yaml_lines.append(f'  excerpt: "{clean_excerpt}"')
            yaml_lines.append("")

        with open(CHESS_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines).strip() + "\n")
        print(f"✓ Updated {CHESS_FILE} with {len(posts)} posts (newest first).")
    else:
        print(f"Kept existing {CHESS_FILE} (no posts retrieved).")


if __name__ == "__main__":
    update_drone_videos()
    update_chess_blogs()
    print("Done!")
