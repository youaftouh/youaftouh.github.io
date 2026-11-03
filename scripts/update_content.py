#!/usr/bin/env python3
"""
Update script for Yasser Ouaftouh's personal website.
Fetches the latest:
  1. YouTube drone videos from @eirefly
  2. Chess.com blog posts from yasser-blog
and updates the corresponding YAML files in _data/.

Run anytime with:
    python3 scripts/update_content.py
"""

import sys
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "_data")
DRONE_FILE = os.path.join(DATA_DIR, "drone_videos.yml")
CHESS_FILE = os.path.join(DATA_DIR, "chess_blogs.yml")

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"


def update_drone_videos():
    print("-> Fetching latest drone videos from @eirefly YouTube RSS feed...")
    channel_id = "UCMkm8dHQ2chmNv6m4NP9rvA"
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    req = urllib.request.Request(feed_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
    except Exception as e:
        print(f"Error fetching YouTube feed: {e}")
        return

    root = ET.fromstring(xml_data)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }

    entries = root.findall("atom:entry", ns)
    if not entries:
        print("No video entries found in feed.")
        return

    videos = []
    known_locations = {
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

    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]

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

        # Parse date
        date_str = ""
        try:
            parts = published.split("T")[0].split("-")
            year = parts[0]
            month = month_names[int(parts[1]) - 1]
            date_str = f"{month} {year}"
        except Exception:
            date_str = published

        # Determine location
        loc = known_locations.get(vid_id, "")
        if not loc:
            if "IE" in title or "Ireland" in title or "Wexford" in title or "Wicklow" in title or "Dublin" in title:
                loc = "Ireland"
            elif "Cologne" in title or "Germany" in title:
                loc = "Germany"
            elif "Nador" in title or "Morocco" in title:
                loc = "Morocco"
            elif "Poland" in title:
                loc = "Poland"
            else:
                loc = "Aerial Film"

        videos.append({
            "id": vid_id,
            "title": title,
            "thumbnail": thumb,
            "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
            "location": loc,
            "date": date_str
        })

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


def update_chess_blogs():
    print("-> Fetching Chess.com blogs from yasser-blog...")
    article_urls = [
        "https://www.chess.com/blog/yasser-blog/the-queens-gambit-the-show-that-made-the-world-fall-in-love-with-chess",
        "https://www.chess.com/blog/yasser-blog/5-of-the-most-expensive-chess-sets-ever-made",
        "https://www.chess.com/blog/yasser-blog/the-pirate-who-sacrificed-a-pawn",
        "https://www.chess.com/blog/yasser-blog/5-mindset-shifts-that-will-instantly-make-you-a-better-chess-player",
    ]

    # Try discovering additional posts dynamically from the blog index
    try:
        index_req = urllib.request.Request("https://www.chess.com/blog/yasser-blog", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(index_req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            found_urls = re.findall(r'href=[\"\'](https://www.chess.com/blog/yasser-blog/[a-zA-Z0-9_-]+)[\"\']', html)
            for u in found_urls:
                if u not in article_urls:
                    article_urls.append(u)
    except Exception as e:
        print(f"Notice: blog index scrape: {e}")

    posts = []
    for u in article_urls:
        req = urllib.request.Request(u, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
                title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
                desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)

                t = title.group(1) if title else "Chess Blog Post"
                thumb = img.group(1) if img else ""
                excerpt = desc.group(1) if desc else ""
                # Clean html entities
                t = t.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
                excerpt = excerpt.replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")

                posts.append({
                    "title": t,
                    "url": u,
                    "thumbnail": thumb,
                    "date": "Chess.com Blog",
                    "excerpt": excerpt
                })
        except Exception as e:
            print(f"Error fetching {u}: {e}")

    if posts:
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
        print(f"✓ Updated {CHESS_FILE} with {len(posts)} posts.")


if __name__ == "__main__":
    update_drone_videos()
    update_chess_blogs()
    print("Done!")
