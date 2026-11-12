#!/usr/bin/env python3
"""
Update script for Yasser Ouaftouh's personal website.
Fetches the latest:
  1. YouTube drone videos from @eirefly (via RSS with direct channel fallback)
  2. Chess.com blog posts from yasser-blog (with dynamic discovery and date-based reverse sorting)
and updates the corresponding YAML files in _data/.

Run anytime with:
    python3 scripts/update_content.py
"""

import sys
import os
import re
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
            yaml_lines.append(f'- id: "{v["id"]}"')
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


def update_chess_blogs():
    print("-> Fetching Chess.com blogs from yasser-blog...")
    
    # 1. Base list of known article URLs
    article_urls = [
        "https://www.chess.com/blog/yasser-blog/my-first-experience-with-chess-i-knew-how-to-play-but-not-how-to-win",
        "https://www.chess.com/blog/yasser-blog/the-queens-gambit-the-show-that-made-the-world-fall-in-love-with-chess",
        "https://www.chess.com/blog/yasser-blog/why-is-the-knight-a-horse",
        "https://www.chess.com/blog/yasser-blog/5-of-the-most-expensive-chess-sets-ever-made",
        "https://www.chess.com/blog/yasser-blog/if-chess-pieces-had-personalities",
        "https://www.chess.com/blog/yasser-blog/build-a-simple-chess-game-in-minutes",
        "https://www.chess.com/blog/yasser-blog/the-pirate-who-sacrificed-a-pawn",
        "https://www.chess.com/blog/yasser-blog/the-most-underrated-chess-openings",
        "https://www.chess.com/blog/yasser-blog/top-5-most-famous-anime-that-showcase-chess",
        "https://www.chess.com/blog/yasser-blog/5-mindset-shifts-that-will-instantly-make-you-a-better-chess-player",
        "https://www.chess.com/blog/yasser-blog/how-to-unlock-the-searching-for-bobby-fischer-secret-achievement-on-chess-com",
    ]

    # 2. Also keep any URLs already in _data/chess_blogs.yml so existing posts are never lost
    if os.path.exists(CHESS_FILE):
        try:
            with open(CHESS_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                existing_urls = re.findall(r'url:\s*\"(https?://[^\"]+)\"', content)
                for u in existing_urls:
                    if u not in article_urls:
                        article_urls.append(u)
        except Exception as e:
            print(f"Notice: Reading existing chess file: {e}")

    # 3. Discover any new posts via Chess.com blog search
    for query in ["yasseruski", "yasser-blog"]:
        try:
            search_url = f"https://www.chess.com/blog/search?keyword={urllib.parse.quote(query)}"
            req = urllib.request.Request(search_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                found_urls = re.findall(r'href=[\"\'](https?://[^\"]*chess\.com/blog/yasser-blog/[a-zA-Z0-9_\-]+)[\"\']', html)
                for u in found_urls:
                    if "register" not in u and "login" not in u and u not in article_urls:
                        print(f"Discovered new blog post: {u}")
                        article_urls.append(u)
        except Exception as e:
            print(f"Notice: search scrape for '{query}': {e}")

    posts = []
    for u in article_urls:
        req = urllib.request.Request(u, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
                img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)

                t = title.group(1) if title else "Chess Blog Post"
                thumb = img.group(1) if img else ""
                excerpt = desc.group(1) if desc else ""

                # Extract date from time tag
                time_match = re.search(r'<time[^>]*datetime=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</time>', html, re.DOTALL)
                sort_key = ""
                display_date = "Chess.com Blog"
                if time_match:
                    sort_key = time_match.group(1).strip()
                    raw_text = re.sub(r'<[^>]+>', '', time_match.group(2)).strip()
                    parts = raw_text.split(',')
                    if len(parts) >= 2:
                        display_date = parts[0].strip() + ', ' + parts[1].strip()
                    else:
                        display_date = raw_text

                # If no sort_key, extract ID from image or use fallback
                if not sort_key:
                    img_id_match = re.search(r'/blog/(\d+)\.', thumb)
                    sort_key = img_id_match.group(1) if img_id_match else u

                # Clean html entities
                t = t.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
                excerpt = excerpt.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")

                posts.append({
                    "title": t,
                    "url": u,
                    "thumbnail": thumb,
                    "date": display_date,
                    "sort_key": sort_key,
                    "excerpt": excerpt
                })
        except Exception as e:
            print(f"Error fetching {u}: {e}")

    if posts:
        # Sort in reverse chronological order (newest first)
        posts.sort(key=lambda p: p["sort_key"], reverse=True)

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


if __name__ == "__main__":
    update_drone_videos()
    update_chess_blogs()
    print("Done!")
